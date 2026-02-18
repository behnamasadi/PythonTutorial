# oidc_client.py - OAuth2/OIDC-like Authorization Code + PKCE client
import secrets
import httpx

try:
    from .client_common import BASE, pkce_challenge
except ImportError:
    from client_common import BASE, pkce_challenge


def run_oidc_like_auth_code():
    client_id = "demo-client"
    redirect_uri = "http://localhost/callback"
    state = "xyz123"

    code_verifier = secrets.token_urlsafe(32)
    code_challenge = pkce_challenge(code_verifier)

    r1 = httpx.get(
        f"{BASE}/oidc/authorize",
        params={
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "code_challenge": code_challenge,
            "login_hint": "behnam",
        },
    )
    redirect_to = r1.json()["redirect_to"]
    query = redirect_to.split("?", 1)[1]
    parts = dict(p.split("=", 1) for p in query.split("&"))
    code = parts["code"]
    signed_state = parts["state"]

    r2 = httpx.post(
        f"{BASE}/oidc/token",
        json={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "code_verifier": code_verifier,
            "state": signed_state,
        },
    )
    data = r2.json()
    access_token = data["access_token"]
    id_token = data["id_token"]

    r3 = httpx.get(
        f"{BASE}/protected/oidc-resource",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    print("OIDC authorize:", r1.status_code, r1.json())
    print("OIDC token:", r2.status_code, {
          k: ("<jwt>" if k == "id_token" else v) for k, v in data.items()})
    print("OIDC id_token (JWT) length:", len(id_token))
    print("OIDC resource:", r3.status_code, r3.json())


if __name__ == "__main__":
    run_oidc_like_auth_code()
