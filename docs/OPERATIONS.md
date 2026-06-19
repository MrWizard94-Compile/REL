# Operations Guide

## Runtime Environment

Required:

- Python 3.10+
- Writable REL data path (`REL_PATH`)

Recommended:

- `REL_LOG_FORMAT=json`
- `REL_LOG_LEVEL=INFO`

## Data Files

`REL_PATH` contains:

- `data/CoreState.json`
- `data/SessionLog.json`
- `data/brain/`
- `data/neural_web/`

The server creates missing folders automatically.

## Security

Set both variables to enforce bearer auth:

- `REL_AUTH_REQUIRED=true`
- `REL_OAUTH2_BEARER_TOKEN=<secure-random-token>`

Tokens are validated in constant time and stripped before business-logic validation.

For REST API OAuth2:

- `REL_API_AUTH_REQUIRED=true`
- `REL_ADMIN_USERNAME=<admin-user>` (optional; default `admin`)
- `REL_ADMIN_PASSWORD=<admin-password>` (required in persistent environments)
- `REL_OAUTH2_SECRET=<long-random-secret>` (required in persistent environments)
- `REL_API_LOGIN_RATE_LIMIT_PER_MINUTE=<int>` (optional; default `12`)
- `REL_CORS_ORIGINS=<comma-separated-origins>`
- `REL_CORS_ALLOW_CREDENTIALS=true|false`

The API also supports API-key auth using `X-API-Key`.

## REST API Runtime

Start:

```bash
python rest_api.py
```

Default bind:

- Host: `0.0.0.0`
- Port: `8080`

Override with:

- `REL_API_HOST`
- `REL_API_PORT`

Swagger docs are available at `/docs`.

## Monitoring

The server records:

- total tool calls
- tool errors
- per-tool average latency

Retrieve metrics through `get_analytics`.

## Local Validation Checklist

```bash
ruff check .
black --check .
mypy brain_typed.py neural_web_typed.py validation_models.py
pytest
```

## Deployment Notes

- Use a persistent volume for `REL_PATH`.
- Rotate bearer tokens by updating environment configuration.
- Use CI as release gate before deployment.

