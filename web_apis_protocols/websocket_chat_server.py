"""Simple multi-client WebSocket chat server using FastAPI."""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


class ConnectionManager:
    """Manages active WebSocket connections and broadcasts messages."""

    def __init__(self):
        self.connections: dict[WebSocket, str] = {}  # ws -> username
        self._guest_count = 0

    async def connect(self, ws: WebSocket) -> str:
        await ws.accept()
        self._guest_count += 1
        username = f"Guest-{self._guest_count}"
        self.connections[ws] = username
        return username

    def set_username(self, ws: WebSocket, username: str) -> None:
        if ws in self.connections:
            self.connections[ws] = username.strip() or self.connections[ws]

    def disconnect(self, ws: WebSocket) -> str | None:
        username = self.connections.pop(ws, None)
        return username

    async def broadcast(self, message: str) -> None:
        for ws in list(self.connections.keys()):
            try:
                await ws.send_text(message)
            except Exception:
                pass


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_chat(ws: WebSocket):
    username = await manager.connect(ws)
    await manager.broadcast(f"[{username} joined the chat]")

    try:
        while True:
            data = await ws.receive_text()

            # First non-empty message can set username: /nick Alice
            if data.startswith("/nick ") and len(data) > 6:
                new_name = data[6:].strip()
                if new_name:
                    manager.set_username(ws, new_name)
                    await ws.send_text(f"[You are now {new_name}]")
                continue
            if not data.strip():
                continue

            username = manager.connections.get(ws, "?")
            await manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        name = manager.disconnect(ws)
        if name:
            await manager.broadcast(f"[{name} left the chat]")


@app.get("/", response_class=HTMLResponse)
async def chat_page():
    """Serve a simple chat client for testing."""
    return CHAT_HTML


CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 2rem auto; }
        #messages { height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 0.5rem; margin-bottom: 0.5rem; }
        #messages p { margin: 0.25rem 0; }
        #input { display: flex; gap: 0.5rem; }
        #msg { flex: 1; padding: 0.5rem; }
        button { padding: 0.5rem 1rem; cursor: pointer; }
    </style>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <div id="messages"></div>
    <div id="input">
        <input type="text" id="msg" placeholder="Type a message..." />
        <button id="send">Send</button>
    </div>
    <p><small>Use /nick YourName to change your name</small></p>

    <script>
        const ws = new WebSocket("ws://" + location.host + "/ws");
        const messages = document.getElementById("messages");
        const input = document.getElementById("msg");
        const sendBtn = document.getElementById("send");

        function addMsg(text, isSystem = false) {
            const p = document.createElement("p");
            p.textContent = text;
            if (isSystem) p.style.color = "#666";
            messages.appendChild(p);
            messages.scrollTop = messages.scrollHeight;
        }

        ws.onopen = () => addMsg("[Connected]", true);
        ws.onclose = () => addMsg("[Disconnected]", true);
        ws.onerror = () => addMsg("[Error]", true);
        ws.onmessage = (e) => addMsg(e.data);

        function send() {
            const text = input.value.trim();
            if (text && ws.readyState === WebSocket.OPEN) {
                ws.send(text);
                input.value = "";
            }
        }

        sendBtn.onclick = send;
        input.onkeydown = (e) => { if (e.key === "Enter") send(); };
    </script>
</body>
</html>
"""
