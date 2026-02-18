# basic_client.py - Basic Authentication client
import httpx

try:
    from .client_common import BASE, b64_basic
except ImportError:
    from client_common import BASE, b64_basic


def run_basic():
    auth_header = f"Basic {b64_basic('behnam', 'secret')}"
    r = httpx.get(f"{BASE}/protected/basic",
                  headers={"Authorization": auth_header})
    print("BASE:", BASE)
    print("auth_header:", auth_header)
    print("BASIC:", r.status_code, r.json())


if __name__ == "__main__":
    run_basic()
