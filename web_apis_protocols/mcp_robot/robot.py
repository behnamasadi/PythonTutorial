"""A toy robot with an ordinary Python API.

Nothing in this file knows about MCP or LLMs: it is the "existing system"
that the MCP server in robot_mcp_server.py exposes to the outside world.

World: a grid of WIDTH x HEIGHT cells. The origin (0, 0) is the bottom-left
corner, x grows to the right and y grows upwards, so the top-left corner is
(0, HEIGHT - 1).
"""

from dataclasses import dataclass, field

WIDTH = 10
HEIGHT = 10

# unit step for each direction, as (dx, dy)
DIRECTIONS = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}


@dataclass
class Robot:
    width: int = WIDTH
    height: int = HEIGHT
    x: int = WIDTH // 2
    y: int = HEIGHT // 2
    path: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        self.path = [(self.x, self.y)]

    def pose(self) -> dict:
        """Current position."""
        return {"x": self.x, "y": self.y}

    def move(self, direction: str, steps: int = 1) -> dict:
        """Move `steps` cells in `direction`; stops at the wall instead of leaving the grid."""
        if direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction!r}, expected one of {list(DIRECTIONS)}")
        if steps < 1:
            raise ValueError("steps must be >= 1")
        dx, dy = DIRECTIONS[direction]
        moved = 0
        for _ in range(steps):
            nx, ny = self.x + dx, self.y + dy
            if not (0 <= nx < self.width and 0 <= ny < self.height):
                break
            self.x, self.y = nx, ny
            self.path.append((nx, ny))
            moved += 1
        return {"x": self.x, "y": self.y, "moved": moved, "hit_wall": moved < steps}

    def go_to(self, x: int, y: int) -> dict:
        """Drive to cell (x, y): first along x, then along y."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"({x}, {y}) is outside the {self.width}x{self.height} grid")
        if x != self.x:
            self.move("right" if x > self.x else "left", abs(x - self.x))
        if y != self.y:
            self.move("up" if y > self.y else "down", abs(y - self.y))
        return self.pose()

    def corners(self) -> dict[str, tuple[int, int]]:
        """The four corners, listed clockwise starting at the top-left."""
        w, h = self.width - 1, self.height - 1
        return {"top-left": (0, h), "top-right": (w, h), "bottom-right": (w, 0), "bottom-left": (0, 0)}

    def patrol_corners(self, start: str = "top-left", clockwise: bool = True) -> list[dict]:
        """Visit all four corners in order, beginning at `start`; returns the pose after each corner."""
        names = list(self.corners())
        if start not in names:
            raise ValueError(f"unknown corner {start!r}, expected one of {names}")
        if not clockwise:
            names.reverse()
        i = names.index(start)
        visits = []
        for name in names[i:] + names[:i]:
            visits.append({"corner": name, **self.go_to(*self.corners()[name])})
        return visits

    def reset(self) -> dict:
        """Back to the centre of the grid, with an empty path."""
        self.x, self.y = self.width // 2, self.height // 2
        self.path = [(self.x, self.y)]
        return self.pose()


def plot_path(path, width=WIDTH, height=HEIGHT, title="Robot path"):
    """Draw the path coloured by step number (dark = early, yellow = late), the start and the end."""
    import matplotlib.pyplot as plt

    xs, ys = zip(*path)
    fig, ax = plt.subplots(figsize=(4.8, 4))
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    ax.grid(True, alpha=0.3)
    ax.set_aspect("equal")
    ax.plot(xs, ys, "-", color="lightgray", zorder=1)
    dots = ax.scatter(xs, ys, c=range(len(path)), cmap="viridis", s=30, zorder=2)
    fig.colorbar(dots, ax=ax, label="step")
    ax.plot(xs[0], ys[0], "o", markersize=16, markerfacecolor="none", markeredgecolor="tab:green", markeredgewidth=2, label="start", zorder=3)
    ax.plot(xs[-1], ys[-1], "x", markersize=12, color="tab:red", markeredgewidth=3, label="end", zorder=4)
    ax.set_title(title)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=8, frameon=False)
    plt.show()
