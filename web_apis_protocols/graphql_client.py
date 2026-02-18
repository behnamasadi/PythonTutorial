import requests

URL = "http://localhost:8000/graphql"

INTROSPECTION = """
query {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types {
      name
      kind
    }
  }
}
"""


def query(q: str, variables: dict = None) -> dict:
    r = requests.post(URL, json={"query": q, "variables": variables or {}})
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]


def wait():
    input("Press Enter to continue...")


if __name__ == "__main__":
    print("1. Fetching schema and available operations...")
    schema = query(INTROSPECTION)
    print("   Query root:", schema["__schema"]["queryType"]["name"])
    print("   Mutation root:", schema["__schema"]["mutationType"]["name"])
    print("   Subscription root:", schema["__schema"]["subscriptionType"]["name"])
    print("   Types:", [t["name"] for t in schema["__schema"]["types"] if not t["name"].startswith("__")])
    wait()

    print("\n2. Adding user Eve...")
    result = query('mutation { addUser(name: "Eve", age: 28) { id name age } }')
    print("   Result:", result["addUser"])
    wait()

    print("\n3. Deleting user Eve...")
    user_id = result["addUser"]["id"]
    deleted = query(f'mutation {{ deleteUser(id: "{user_id}") }}')
    print("   Deleted id:", deleted["deleteUser"])
    wait()

    print("\n4. Subscribing to userAdded...")
    sub = query("subscription { userAdded { id name age } }")
    print("   Subscription result:", sub)
