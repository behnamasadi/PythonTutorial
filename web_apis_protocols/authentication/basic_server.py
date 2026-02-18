# basic_server.py - Basic Authentication
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

try:
    from .server_common import USERS, constant_time_eq
except ImportError:
    from server_common import USERS, constant_time_eq

basic_scheme = HTTPBasic()
router = APIRouter(tags=["basic-auth"])


def auth_basic(creds: HTTPBasicCredentials = Depends(basic_scheme)) -> str:
    u = USERS.get(creds.username)
    if not u or not constant_time_eq(u["password"], creds.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid basic credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return creds.username


@router.get("/protected/basic")
def protected_basic(username: str = Depends(auth_basic)):
    return {"ok": True, "method": "basic", "user": username}


app = FastAPI(title="Auth Playground - Basic")
app.include_router(router)
