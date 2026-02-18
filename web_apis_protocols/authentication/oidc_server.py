# oidc_server.py - OAuth2/OIDC-like Authorization Code + PKCE
import secrets
from fastapi import APIRouter, FastAPI, Request, Depends, HTTPException
from itsdangerous import URLSafeSerializer

try:
    from .server_common import (
        require_user,
        now,
        pkce_challenge,
        OAUTH_CODES,
        ACCESS_TOKENS,
        OAUTH_REFRESH,
        create_jwt_for,
    )
    from .bearer_server import auth_bearer
except ImportError:
    from server_common import (
        require_user,
        now,
        pkce_challenge,
        OAUTH_CODES,
        ACCESS_TOKENS,
        OAUTH_REFRESH,
        create_jwt_for,
    )
    from bearer_server import auth_bearer

state_signer = URLSafeSerializer("dev_state_signing_key")
router = APIRouter(tags=["oidc-auth"])


@router.get("/oidc/authorize")
def oidc_authorize(
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str,
    login_hint: str = "behnam",
):
    require_user(login_hint)

    signed_state = state_signer.dumps(
        {"state": state, "client_id": client_id, "redirect_uri": redirect_uri})

    code = secrets.token_urlsafe(24)
    OAUTH_CODES[code] = {
        "username": login_hint,
        "code_challenge": code_challenge,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "exp": now() + 120,
        "signed_state": signed_state,
    }

    redirect_back = f"{redirect_uri}?code={code}&state={signed_state}"
    return {"redirect_to": redirect_back}


@router.post("/oidc/token")
async def oidc_token(request: Request):
    body = await request.json()
    grant_type = body.get("grant_type")
    if grant_type != "authorization_code":
        raise HTTPException(
            status_code=400, detail="Only authorization_code supported in demo")

    code = body.get("code", "")
    redirect_uri = body.get("redirect_uri", "")
    client_id = body.get("client_id", "")
    code_verifier = body.get("code_verifier", "")

    rec = OAUTH_CODES.get(code)
    if not rec:
        raise HTTPException(status_code=400, detail="Invalid code")
    if rec["exp"] < now():
        raise HTTPException(status_code=400, detail="Expired code")
    if rec["client_id"] != client_id or rec["redirect_uri"] != redirect_uri:
        raise HTTPException(
            status_code=400, detail="client_id/redirect_uri mismatch")

    if pkce_challenge(code_verifier) != rec["code_challenge"]:
        raise HTTPException(
            status_code=400, detail="Bad code_verifier (PKCE failed)")

    username = rec["username"]

    access_token = secrets.token_urlsafe(32)
    ACCESS_TOKENS[access_token] = username

    id_token = create_jwt_for(username)

    refresh_token = secrets.token_urlsafe(32)
    OAUTH_REFRESH[refresh_token] = username

    del OAUTH_CODES[code]

    return {
        "token_type": "Bearer",
        "access_token": access_token,
        "id_token": id_token,
        "refresh_token": refresh_token,
        "expires_in": 3600,
    }


@router.get("/protected/oidc-resource")
def protected_oidc_resource(username: str = Depends(auth_bearer)):
    return {"ok": True, "method": "oidc-like", "user": username}


app = FastAPI(title="Auth Playground - OIDC")
app.include_router(router)
