# REL REST API

`rest_api.py` exposes REL over HTTP with FastAPI.

## Highlights

- 45 dedicated tool endpoints at `/api/v1/tools/<tool_name>`
- Generic invoke endpoint at `/api/v1/tools/{tool_name}`
- OpenAPI docs at `/docs` and schema at `/openapi.json`
- OAuth2 bearer token endpoint: `POST /api/v1/auth/token`
- API key lifecycle endpoints:
  - `POST /api/v1/api-keys`
  - `GET /api/v1/api-keys`
  - `DELETE /api/v1/api-keys/{key_id}`
- Rate limiting middleware (including login route; configurable via env vars)
- CORS middleware (configurable via `REL_CORS_ORIGINS`, `REL_CORS_ALLOW_CREDENTIALS`)
- Request/response structured logging

## Start API

```bash
python rest_api.py
```

Or:

```bash
uvicorn rest_api:api_app --host 0.0.0.0 --port 8080
```

## Auth

Bootstrap admin and token settings (set before startup):

- `REL_ADMIN_USERNAME`
- `REL_ADMIN_PASSWORD`
- `REL_OAUTH2_SECRET`
- `REL_API_LOGIN_RATE_LIMIT_PER_MINUTE`

If `REL_ADMIN_PASSWORD` or `REL_OAUTH2_SECRET` are missing, runtime-only random values are generated and startup logs warn about it.

## Collaboration, Plugins, Notifications

- Multi-user and project sharing endpoints under `/api/v1/projects/*`
- Plugin discovery/execution endpoints under `/api/v1/plugins/*`
- Realtime notifications websocket at `/ws/notifications`
  - Preferred auth: `Sec-WebSocket-Protocol: rel-notify, bearer.<token>`
  - Legacy fallback: `?token=<bearer_token>` (deprecated)
