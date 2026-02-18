from graphql import graphql, subscribe, parse
from graphql.language import OperationType
from graphql.type import (
    GraphQLObjectType,
    GraphQLField,
    GraphQLSchema,
    GraphQLArgument,
    GraphQLString,
    GraphQLInt,
    GraphQLID,
    GraphQLList,
    GraphQLNonNull,
)
from fastapi import FastAPI, Request

USERS = [{"id": "1", "name": "Alice", "age": 30}, {"id": "2", "name": "Bob", "age": 25}, {"id": "3", "name": "Charlie", "age": None}]

User = GraphQLObjectType("User", {
    "id": GraphQLField(GraphQLNonNull(GraphQLID)),
    "name": GraphQLField(GraphQLNonNull(GraphQLString)),
    "age": GraphQLField(GraphQLInt),
})

def add_user(_, info, name, age=None):
    u = {"id": str(len(USERS) + 1), "name": name, "age": age}
    USERS.append(u)
    return u

def delete_user(_, info, id):
    global USERS
    USERS = [u for u in USERS if u["id"] != id]
    return id

async def user_added(*_):
    yield {"userAdded": USERS[-1]} if USERS else {}

Query = GraphQLObjectType("Query", {"users": GraphQLField(GraphQLList(User), resolve=lambda *_: USERS)})
Mutation = GraphQLObjectType("Mutation", {
    "addUser": GraphQLField(User, args={"name": GraphQLArgument(GraphQLNonNull(GraphQLString)), "age": GraphQLArgument(GraphQLInt)}, resolve=add_user),
    "deleteUser": GraphQLField(GraphQLNonNull(GraphQLString), args={"id": GraphQLArgument(GraphQLNonNull(GraphQLID))}, resolve=delete_user),
})
Subscription = GraphQLObjectType("Subscription", {
    "userAdded": GraphQLField(User, subscribe=user_added),
})

schema = GraphQLSchema(query=Query, mutation=Mutation, subscription=Subscription)
app = FastAPI()

@app.post("/graphql")
async def graphql_endpoint(request: Request):
    body = await request.json()
    query, vars = body.get("query", ""), body.get("variables")
    doc = parse(query)
    op = next((n for n in doc.definitions if hasattr(n, "operation") and n.operation == OperationType.SUBSCRIPTION), None)
    if op:
        stream = await subscribe(schema, doc, variable_values=vars)
        first = await stream.__anext__()
        return {"data": first.data, "errors": first.errors}
    result = await graphql(schema, query, variable_values=vars)
    return {"data": result.data, "errors": result.errors}
