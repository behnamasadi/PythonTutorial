## 1. What “authentication” means in HTTP

**Authentication** answers one question:

> ❓ *Who is making this HTTP request?*

HTTP itself is **stateless**:

* Each request is independent
* The server does **not remember** previous requests unless **authentication data** is sent again

So authentication works by **sending proof of identity with each request**.

---

## 2. Basic HTTP request anatomy

```text
GET /api/profile HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOi...
Cookie: session_id=abc123
```

Authentication data is usually sent via:

* **Headers**
* **Cookies**
* Sometimes **query parameters** (not recommended)

---

## 3. The core authentication flow (generic)

### Step 1 — Client identifies itself

Client sends credentials (password, token, key, etc.)

### Step 2 — Server verifies

Server checks credentials against:

* Database
* Token signature
* External identity provider

### Step 3 — Server grants identity

Server now knows **who the client is**

### Step 4 — Client proves identity on future requests

Client sends a **token**, **cookie**, or **key** with every request

---

## 4. Authentication vs Authorization (important)

| Term           | Meaning                     |
| -------------- | --------------------------- |
| Authentication | Who are you?                |
| Authorization  | What are you allowed to do? |

Example:

* Authenticated as `behnam`
* Authorized to read `/profile`
* Not authorized to delete `/users`

### Where IAM (Identity and Access Management) fits in

**IAM** is the broader framework that combines both identity and access control:

| IAM pillar | What it covers | Examples |
| ---------- | -------------- | -------- |
| **Identity** | Establishing who you are | Login, MFA, identity providers (IdP), user provisioning |
| **Access Management** | What you are allowed to do | Roles, permissions, policies, resource-level access |

Authentication (section 5) is the **identity** piece: Basic, Session, Bearer, JWT, API Keys, OAuth2/OIDC all answer "who are you?". Authorization is the **access** piece: once the server knows who you are, it checks whether you may perform the requested action (e.g. read vs delete).

Real IAM systems (AWS IAM, Azure AD, Okta, Keycloak) typically:

* Provide **identity**: user store, SSO, MFA, federated login
* Provide **access control**: roles, groups, policies, RBAC/ABAC
* Emit **tokens** (JWT, OAuth2) that encode identity and often scopes/permissions
* Integrate with applications via OAuth2/OIDC, SAML, or API keys

This document focuses on **authentication** (identity verification). A full IAM setup adds authorization layers (e.g. role checks, attribute-based policies) on top of the authenticated identity.

---

## 5. Common HTTP authentication methods

---

## 5.1 Basic Authentication (simple but weak)

### How it works

```text
Authorization: Basic base64(username:password)
```

Example:

```text
Authorization: Basic YmVobmFtOnNlY3JldA==
```

### Properties

✅ Easy to implement
❌ Password sent on every request
❌ Must use HTTPS
❌ Not suitable for modern APIs

Used mainly for:

* Internal tools
* Testing
* Very simple setups

### Code example

**Server** (`basic_server.py`):

```python
def auth_basic(creds: HTTPBasicCredentials = Depends(basic_scheme)) -> str:
    u = USERS.get(creds.username)
    if not u or not constant_time_eq(u["password"], creds.password):
        raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Basic"})
    return creds.username

@router.get("/protected/basic")
def protected_basic(username: str = Depends(auth_basic)):
    return {"ok": True, "method": "basic", "user": username}
```

**Client** (`basic_client.py`):

```python
auth_header = f"Basic {b64_basic('behnam', 'secret')}"
r = httpx.get(f"{BASE}/protected/basic", headers={"Authorization": auth_header})
```

### How `/protected/basic` maps from client to server

1. **Client builds the URL**: `BASE` (e.g. `http://127.0.0.1:8000`) + `/protected/basic` yields `GET http://127.0.0.1:8000/protected/basic`.

2. **HTTP request**: The client sends this URL plus the `Authorization: Basic ...` header. The path portion is `/protected/basic`.

3. **Server route registration**: In `basic_server.py`, `@router.get("/protected/basic")` registers that path on the FastAPI router. With `app.include_router(router)` (no prefix), the full route is `/protected/basic`.

4. **Path matching**: Uvicorn receives the request and passes it to FastAPI. FastAPI matches the path `/protected/basic` to the `protected_basic` endpoint.

5. **Dependency chain**: Before `protected_basic` runs, FastAPI executes `Depends(auth_basic)`. `auth_basic` uses `HTTPBasic()`, which reads the `Authorization` header, decodes the Base64 credentials, validates them against `USERS`, and returns the username (or raises 401). The result is passed into `protected_basic` as `username`.

6. **Response**: `protected_basic` returns `{"ok": True, "method": "basic", "user": username}`, which FastAPI serializes as JSON and sends back to the client.

---

## 5.2 Session-based authentication (cookies)

