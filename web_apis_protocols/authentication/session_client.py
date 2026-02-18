# session_client.py - Session cookie authentication client
import httpx

try:
    from .client_common import BASE
except ImportError:
    from client_common import BASE


def run_session_cookie():
    login_url = f"{BASE}/auth/session/login"
    protected_url = f"{BASE}/protected/session"
    login_body = {"username": "behnam", "password": "secret"}

    print("--- SESSION CLIENT ---")
    print("BASE:", BASE)
    print()

    with httpx.Client() as c:
        # Login request
        print("--- LOGIN REQUEST ---")
        print("URL:", login_url)
        print("Method: POST")
        print("Body:", login_body)
        r1 = c.post(login_url, json=login_body)
        print()
        print("--- LOGIN RESPONSE ---")
        print("Status:", r1.status_code)
        print("Headers:", dict(r1.headers))
        print("Cookies:", dict(r1.cookies))
        print("Body:", r1.json())
        print()

        # Protected request (uses session cookie)
        print("--- PROTECTED REQUEST ---")
        print("URL:", protected_url)
        print("Method: GET")
        print("Cookies sent:", dict(c.cookies))
        r2 = c.get(protected_url)
        print()
        print("--- PROTECTED RESPONSE ---")
        print("Status:", r2.status_code)
        print("Headers:", dict(r2.headers))
        print("Body:", r2.json())


if __name__ == "__main__":
    run_session_cookie()
