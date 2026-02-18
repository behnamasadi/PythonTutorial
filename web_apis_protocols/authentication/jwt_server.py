# jwt_server.py - JWT authentication
from typing import Dict, Any
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException

try:
    from .server_common import USERS, constant_time_eq, create_jwt_for, verify_jwt, JWT_TTL_SECONDS
except ImportError:
    from server_common import USERS, constant_time_eq, create_jwt_for, verify_jwt, JWT_TTL_SECONDS

router = APIRouter(tags=["jwt-auth"])


@router.post("/auth/jwt/login")
async def jwt_login(request: Request):
    body = await request.json()
    username = body.get("username", "")
    password = body.get("password", "")

    u = USERS.get(username)
    if not u or not constant_time_eq(u["password"], password):
        raise HTTPException(status_code=401, detail="Invalid username/password")

    token = create_jwt_for(username)
    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_TTL_SECONDS}


def auth_jwt(request: Request) -> Dict[str, Any]:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing JWT")
    token = auth.removeprefix("Bearer ").strip()
    return verify_jwt(token)


@router.get("/protected/jwt")
def protected_jwt(claims: Dict[str, Any] = Depends(auth_jwt)):
    return {"ok": True, "method": "jwt", "sub": claims["sub"], "email": claims["email"], "name": claims["name"]}


app = FastAPI(title="Auth Playground - JWT")
app.include_router(router)
