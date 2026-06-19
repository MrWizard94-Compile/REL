# REL User Manual

This manual explains how to run and use REL (Radiant Ether Loom) as:

- an MCP server (`mcp_server.py`)
- an HTTP API (`rest_api.py`)
- a web dashboard (`web-dashboard/`)

## 1. What REL Provides

REL is a cognitive project/session system with:

- 45 tools for state, projects, sessions, analytics, and learning
- persistent storage under `REL_PATH/data`
- OAuth2 bearer auth and API key auth (REST API)
- plugin discovery/execution
- realtime notifications over WebSocket
- a React dashboard for operations and analytics

## 2. Quick Start

### Local Python Setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
```

### Start REST API

```bash
python rest_api.py
```

Default API URL: `http://localhost:8080`  
Swagger docs: `http://localhost:8080/docs`

### Start Web Dashboard

```bash
cd web-dashboard
npm install
npm run dev
```

Default dashboard URL: `http://localhost:5173`

### Start MCP Server (stdio)

```bash
python mcp_server.py
```

Use this command in your MCP client config as the REL server process.

## 3. Authentication

### REST API auth methods

REL API supports:

- OAuth2 bearer tokens
- API keys (`X-API-Key`)

By default, REST auth is enabled (`REL_API_AUTH_REQUIRED=true`).

### OAuth2 login

Bootstrap admin credentials:

- username: `REL_ADMIN_USERNAME` (defaults to `admin` if unset)
- password: `REL_ADMIN_PASSWORD` (set this explicitly for persistent environments)

If `REL_ADMIN_PASSWORD` is not set, REL generates a runtime-only random password and logs a startup warning.

Request token:

```bash
curl -X POST "http://localhost:8080/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=<REL_ADMIN_USERNAME>&password=<REL_ADMIN_PASSWORD>"
```

Use token:

