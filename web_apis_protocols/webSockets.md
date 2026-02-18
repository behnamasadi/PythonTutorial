## 1. What Is a WebSocket (in plain terms)

A **WebSocket** is a **long-lived, two-way connection** between a client and a server.

Think of it like a **phone call** instead of sending letters:

* REST = send a letter, wait for reply, hang up
* WebSocket = call once, talk back and forth anytime

**Key idea**

* One connection
* Both sides can send messages anytime
* No polling
* Very low latency

---

## 2. Why Not Just Use REST?

With REST, the client must keep asking:

```text
Client: Any new message?
Server: No
Client: Any new message?
Server: No
Client: Any new message?
Server: Yes
```

With WebSocket:

```text
Server: New message!
```

No asking.

---

## 3. Where WebSockets Are Used

* Chat applications
* Live notifications
* Multiplayer games
* Live dashboards
* Trading systems
* Collaborative editors

---

## 4. How WebSockets Work (Conceptually)

### Step 1: HTTP handshake

Client sends an HTTP request saying:

> “Upgrade this connection to WebSocket”

### Step 2: Protocol upgrade

Server agrees and upgrades the connection.

### Step 3: Persistent channel

Now both sides can send messages at any time.

```
Client  ⇄  Server
     WebSocket
```

---

## 5. Minimal Python WebSocket Server (FastAPI)

### Install dependencies

```bash
pip install fastapi uvicorn
```

---

### Server code

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        message = await ws.receive_text()
        await ws.send_text(f"Echo: {message}")
```

Run it:

```bash
uvicorn main:app --reload
```

---

## 6. Simple WebSocket Client (Browser)

Open your browser console and run:

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onmessage = (event) => {
  console.log("Server says:", event.data);
};

ws.onopen = () => {
  ws.send("Hello WebSocket");
};
```

Output:

```text
Server says: Echo: Hello WebSocket
```

---

## 7. What Just Happened

1. Browser opened a WebSocket connection
2. Server accepted it
3. Client sent a message
4. Server responded
5. Connection stayed open

No new HTTP request.

---

## 8. Important Properties to Know

### WebSocket is stateful

* Server remembers the connection
* You can store per-client data

### WebSocket is bidirectional

* Server can push messages without request

### WebSocket runs over TCP

* Reliable
* Ordered
* Low latency

---

## 9. WebSocket vs Webhook (Quick Contrast)

| Feature             | WebSocket | Webhook         |
| ------------------- | --------- | --------------- |
| Direction           | Both ways | Server → server |
| Persistent          | Yes       | No              |
| Browser friendly    | Yes       | No              |
| Real-time           | Yes       | Yes (async)     |
| Requires public URL | No        | Yes             |

---

## 10. Common Beginner Mistakes

❌ Using WebSocket for CRUD APIs
❌ Expecting WebSocket to scale without message queues
❌ Forgetting reconnect logic
❌ No authentication on connection

---

## 11. When NOT to Use WebSockets

* Simple request/response APIs
* Rare updates
* Stateless services
* Background jobs

---

## 12. One-Line Mental Model

> **WebSocket = keep the pipe open and talk anytime**

---

