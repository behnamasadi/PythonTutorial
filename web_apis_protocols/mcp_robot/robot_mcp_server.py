"""MCP server that exposes the toy robot from robot.py.

Run it directly to speak MCP over stdin/stdout:

    python robot_mcp_server.py

Every function decorated below becomes something an MCP client can discover
and use. The SDK turns the type hints and docstrings into JSON Schema.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from mcp.server.mcpserver import MCPServer
from robot import HEIGHT, WIDTH, Robot

robot = Robot()

server = MCPServer(
    "robot",
    instructions=(
        f"Controls a robot on a {WIDTH}x{HEIGHT} grid. (0, 0) is the bottom-left corner, "
        f"x grows to the right, y grows upwards, so the top-left corner is (0, {HEIGHT - 1})."
    ),
)


class Pose(BaseModel):
    x: int = Field(description="column, 0 = left edge")
    y: int = Field(description="row, 0 = bottom edge")


class MoveResult(Pose):
    moved: int = Field(description="cells actually moved")
    hit_wall: bool = Field(description="true if the robot stopped early at the edge of the grid")


# ---- tools: actions the client can invoke ----------------------------------


@server.tool()
def get_pose() -> Pose:
    """Return the robot's current position on the grid."""
    return Pose(**robot.pose())


@server.tool()
def move(
    direction: Annotated[Literal["up", "down", "left", "right"], Field(description="direction to move in")],
    steps: Annotated[int, Field(ge=1, le=max(WIDTH, HEIGHT), description="number of cells to move")] = 1,
) -> MoveResult:
    """Move the robot a number of cells in one direction. It stops at the edge of the grid."""
    return MoveResult(**robot.move(direction, steps))


@server.tool()
def go_to(
    x: Annotated[int, Field(ge=0, lt=WIDTH, description="target column")],
    y: Annotated[int, Field(ge=0, lt=HEIGHT, description="target row")],
) -> Pose:
    """Drive the robot to the cell (x, y)."""
    return Pose(**robot.go_to(x, y))


Corner = Literal["top-left", "top-right", "bottom-right", "bottom-left"]


class CornerVisit(Pose):
    corner: Corner


@server.tool()
def patrol_corners(
    start: Annotated[Corner, Field(description="corner to visit first")] = "top-left",
    clockwise: Annotated[bool, Field(description="true for clockwise, false for counter-clockwise")] = True,
) -> list[CornerVisit]:
    """Drive through all four corners in clockwise or counter-clockwise order, beginning at `start`."""
    return [CornerVisit(**v) for v in robot.patrol_corners(start, clockwise)]


@server.tool()
def reset() -> Pose:
    """Put the robot back in the centre of the grid and clear its path."""
    return Pose(**robot.reset())


# ---- resources: read-only data the client can fetch ------------------------


@server.resource("robot://world", mime_type="application/json")
def world() -> dict:
    """Grid size, coordinate convention and named places."""
    return {
        "width": WIDTH,
        "height": HEIGHT,
        "origin": "bottom-left",
        "x_axis": "grows to the right",
        "y_axis": "grows upwards",
        "places": {
            "bottom-left": [0, 0],
            "bottom-right": [WIDTH - 1, 0],
            "top-left": [0, HEIGHT - 1],
            "top-right": [WIDTH - 1, HEIGHT - 1],
            "centre": [WIDTH // 2, HEIGHT // 2],
        },
    }


@server.resource("robot://path", mime_type="application/json")
def path() -> list[list[int]]:
    """Every cell the robot has visited since the last reset, in order."""
    return [list(p) for p in robot.path]


# ---- prompts: reusable message templates the client can offer to a user -----


@server.prompt()
def tour(places: str = "the four corners") -> str:
    """Ask for a tour through the given places."""
    return f"Drive the robot to {places}, in that order, then report where it ended up."


if __name__ == "__main__":
    server.run()  # stdio transport by default
