# api_key_client.py - API Key authentication client
import httpx

from .client_common import BASE


def run_api_key():
    r = httpx.get(f"{BASE}/protected/api-key",
                  headers={"X-API-Key": "api_key_demo_123"})
    print("API KEY:", r.status_code, r.json())
