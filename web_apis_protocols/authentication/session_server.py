# session_server.py - Session-based authentication (cookies)
import secrets
from fastapi import APIRouter, FastAPI, Request, Response, Depends, HTTPException

try:
    from .server_common import USERS, SESSIONS, SESSION_COOKIE_NAME, constant_time_eq
except ImportError:
    from server_common import USERS, SESSIONS, SESSION_COOKIE_NAME, constant_time_eq

router = APIRouter(tags=["session-auth"])


@router.post("/auth/session/login")
async def session_login(request: Request, response: Response):
    body = await request.json()
    username = body.get("username", "")
    password = body.get("password", "")

    u = USERS.get(username)
    if not u or not constant_time_eq(u["password"], password):
        raise HTTPException(
            status_code=401, detail="Invalid username/password")

    sid = secrets.token_urlsafe(24)
    SESSIONS[sid] = username

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=sid,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60
    )
    return {"ok": True, "method": "session", "message": "logged_in"}


def auth_session(request: Request) -> str:
    sid = request.cookies.get(SESSION_COOKIE_NAME)
    if not sid:
        raise HTTPException(status_code=401, detail="Missing session cookie")
    username = SESSIONS.get(sid)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid/expired session")
    return username


@router.get("/protected/session")
def protected_session(username: str = Depends(auth_session)):
    return {"ok": True, "method": "session", "user": username}


app = FastAPI(title="Auth Playground - Session")
app.include_router(router)