### Typical flow

1. User logs in with username + password
2. Server creates a **session**
3. Server sends back a **cookie** via `Set-Cookie` header
4. Browser/client sends cookie automatically on future requests

```text
Set-Cookie: session_id=abc123; HttpOnly; Secure
```

Later requests:

```text
Cookie: session_id=abc123
```

### Cookie creation and storage

**Server creates the cookie** after successful login using `response.set_cookie()` with the session ID. Typical options: `httponly=True`, `samesite="lax"`, `max_age` (e.g. 1 hour).

**Where is it stored?**

| Location | Storage | Notes |
| -------- | ------- | ----- |
| **Client** (cookie) | Browser stores it | With `max_age`, it is a persistent cookie; browsers typically store it on disk so it survives restarts until expiry |
| **Server** (session data) | In-memory dict (`SESSIONS`) | Not on disk; server restart loses all sessions |

### Cookie must be sent with every request

The client must send the session cookie with **every authenticated request**. The good news: this is automatic. Browsers and `httpx.Client()` persist cookies and send them on subsequent requests to the same domain. You do not add the cookie manually.

### Properties

✅ Browser-friendly
✅ Server can revoke sessions
❌ Server must store session state
❌ Harder to scale horizontally

Used by:

* Traditional websites
* Server-rendered apps

### Code example

**Server** (`session_server.py`):

```python
@router.post("/auth/session/login")
async def session_login(request: Request, response: Response):
    # ... validate credentials ...
    sid = secrets.token_urlsafe(24)
    SESSIONS[sid] = username
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=sid,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60
    )
    return {"ok": True, "method": "session", "message": "logged_in"}

@router.get("/protected/session")
def protected_session(username: str = Depends(auth_session)):
    return {"ok": True, "method": "session", "user": username}
```

**Client** (`session_client.py`):

```python
with httpx.Client() as c:
    c.post(f"{BASE}/auth/session/login", json={"username": "behnam", "password": "secret"})
    r = c.get(f"{BASE}/protected/session")  # cookie sent automatically
```

---

## 5.3 Token-based authentication (Bearer tokens)

### How it works

1. Client logs in
2. Server returns a **token**
3. Client stores token
4. Client sends token in header

```text
Authorization: Bearer <token>
```

### Properties

✅ Stateless server
✅ Easy to scale
✅ Works well for APIs
❌ Token must be protected on client

Used by:

* REST APIs
* Mobile apps
* SPAs
* Microservices

### Code example

**Server** (`bearer_server.py`):

```python
@router.post("/auth/token/login")
async def token_login(request: Request):
    # ... validate credentials ...
    token = secrets.token_urlsafe(32)
    ACCESS_TOKENS[token] = username
    return {"access_token": token, "token_type": "bearer", "expires_in": 3600}

@router.get("/protected/bearer")
def protected_bearer(username: str = Depends(auth_bearer)):
    return {"ok": True, "method": "bearer-opaque", "user": username}
```

**Client** (`bearer_client.py`):

```python
r1 = httpx.post(f"{BASE}/auth/token/login", json={"username": "behnam", "password": "secret"})
token = r1.json()["access_token"]
r2 = httpx.get(f"{BASE}/protected/bearer", headers={"Authorization": f"Bearer {token}"})
```

---

## 5.4 JWT (JSON Web Tokens)

JWT is a **specific type of token**.

### Flow

1. **Login**: Client sends username + password
2. **Server creates token**: Server validates credentials, signs a JWT (payload with `sub`, `exp`, etc.), returns `access_token`
3. **Client stores token**: Client saves it (memory, secure storage)
4. **Every request**: Client sends the token in the header for every GET, POST, etc.

```text
Authorization: Bearer <jwt_access_token>
```

### Tokens generated

| Context        | Tokens returned                    |
| -------------- | ----------------------------------- |
| **Simple JWT** | `access_token` only                 |
| **OAuth2/OIDC** | `access_token`, `refresh_token`, `id_token` |

* `access_token`: Used to access protected resources; sent with every API request
* `refresh_token`: Used to obtain a new `access_token` when it expires; not sent on every request
* `id_token`: Identity claims (user info); often used in OIDC for login confirmation

### If someone steals the token

Whoever possesses the token is treated as that user. The server cannot tell the difference between the real client and an attacker.

**Consequences**:
- Attacker can call APIs as the victim
- Attacker can read/modify data the victim can access
- Until the token expires, the victim is effectively compromised

**Mitigations**:
- Use HTTPS so tokens are not sniffed in transit
- Short expiry (e.g. 15 min for `access_token`) limits damage window
- Store tokens securely on client (avoid localStorage for sensitive apps)
- Use `refresh_token` to rotate access tokens without re-login
- Revocation: JWT cannot be revoked easily; use blocklist or very short TTL

### Structure

```text
header.payload.signature
```

