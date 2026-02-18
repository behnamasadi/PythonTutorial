from pydantic import BaseModel
from fastapi import FastAPI, Request
import hmac
import hashlib
from fastapi import Header, HTTPException, Request

SECRET = b"my_shared_secret"


class WebhookEvent(BaseModel):
    event: str
    object_id: int


app = FastAPI()


@app.post("/webhook")
async def webhook(event: WebhookEvent):
    print("Event:", event.event)
    print("Object ID:", event.object_id)
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(event: WebhookEvent):
    if event.event == "user_created":
        handle_user_created(event.object_id)
    elif event.event == "payment_succeeded":
        handle_payment(event.object_id)
    else:
        print("Unknown event:", event.event)

    return {"status": "ok"}


def verify_signature(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        SECRET,
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
