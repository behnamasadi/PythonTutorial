# server_common.py - Shared data and helpers for auth server
from __future__ import annotations

import base64
import hashlib
import secrets
import time
from typing import Dict, Any

import jwt
from fastapi import HTTPException

# Demo "database" / settings
USERS = {
    "behnam": {
        "password": "secret",  # demo only; never store plaintext in real apps
        "sub": "user_123",
        "email": "behnam@example.com",
        "name": "Behnam Asadi",
        "role": "user",
    }
}

# Session cookie (server-side session store)
SESSION_COOKIE_NAME = "session_id"
SESSIONS: Dict[str, str] = {}  # session_id -> username

# Opaque bearer tokens
ACCESS_TOKENS: Dict[str, str] = {}  # access_token -> username

# API keys
API_KEYS: Dict[str, str] = {
    "api_key_demo_123": "behnam"
}

# JWT settings
JWT_ISSUER = "http://localhost:8000"
JWT_AUDIENCE = "auth-playground-client"
JWT_SECRET = "dev_only_change_me"
JWT_ALG = "HS256"
JWT_TTL_SECONDS = 15 * 60

# Mini OAuth authorization codes (in-memory)
OAUTH_CODES: Dict[str, Dict[str, Any]] = {}
OAUTH_REFRESH: Dict[str, str] = {}  # refresh_token -> username


def now() -> int:
    return int(time.time())


def require_user(username: str) -> Dict[str, Any]:
    u = USERS.get(username)
    if not u:
        raise HTTPException(status_code=401, detail="Unknown user")
    return u


def constant_time_eq(a: str, b: str) -> bool:
    return secrets.compare_digest(a.encode(), b.encode())


def create_jwt_for(username: str) -> str:
    u = require_user(username)
    payload = {
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "sub": u["sub"],
        "email": u["email"],
        "name": u["name"],
        "role": u["role"],
        "iat": now(),
        "exp": now() + JWT_TTL_SECONDS,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def verify_jwt(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALG],
            audience=JWT_AUDIENCE,
            issuer=JWT_ISSUER,
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid JWT")


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")