### Payload data (what we put in the token)

In `server_common.py`, `create_jwt_for()` builds the payload from the user record:

| Claim | Meaning | Example (user "behnam") |
| ----- | ------- | ----------------------- |
| `iss` | Issuer | `"http://localhost:8000"` |
| `aud` | Audience | `"auth-playground-client"` |
| `sub` | Subject (user ID) | `"user_123"` |
| `email` | User email | `"behnam@example.com"` |
| `name` | Display name | `"Behnam Asadi"` |
| `role` | Role | `"user"` |
| `iat` | Issued at (Unix time) | Current timestamp |
| `exp` | Expires at | `iat` + 900 sec (15 min) |

**Header** (from PyJWT): `{"alg": "HS256", "typ": "JWT"}`

**Secret** (server_common.py): `JWT_SECRET = "dev_only_change_me"` (used for signing)

The payload is base64-encoded, not encrypted; anyone with the token can decode and read it. Only the signature proves the token was signed by the server.

### Decode / verify on jwt.io

You can use [jwt.io](https://www.jwt.io/) to inspect tokens from this project.

**Example token** (paste into the Decoder):

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAiLCJhdWQiOiJhdXRoLXBsYXlncm91bmQtY2xpZW50Iiwic3ViIjoidXNlcl8xMjMiLCJlbWFpbCI6ImJlaG5hbUBleGFtcGxlLmNvbSIsIm5hbWUiOiJCZWhuYW0gQXNhZGkiLCJyb2xlIjoidXNlciIsImlhdCI6MTc3MTMzMjA5NSwiZXhwIjoxNzcxMzMyOTk1fQ.6xjXSos25nATvbV_cNPoqzjF4zzf01HjfKdOWwcUttE
```

**Valid secret** (for "Verify Signature"): `dev_only_change_me`

**Decoded payload**:

```json
{
  "iss": "http://localhost:8000",
  "aud": "auth-playground-client",
  "sub": "user_123",
  "email": "behnam@example.com",
  "name": "Behnam Asadi",
  "role": "user",
  "iat": 1771332095,
  "exp": 1771332995
}
```

To get a fresh token: run the auth server and `python jwt_client.py`, then copy the `access_token` from the output.

### Server verification

* Check signature
* Check expiration
* Extract identity

### Properties

✅ No database lookup needed
✅ Self-contained
❌ Cannot be revoked easily
❌ Bigger than opaque tokens

### Code example

**Server** (`jwt_server.py`):

```python
@router.post("/auth/jwt/login")
async def jwt_login(request: Request):
    # ... validate credentials ...
    token = create_jwt_for(username)
    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_TTL_SECONDS}

@router.get("/protected/jwt")
def protected_jwt(claims: Dict[str, Any] = Depends(auth_jwt)):
    return {"ok": True, "method": "jwt", "sub": claims["sub"], "email": claims["email"]}
```

**Client** (`jwt_client.py`):

```python
r1 = httpx.post(f"{BASE}/auth/jwt/login", json={"username": "behnam", "password": "secret"})
token = r1.json()["access_token"]
r2 = httpx.get(f"{BASE}/protected/jwt", headers={"Authorization": f"Bearer {token}"})
```

### Token (opaque) vs JWT: comparison

| Aspect | Bearer (opaque token) | JWT |
| ------ | --------------------- | --- |
| **What is sent** | Random string (e.g. `secrets.token_urlsafe`) | Signed JSON payload (header.payload.signature) |
| **Server storage** | Server stores `token -> user` mapping | No storage; claims are in the token |
| **Verification** | Lookup in `ACCESS_TOKENS` dict | Verify signature, check `exp`, read payload |
| **Revocation** | Delete from server store | Hard; must use blocklist or short expiry |
| **Size** | Small (32+ chars) | Larger (base64-encoded JSON) |
| **Claims** | None; server derives identity from lookup | `sub`, `exp`, `role`, etc. embedded |
| **Stateless** | No (server must remember tokens) | Yes (no DB lookup per request) |
| **Best for** | Few tokens, need revocation | Many tokens, distributed systems |

Both use the same HTTP header: `Authorization: Bearer <token>`. The difference is the token format and how the server validates it.

---

## 5.5 API Keys

### How it works

```text
Authorization: Api-Key abcdef123456
```

or

```text
X-API-Key: abcdef123456
```

### Properties

✅ Very simple
❌ No user identity
❌ Usually no expiration
❌ Easy to leak

Used for:

* Public APIs
* Rate limiting
* Service identification

### If someone finds the API key

Whoever has the key can call your API as if they were the legitimate client. The server cannot tell the difference.

**Consequences**:
- Use your quota, incur costs, or trigger rate limits tied to your key
- Access or modify data the key is authorized for
- Abuse continues until you revoke the key (API keys usually have no expiry)

**Mitigations**:
- Revoke and rotate the key immediately
- Use separate keys per app/service (limit blast radius)
- Store keys in environment variables or a secrets manager; never hardcode
- Use HTTPS so keys are not sniffed in transit
- Monitor usage for unusual patterns
- Restrict keys by IP or referrer if the provider supports it

### Code example

**Server** (`api_key_server.py`):

```python
def auth_api_key(request: Request) -> str:
    api_key = request.headers.get("X-API-Key", "")
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    return API_KEYS[api_key]