```bash
curl -X GET "http://localhost:8080/api/v1/auth/me" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### API key usage

Create/list/revoke API keys via:

- `POST /api/v1/api-keys` (admin)
- `GET /api/v1/api-keys` (admin)
- `DELETE /api/v1/api-keys/{key_id}` (admin)

Then call endpoints with:

```http
X-API-Key: rel_xxx...
```

### MCP tool auth

MCP-side tool auth is controlled separately:

- `REL_AUTH_REQUIRED=true`
- `REL_OAUTH2_BEARER_TOKEN=<token>`

When enabled, include one of these fields in tool arguments:

- `auth_token`
- `_auth_token`
- `access_token`
- `bearer_token`

## 4. Configuration Reference

Set environment variables before startup.

- `REL_PATH`: base runtime path (default: repo root)
- `REL_LOG_FORMAT`: `json` or text (default: `json`)
- `REL_LOG_LEVEL`: log level (default: `INFO`)
- `REL_AUTH_REQUIRED`: require MCP tool bearer auth (`true/false`)
- `REL_OAUTH2_BEARER_TOKEN`: MCP bearer token
- `REL_BEARER_TOKEN`: alias for MCP bearer token
- `REL_API_AUTH_REQUIRED`: require API auth (default: `true`)
- `REL_ADMIN_USERNAME`: seeded admin username (default: `admin`)
- `REL_ADMIN_PASSWORD`: admin bootstrap password (set explicitly for persistent environments)
- `REL_OAUTH2_SECRET`: HMAC secret for API token signatures (set explicitly for persistent environments)
- `REL_ACCESS_TOKEN_EXPIRE_MINUTES`: API token lifetime (default: `120`)
- `REL_API_RATE_LIMIT_PER_MINUTE`: limit count (default: `180`)
- `REL_API_LOGIN_RATE_LIMIT_PER_MINUTE`: login limit count (default: `12`)
- `REL_API_RATE_LIMIT_WINDOW_SECONDS`: limit window (default: `60`)
- `REL_CORS_ORIGINS`: comma-separated origins or `*` (default: `*`)
- `REL_CORS_ALLOW_CREDENTIALS`: allow credentialed CORS (`true`/`false`, default: `true`)
- `REL_API_HOST`: API bind host (default: `0.0.0.0`)
- `REL_API_PORT`: API port (default: `8080`)

## 5. Data Files and Persistence

REL stores runtime data under `REL_PATH/data`.

Core files:

- `data/CoreState.json`
- `data/SessionLog.json`
- `data/brain/`
- `data/neural_web/`
- `data/users.json`
- `data/api_keys.json`
- `data/collaboration.json`

Back up `REL_PATH/data` regularly.

## 6. REST API Overview

Core endpoints:

- `GET /health`
- `GET /api/v1/tools`
- `POST /api/v1/tools/{tool_name}`
- `GET /api/v1/dashboard/overview`
- `GET /api/v1/dashboard/projects`
- `GET /api/v1/dashboard/activity`
- `GET /api/v1/dashboard/context-pressure`
- `GET /api/v1/analytics/advanced`
- `GET /api/v1/analytics/recommendations`
- `GET /api/v1/analytics/predictions`
- `GET /api/v1/plugins`
- `POST /api/v1/plugins/reload`
- `POST /api/v1/plugins/{plugin_name}/enable`
- `POST /api/v1/plugins/{plugin_name}/execute`
- `GET /api/v1/notifications/recent`
- `WS /ws/notifications`

Role-restricted endpoints:

- `POST /api/v1/users` (admin)
- `GET /api/v1/users` (admin, manager)
- API key management endpoints (admin)

### Generic tool invocation example

```bash
curl -X POST "http://localhost:8080/api/v1/tools/create_project" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d "{\"arguments\":{\"key\":\"proj_1\",\"name\":\"Project 1\",\"description\":\"Test project\"}}"
```

## 7. Tool Catalog (45 Tools)

Core state:

- `get_state`
- `get_state_summary`
- `update_state`
- `get_stats`
- `validate`
- `get_all_flags`

Project:

- `create_project`
- `get_project`
- `list_projects`
- `update_project`
- `set_active_project`
- `get_active_project`
- `archive_project`
- `get_project_stats`

Session:

- `log_session`
- `get_session_history`
- `get_current_session`
- `end_session`
- `search_sessions`

Progress:

- `log_win`
- `capture_idea`
- `update_focus`
- `log_progress`

Pattern/cognitive:

- `get_insights`
- `get_patterns`
- `analyze_productivity`
- `predict_cold_projects`
- `get_suggested_actions`
- `check_for_conflict`
- `get_story_arc`
- `get_affective_trends`

Context:

- `load_context`
- `get_loading_preview`
- `get_recommendations`
- `search_files`

Advanced:

- `get_analytics`
- `create_snapshot`
- `get_knowledge_graph`
- `sync_obsidian`
- `smart_load`

Brain:

- `semantic_search`

Neural learning:

- `neural_learn`
- `neural_get_related`
- `neural_get_patterns`
- `neural_apply_decay`

## 8. Dashboard Usage

The dashboard supports:

- OAuth2 login/logout
- live project and session overview
- momentum and prediction charts
- quick actions (session check, recommendations, context pressure)
- realtime activity updates via WebSocket

It polls API data every 15 seconds and listens to `/ws/notifications`.

## 9. Plugin System

Plugin roots:

- `plugins/installed/`
- `plugins/marketplace/`

Each plugin requires:

- `manifest.json`
- entrypoint file (`main.py` by default) with `run(payload, context=None)`

Example manifest:

```json
{
  "name": "my_plugin",
  "version": "1.0.0",
  "description": "Example plugin",
  "entrypoint": "main.py",
  "dependencies": [],
  "enabled": true,
  "sandbox_timeout_seconds": 15
}
```

Plugins execute in a separate process with timeout protection.

## 10. Realtime Notifications

Connect using:

```text
ws://localhost:8080/ws/notifications
```

Notes:

- token is required
- preferred auth transport: `Sec-WebSocket-Protocol: rel-notify, bearer.<ACCESS_TOKEN>`
- query-string `?token=...` is supported for compatibility but deprecated
- connection is rejected on invalid/expired token
- API events (tool calls, sharing, comments, plugin actions, key/user operations) are published to subscribers

## 11. Rate Limiting and CORS

HTTP rate limiting applies to `/api/v1/*` except health/docs routes.

Response headers include:

- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `Retry-After` (when limited)

CORS is controlled by `REL_CORS_ORIGINS` and `REL_CORS_ALLOW_CREDENTIALS`.
When origins are `*`, credentialed CORS is automatically disabled.

## 12. Docker Deployment

Run both API and MCP containers:

```bash
docker compose up --build
```

Provided services:

- `rel-api` on port `8080`
- `rel-mcp-server` (stdio process container)

Persisted data is mounted from local `./data`.

## 13. Troubleshooting

401 Unauthorized:

- verify token or API key
- verify `REL_API_AUTH_REQUIRED` setting
- reissue token via `/api/v1/auth/token`

403 Forbidden:

- endpoint requires a stronger role (admin/manager/member policy)

404 Unknown tool:

- call `GET /api/v1/tools` to confirm valid tool names

429 Too Many Requests:

- wait for `Retry-After`
- raise rate limit env vars if appropriate

Plugin execution errors:

- check plugin `manifest.json`
- ensure dependencies exist
- verify entrypoint exports callable `run(payload, context=None)`

Dashboard login fails:

- verify API is running on expected host/port
- verify admin credentials/environment overrides

## 14. Production Checklist

- change default admin credentials
- set strong `REL_OAUTH2_SECRET`
- set `REL_API_AUTH_REQUIRED=true`
- set `REL_API_LOGIN_RATE_LIMIT_PER_MINUTE` for your threat model
- set restrictive `REL_CORS_ORIGINS`
- back up `REL_PATH/data`
- keep `REL_LOG_FORMAT=json` for machine-readable logs
