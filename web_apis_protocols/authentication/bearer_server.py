# bearer_server.py - Bearer token (opaque)
import secrets
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException

try:
    from .server_common import USERS, ACCESS_TOKENS, constant_time_eq
except ImportError:
    from server_common import USERS, ACCESS_TOKENS, constant_time_eq

router = APIRouter(tags=["bearer-auth"])


@router.post("/auth/token/login")
async def token_login(request: Request):
    body = await request.json()
    username = body.get("username", "")
    password = body.get("password", "")

    u = USERS.get(username)
    if not u or not constant_time_eq(u["password"], password):
        raise HTTPException(
            status_code=401, detail="Invalid username/password")

    token = secrets.token_urlsafe(32)
    ACCESS_TOKENS[token] = username
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}


def auth_bearer(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = auth.removeprefix("Bearer ").strip()
    username = ACCESS_TOKENS.get(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    return username


@router.get("/protected/bearer")
def protected_bearer(username: str = Depends(auth_bearer)):
    return {"ok": True, "method": "bearer-opaque", "user": username}


app = FastAPI(title="Auth Playground - Bearer")
app.include_router(router)
