# REL MCP Server

**Repository:** https://github.com/MrWizard94-Compile/REL

REL (Radiant Ether Loom) is an MCP server with cognitive helpers, persistent state, semantic memory, and neural concept-learning.

## JanusPrime Layering

REL is the **cognition layer**; [JanusPrime](https://github.com/MrWizard94-Compile/JanusPrime) is the **execution layer**. REL owns session continuity, project state, and neural concept learning (`get_state_summary`, `log_session`, `load_context`). JanusPrime owns validation-gated code changes (`janus loop run`, patch kernel, assets). REL bridge tools (PowerShell, filesystem) are **orchestrator-only** — executors must not mutate code through REL.

See [`integrations/janusprime.md`](integrations/janusprime.md) for the REST bridge contract and configuration.

## Key Improvements Included

- Complete Pydantic request validation integrated into runtime tool dispatch.
- OAuth2-style bearer token enforcement (env-driven, optional).
- Structured JSON logging (`REL_LOG_FORMAT=json`) with per-tool monitoring counters.
- Extended integration tests for real `call_tool` execution paths.
- CI pipeline for lint, type-checking, tests, and Docker build.
- Pre-commit hooks for local quality enforcement.

## Repository Layout

- Active runtime code: `mcp_server.py`, `brain_typed.py`, `neural_web_typed.py`, `validation_models.py`
- HTTP API layer: `rest_api.py`
- Analytics/plugin support: `analytics_engine.py`, `plugin_system.py`, `plugins/`
- Web dashboard: `web-dashboard/`
- Test suite: `tests/`
- Ops and docs: `docs/`, `.github/workflows/`
- Archived historical/legacy material: `archive/`

## Quick Start

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e .[dev]
pytest
```

## Authentication

Authentication is optional and controlled by environment variables.

- `REL_AUTH_REQUIRED=true` enables auth checks.
- `REL_OAUTH2_BEARER_TOKEN=<token>` sets the required bearer token.

When enabled, pass one of these fields in tool arguments:

- `auth_token`
- `_auth_token`
- `access_token`
- `bearer_token`

Example argument payload:

```json
{
  "auth_token": "your-token",
  "query": "status"
}
```

## REST API Layer

Start FastAPI server:

```bash
python rest_api.py
```

Key endpoints:

- `POST /api/v1/auth/token` (OAuth2 password flow)
- `GET /api/v1/tools`
- `POST /api/v1/tools/<tool_name>` (all 45 tools exposed)
- `GET /api/v1/analytics/advanced`
- `GET /api/v1/dashboard/overview`
- `GET /docs` (OpenAPI/Swagger)

See `docs/REST_API.md` for details.
For full operator and end-user usage, see `docs/USER_MANUAL.md`.

## Web Dashboard

```bash
cd web-dashboard
npm install
npm run dev
```

The dashboard uses the REST API and realtime websocket notifications from `rest_api.py`.

## Logging and Monitoring

- Structured JSON logs are enabled by default.
- Configure level with `REL_LOG_LEVEL`.
- Monitoring counters are exposed through `get_analytics` under the `monitoring` field.

## Quality Gates

- Lint: `ruff check .`
- Format check: `black --check .`
- Type-check: `mypy brain_typed.py neural_web_typed.py validation_models.py`
- Tests: `pytest`
- Coverage target: `>= 80%` for configured core modules

## Docker

Build and run:

```bash
docker compose up --build
```

Set required secrets before running compose:

- `REL_ADMIN_PASSWORD`
- `REL_OAUTH2_SECRET`

`docker-compose.yml` enforces these values for production-safe startup.

## CI

GitHub Actions workflow is defined in `.github/workflows/ci.yml` and runs:

1. Ruff
2. Black
3. Mypy
4. Pytest + coverage
5. Docker build

