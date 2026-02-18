# Webhooks with FastAPI — A Simple Tutorial

## 1. What is a webhook?

A **webhook** is an HTTP endpoint that receives data **when an event happens** in another system.

Instead of your app asking:

* “Did something happen?”

The other system tells you:

* “Something happened — here is the data.”

Technically:

* HTTP request
* Usually `POST`
* Payload is JSON
* Your server processes it

---

## 2. Why FastAPI for webhooks?

FastAPI is ideal for webhooks because it provides:

* Fast async request handling
* Automatic JSON parsing
* Input validation via Pydantic
* Clean error handling
* Background task support
* Production-ready ASGI stack

---

## 3. Install dependencies

```bash
pip install fastapi uvicorn
```

---

## 4. Minimal webhook server

### `main.py`

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    payload = await request.json()
    print("Received webhook:", payload)
    return {"status": "ok"}
```

Run the server:

```bash
uvicorn main:app --reload --port 8000
```

Webhook URL:

```
http://localhost:8000/webhook
```

---

## 5. Test the webhook locally

```bash
curl -X POST http://localhost:8000/webhook \
     -H "Content-Type: application/json" \
     -d '{"event":"user_created","user_id":42}'
```

Console output:

```
Received webhook: {'event': 'user_created', 'user_id': 42}
```

This is a complete webhook round trip.

---

## 6. Validate webhook payloads with Pydantic

Validation is critical in webhook handlers.

```python
from pydantic import BaseModel

class WebhookEvent(BaseModel):
    event: str
    object_id: int

@app.post("/webhook")
async def webhook(event: WebhookEvent):
    print("Event:", event.event)
    print("Object ID:", event.object_id)
    return {"status": "ok"}
```

If invalid data is sent, FastAPI automatically returns `422 Unprocessable Entity`.

---

## 7. Handling multiple event types

```python
@app.post("/webhook")
async def webhook(event: WebhookEvent):
    if event.event == "user_created":
        handle_user_created(event.object_id)
    elif event.event == "payment_succeeded":
        handle_payment(event.object_id)
    else:
        print("Unknown event:", event.event)

    return {"status": "ok"}
```

Webhook handlers usually route logic based on `event`.

---

## 8. Verifying webhook signatures (important)

In production, **never trust incoming webhooks blindly**.

Most providers sign webhook payloads using HMAC.

### Signature verification example

```python
import hmac
import hashlib
from fastapi import Header, HTTPException, Request

SECRET = b"my_shared_secret"

def verify_signature(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        SECRET,
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

Usage:

```python
@app.post("/webhook")
async def webhook(
    request: Request,
    x_signature: str = Header(None)
):
    body = await request.body()

    if not verify_signature(body, x_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()
    print("Verified webhook:", payload)

    return {"status": "ok"}
```

This prevents forged webhook requests.

---

## 9. Respond fast and process asynchronously

Webhook providers expect **fast responses**.
Long processing causes retries or failures.

Use background tasks:

```python
from fastapi import BackgroundTasks

def process_event(event: WebhookEvent):
    print("Processing:", event)

@app.post("/webhook")
async def webhook(
    event: WebhookEvent,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(process_event, event)
    return {"status": "accepted"}
```

This returns immediately while work continues.

---

## 10. Expose your webhook during development

To receive webhooks from external services on localhost:

```bash
ngrok http 8000
```

You’ll get a public URL like:

```
https://abcd1234.ngrok.io/webhook
```

Register this URL with the webhook provider.

---

## 11. Common webhook mistakes

* Not verifying signatures
* Doing heavy work inside the request
* Assuming events are delivered only once
* Not handling retries
* Not validating payload structure

---

## 12. Mental model

Think of a webhook as:

> “Another system calling my function over HTTP with JSON data.”

Everything else is:

* Validation
* Security
* Fast responses
* Idempotent processing

---

## 13. When to use webhooks

Use webhooks when you need:

* Real-time notifications
* Event-driven architecture
* Efficient integration with external systems

Typical events:

* Payments
* File uploads
* CI results
* Device or sensor updates

---

### Summary

* FastAPI is excellent for webhooks
* Easy to implement
* Safe and fast by default
* Scales cleanly to production

---

If you want next steps, I can show:

* Idempotent webhook handling
* Webhooks with database persistence
* Webhooks + message queues
* A production FastAPI webhook template

Just tell me what you want next.
