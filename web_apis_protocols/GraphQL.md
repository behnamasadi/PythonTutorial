# GraphQL Basics

## What GraphQL Is

GraphQL is a query language for APIs. Clients request exactly the data they need in a single request, avoiding multiple round-trips typical in REST.

---

## Schema and Types

A **schema** is the contract between the API and clients. It describes what data exists, what fields each type has, and what operations (queries, mutations, subscriptions) clients can perform.

### The `type` Keyword

In GraphQL SDL, `type` declares an object type with named fields:

```graphql
type User {
  id: ID!
  name: String!
  age: Int
}
```

- `!` means non-nullable
- `age` is optional (nullable)

### Root Types

| Type | Purpose |
|------|---------|
| `Query` | Read operations (front door to the API) |
| `Mutation` | Write operations (create, update, delete) |
| `Subscription` | Real-time updates (streaming) |

Example:

```graphql
type Query {
  users: [User!]!
  user(id: ID!): User
}
type Mutation {
  addUser(name: String!, age: Int): User
}
type Subscription {
  userAdded: User
}
```

---

## The `ID` Scalar

`ID` is a built-in scalar for unique identifiers. It is opaque, not for arithmetic, and usually serialized as a string.

| Type | Use |
|------|-----|
| `ID` | Object identity |
| `Int` | Numbers, counters |
| `String` | Text |

GraphQL does not enforce uniqueness; your backend does.

---

## Python Implementation (graphql-core + FastAPI)

This project uses **graphql-core** (no Strawberry) with programmatic schema definition via `GraphQLObjectType` and `GraphQLSchema`.

### Key Components

**GraphQLObjectType** – Defines a type and its fields:

```python
User = GraphQLObjectType("User", {
    "id": GraphQLField(GraphQLNonNull(GraphQLID)),
    "name": GraphQLField(GraphQLNonNull(GraphQLString)),
    "age": GraphQLField(GraphQLInt),
})
```

**Query** – Root type for reads. Fields use `resolve` to return data:

```python
Query = GraphQLObjectType("Query", {
    "users": GraphQLField(GraphQLList(User), resolve=lambda *_: USERS),
})
```

**Mutation** – Root type for writes. Fields take `args` and `resolve`:

```python
Mutation = GraphQLObjectType("Mutation", {
    "addUser": GraphQLField(User, args={
        "name": GraphQLArgument(GraphQLNonNull(GraphQLString)),
        "age": GraphQLArgument(GraphQLInt),
    }, resolve=add_user),
    "deleteUser": GraphQLField(GraphQLNonNull(GraphQLString), args={
        "id": GraphQLArgument(GraphQLNonNull(GraphQLID)),
    }, resolve=delete_user),
})
```

**Subscription** – Root type for streaming. Fields use `subscribe` (not `resolve`); the resolver must be an async generator:

```python
async def user_added(*_):
    yield {"userAdded": USERS[-1]} if USERS else {}

Subscription = GraphQLObjectType("Subscription", {
    "userAdded": GraphQLField(User, subscribe=user_added),
})
```

**GraphQLSchema** – Wires the three root types together:

```python
schema = GraphQLSchema(query=Query, mutation=Mutation, subscription=Subscription)
```

### Execution Flow

- **Query / Mutation**: `graphql(schema, query, variable_values=vars)`
- **Subscription**: `subscribe(schema, document, variable_values=vars)` returns an async iterator; each item is mapped through `execute()` to produce `ExecutionResult`s.

The FastAPI endpoint parses the document, checks `OperationType.SUBSCRIPTION`, and routes to `subscribe()` or `graphql()` accordingly.

---

## Introspection

When you do not know the schema, send an introspection query:

```graphql
query {
  __schema {
    queryType { name }
    mutationType { name }
    subscriptionType { name }
    types { name kind }
  }
}
```

`__schema` and `__type` are reserved meta-fields in the GraphQL spec.

---

## Python Client

The client (`graphql_client.py`) talks to the GraphQL server over HTTP. All operations use the same endpoint: `POST /graphql`.

### Request Format

Every request sends a JSON body with:

| Field | Description |
|-------|-------------|
| `query` | GraphQL document (query, mutation, or subscription string) |
| `variables` | Optional map of variable names to values |

```python
requests.post(URL, json={"query": q, "variables": variables or {}})
```

The server returns `{"data": {...}, "errors": [...]}`. If `errors` is present, the operation failed.

### The `query()` Helper

```python
def query(q: str, variables: dict = None) -> dict:
    r = requests.post(URL, json={"query": q, "variables": variables or {}})
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    return data["data"]
```

It POSTs the operation, checks for HTTP and GraphQL errors, and returns only `data`. The same function works for queries, mutations, and subscriptions because the server uses one endpoint for all.

### Demo Flow

The interactive demo runs four steps with Enter between each:

1. **Introspection** – Fetch `__schema` to discover root types and available types.
2. **Add user** – `mutation { addUser(name: "Eve", age: 28) { id name age } }`
3. **Delete user** – `mutation { deleteUser(id: "...") }` using the id from step 2.
4. **Subscribe** – `subscription { userAdded { id name age } }` returns one event (our server yields the last user).

### Variables

For dynamic values, use variables instead of string interpolation:

```graphql
mutation AddUser($name: String!, $age: Int) {
  addUser(name: $name, age: $age) { id name age }
}
```

```python
query(ADD_USER, variables={"name": "Eve", "age": 28})
```

This avoids injection and keeps the query reusable.
