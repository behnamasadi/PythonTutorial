"""
REST API client - demonstrates calling the rest_server endpoints.
Start the server first: uvicorn rest_server:app --reload --port 8000
"""

import requests

BASE_URL = "http://localhost:8000"


def main():
    # GET /ping - simple health check
    r = requests.get(f"{BASE_URL}/ping")
    print(f"GET /ping -> {r.status_code} {r.json()}")

    # GET /item/{item_id} - path parameter
    r = requests.get(f"{BASE_URL}/item/42")
    print(f"GET /item/42 -> {r.status_code} {r.json()}")

    # POST /items - JSON body + auth header
    headers = {"Content-Type": "application/json", "X-Token": "secret"}
    payload = {"name": "sensor", "count": 4}
    r = requests.post(f"{BASE_URL}/items", json=payload, headers=headers)
    print(f"POST /items -> {r.status_code} {r.json()}")

    # POST /items without token - expect 401
    r = requests.post(f"{BASE_URL}/items", json=payload)
    print(f"POST /items (no token) -> {r.status_code} {r.json()}")

    # GET /slow - query parameter
    r = requests.get(f"{BASE_URL}/slow", params={"ms": 100})
    print(f"GET /slow?ms=100 -> {r.status_code} {r.json()}")


if __name__ == "__main__":
    main()
