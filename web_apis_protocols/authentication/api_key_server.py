# api_key_server.py - API Key authentication
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException

try:
    from .server_common import API_KEYS
except ImportError:
    from server_common import API_KEYS

router = APIRouter(tags=["api-key-auth"])


def auth_api_key(request: Request) -> str:
    api_key = request.headers.get("X-API-Key", "")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")
    username = API_KEYS.get(api_key)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return username


@router.get("/protected/api-key")
def protected_api_key(username: str = Depends(auth_api_key)):
    return {"ok": True, "method": "api-key", "user": username}


app = FastAPI(title="Auth Playground - API Key")
app.include_router(router)
