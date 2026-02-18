from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()


class Item(BaseModel):
    name: str
    count: int


@app.get("/ping")
def ping():
    return {"ok": True}


@app.get("/item/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": "demo", "count": 3}


@app.post("/items")
def create_item(item: Item, x_token: str | None = Header(default=None)):
    if x_token != "secret":
        raise HTTPException(status_code=401, detail="bad token")
    return {"created": True, "item": item}


@app.get("/slow")
def slow(ms: int = 500):
    time.sleep(ms / 1000.0)
    return {"slept_ms": ms}
