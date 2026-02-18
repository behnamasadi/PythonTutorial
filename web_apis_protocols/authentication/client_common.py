# client_common.py - Shared utilities for auth clients
import base64
import hashlib

BASE = "http://127.0.0.1:8000"


def b64_basic(user: str, pwd: str) -> str:
    raw = f"{user}:{pwd}".encode()
    return base64.b64encode(raw).decode()


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")