@router.get("/protected/api-key")
def protected_api_key(username: str = Depends(auth_api_key)):
    return {"ok": True, "method": "api-key", "user": username}
```

**Client** (`api_key_client.py`):

```python
r = httpx.get(f"{BASE}/protected/api-key", headers={"X-API-Key": "api_key_demo_123"})
```

---

## 5.6 OAuth2 / OIDC OpenID Connect (Authorization Code + Proof Key for Code Exchange PKCE)

OAuth2/OIDC uses an authorization code flow with PKCE for public clients.

### Typical flow

1. Client redirects user to `/oidc/authorize` with `client_id`, `redirect_uri`, `state`, `code_challenge`
2. User logs in; server returns redirect with `code` and `state`
3. Client exchanges `code` + `code_verifier` for tokens at `/oidc/token`
4. Client uses `access_token` for protected resources

### Third-party permissions (scopes)

In production OAuth2/OIDC, **scopes** control what each third-party app can access. The user sees a consent screen: "App X wants to: read your email, access your profile" and can grant or deny each scope. The token only includes granted scopes; the resource server checks them before allowing access.

| Scope | What the third party can access |
| ----- | -------------------------------- |
| `openid` | Basic identity (subject ID) |
| `profile` | Name, picture, etc. |
| `email` | Email address |
| `read` | Read-only access to resources |
| `write` | Create/update data |

**This demo** (`oidc_server.py`) does not implement scopes. Every client gets the same full access; there is no `scope` parameter and no granular permissions. It is a simplified flow for learning Authorization Code + PKCE.

### Code example

**Server** (`oidc_server.py`):

```python
@router.get("/oidc/authorize")
def oidc_authorize(client_id: str, redirect_uri: str, state: str, code_challenge: str, login_hint: str = "behnam"):
    require_user(login_hint)
    code = secrets.token_urlsafe(24)
    OAUTH_CODES[code] = {"username": login_hint, "code_challenge": code_challenge, ...}
    return {"redirect_to": f"{redirect_uri}?code={code}&state={signed_state}"}

@router.post("/oidc/token")
async def oidc_token(request: Request):
    # Verify code, PKCE, issue access_token + id_token + refresh_token
    return {"access_token": ..., "id_token": ..., "refresh_token": ...}
```

**Client** (`oidc_client.py`):

```python
code_verifier = secrets.token_urlsafe(32)
code_challenge = pkce_challenge(code_verifier)
r1 = httpx.get(f"{BASE}/oidc/authorize", params={"client_id": ..., "code_challenge": code_challenge, ...})
# Parse code from redirect, then:
r2 = httpx.post(f"{BASE}/oidc/token", json={"code": code, "code_verifier": code_verifier, ...})
access_token = r2.json()["access_token"]
r3 = httpx.get(f"{BASE}/protected/oidc-resource", headers={"Authorization": f"Bearer {access_token}"})
```

---

## 6. How authentication fits into HTTP status codes

| Code             | Meaning                           |
| ---------------- | --------------------------------- |
| 401 Unauthorized | Missing or invalid authentication |
| 403 Forbidden    | Authenticated, but not allowed    |
| 200 OK           | Authenticated and authorized      |

---

## 7. Authentication in browsers vs APIs

### Browser apps

* Cookies
* Sessions
* CSRF protection required

### API clients

* Bearer tokens
* API keys
* HMAC signatures

---

## 8. Why HTTPS is mandatory

Without HTTPS:

* Headers are visible
* Cookies can be stolen
* Tokens can be replayed

With HTTPS:

* Authentication data is encrypted in transit

**Rule**:
❌ Never send credentials over plain HTTP

---

## 9. Typical real-world example

### Login request

```text
POST /login
{
  "username": "behnam",
  "password": "secret"
}
```

### Server response

```json
{
  "access_token": "...",
  "expires_in": 3600
}
```

### Authenticated request

```text
GET /api/data
Authorization: Bearer <access_token>
```

---

## 10. Summary

* HTTP is stateless → authentication data must be sent each request
* Authentication proves **who you are**; authorization controls **what you can do**
* **IAM** (Identity and Access Management) combines both: identity (login, IdP) + access (roles, permissions)
* Most modern APIs use **Bearer tokens**
* Browsers often use **cookies + sessions**
* HTTPS is non-negotiable

---

