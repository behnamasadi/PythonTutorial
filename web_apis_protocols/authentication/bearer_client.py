# bearer_client.py - Bearer token (opaque) authentication client
import httpx

try:
    from .client_common import BASE
except ImportError:
    from client_common import BASE


def run_bearer_opaque():
    login_url = f"{BASE}/auth/token/login"
    protected_url = f"{BASE}/protected/bearer"
    login_body = {"username": "behnam", "password": "secret"}

    print("--- BEARER CLIENT ---")
    print("BASE:", BASE)
    print()

    # Login request
    print("--- LOGIN REQUEST ---")
    print("URL:", login_url)
    print("Method: POST")
    print("Body:", login_body)
    r1 = httpx.post(login_url, json=login_body)
    print()
    print("--- LOGIN RESPONSE ---")
    print("Status:", r1.status_code)
    print("Headers:", dict(r1.headers))
    body = r1.json()
    print("Body:", body)
    token = body.get("access_token", "")
    print("Token extracted:", token)
    print()

    if not token:
        print("--- SKIPPED: No token from login")
        print("Start the auth server first (from authentication dir): python run_server.py")
        return

    # Protected request (uses Bearer token)
    auth_header = f"Bearer {token}"
    print("--- PROTECTED REQUEST ---")
    print("URL:", protected_url)
    print("Method: GET")
    print("Authorization:", auth_header)
    r2 = httpx.get(protected_url, headers={"Authorization": auth_header})
    print()
    print("--- PROTECTED RESPONSE ---")
    print("Status:", r2.status_code)
    print("Headers:", dict(r2.headers))
    print("Body:", r2.json())


if __name__ == "__main__":
    run_bearer_opaque()
