# REST API + FastAPI — A Simple Tutorial

## 1. What is a REST API?

A **REST API** is a way for programs to talk to each other over **HTTP**.

It is based on:

* **Resources** (things): users, items, orders, sensors
* **URLs** identifying resources
* **HTTP methods** describing actions
* **Status codes** describing results
* **JSON** as the most common data format

### Core HTTP methods

| Method | Meaning        | Example            |
| ------ | -------------- | ------------------ |
| GET    | Read data      | Get an item        |
| POST   | Create data    | Create a new item  |
| PUT    | Replace data   | Update entire item |
| PATCH  | Partial update | Update one field   |
| DELETE | Remove data    | Delete an item     |

Example:

```
GET /items/42
```

Means: *“Give me item with id = 42”*

---

## 2. REST Design Basics

### Resources, not actions

❌ Bad:

```
/getItem
/createUser
```

✅ Good:

```
GET    /items/42
POST   /users
DELETE /users/7
```

### Status codes matter

| Code | Meaning      |
| ---- | ------------ |
| 200  | OK           |
| 201  | Created      |
| 400  | Bad request  |
| 401  | Unauthorized |
| 404  | Not found    |
| 500  | Server error |

---


## 5. Your First FastAPI Server

Create a file called `rest_server.py`

```python
from fastapi import FastAPI

# Create the FastAPI application instance. This is the central object that
# holds all routes, middleware, and configuration for your REST API.
app = FastAPI()

# @app.get("/ping") is a decorator that does two things:
#   1. Registers the function below as a route handler
#   2. Binds it to HTTP GET requests at the path "/ping"
# When a client sends GET /ping, FastAPI calls the ping() function and
# returns its return value as JSON (FastAPI auto-serializes dicts to JSON).
@app.get("/ping")
def ping():
    return {"message": "pong"}
```

Run the rest_server:

```bash
uvicorn rest_server:app --reload --port 8000
```

Open browser:

```
http://localhost:8000/ping
```

Response:

```json
{
  "message": "pong"
}
```

---

## 6. Automatic API Documentation

FastAPI generates docs for you.

Open:

```
http://localhost:8000/docs
```

You get:

* Swagger UI
* Interactive testing
* Request/response schemas

This is extremely useful when writing clients.

---

## 7. Path Parameters

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "id": item_id,
        "name": "example",
        "count": 3
    }
```

Request:

```
GET /items/5
```

Response:

```json
{
  "id": 5,
  "name": "example",
  "count": 3
}
```

FastAPI automatically:

* Parses the URL
* Converts to int
* Returns 422 if type is wrong

---

## 8. Query Parameters

```python
@app.get("/search")
def search_items(q: str, limit: int = 10):
    return {
        "query": q,
        "limit": limit
    }
```

Request:

```
GET /search?q=camera&limit=5
```

---

## 9. JSON Request Body (POST)

**POST** is used to *create* or *submit* data. Unlike GET (which reads data and has no body), POST sends a **request body** containing the payload (often JSON). This is the standard way to create new resources in REST.

Define a data model using **Pydantic**. FastAPI uses this for validation and OpenAPI docs:

```python
from pydantic import BaseModel

# BaseModel defines the expected shape of the incoming JSON.
# FastAPI will parse the body, validate against these types, and return 422 if invalid.
class Item(BaseModel):
    name: str   # required string
    count: int  # required integer
```

Create the endpoint. Use `@app.post` (not `@app.get`) because we are *creating* data:

```python
@app.post("/items")
def create_item(item: Item):
    # 'item' is automatically parsed from the JSON body and validated
    return {
        "created": True,
        "item": item
    }
```

Request (client sends JSON in the body):

```json
{
  "name": "sensor",
  "count": 4
}
```

Example with curl:

```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "sensor", "count": 4}'
```

FastAPI automatically:

* Parses the JSON request body into the Pydantic model
* Validates types (e.g. rejects `"count": "four"` because count must be `int`)
* Returns 422 Unprocessable Entity with error details if validation fails

---

## 10. Headers (Authentication Example)

```python
from fastapi import Header, HTTPException

@app.post("/secure")
def secure_endpoint(x_token: str | None = Header(default=None)):
    if x_token != "secret":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"ok": True}
```

Client must send:

```
X-Token: secret
```

---

## 11. Error Handling

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid item id"
        )
    return {"id": item_id}
```

This is essential for client-side testing.

---

## 12. Simulating Slow or Failing Endpoints

Useful for timeout and retry logic in C++.

```python
import time

@app.get("/slow")
def slow(ms: int = 500):
    time.sleep(ms / 1000.0)
    return {"slept_ms": ms}
```

---

## 13. Typical REST API Structure

```
server.py
models.py
routes/
  items.py
  users.py
```

Example separation:

```python
app.include_router(items.router)
```

This mirrors real production services.

---
