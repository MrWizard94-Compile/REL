# JanusPrime Integration Contract

REL (Radiant Ether Loom) layers **above** [JanusPrime](https://github.com/MrWizard94-Compile/JanusPrime) as the orchestrator cognition plane. JanusPrime owns validation-gated execution; REL owns session continuity, project state, and neural concept learning.

## Layering

| Layer | System | Role |
|-------|--------|------|
| Cognition | REL | `get_state_summary`, `log_session`, `load_context`, decisions, neural web |
| Execution | JanusPrime | `janus loop run`, patch validation, assets, Smart-Library heal |
| Engineering memory | Smart-Library | Doctrine, repair patterns, accepted task seeds |

**Invariant:** REL `PowerShell` and filesystem bridge tools are **orchestrator-only**. Executors (Grok) must not use them — all code mutations flow through JanusPrime validation kernel (SOUL §1).

## Bridge Tools (REST)

JanusPrime calls these via `POST /api/v1/tools/{tool_name}`:

| Tool | When | Payload |
|------|------|---------|
| `get_state_summary` | `janus rel status` | `{}` |
| `load_context` | Orchestrator context pull | `{ "query": "...", "max_tokens": 800 }` |
| `log_session` | After `janus loop run` | `{ "summary": "...", "achievements": ["..."] }` |
| `neural_learn` | After successful loop rollup | `{ "text": "JanusPrime loop ..." }` |

## Authentication

Set one of:

- `JANUS_REL_API_KEY` → `X-API-Key` header (create via `POST /api/v1/api-keys` as admin)
- `JANUS_REL_BEARER_TOKEN` → `Authorization: Bearer` (from `POST /api/v1/auth/token`)

REL REST defaults to `REL_API_AUTH_REQUIRED=true`. For local dev, create a service-role API key.

## Runtime

```powershell
# Terminal 1 — REL REST API
cd C:\REL_Codex_Variant
python rest_api.py

# Terminal 2 — JanusPrime
cd C:\Users\Bulkl\OneDrive\Desktop\Janus\Project-Janus
node packages/cli/dist/bin.js janus rel status
node packages/cli/dist/bin.js janus loop run -t <parentId>
```

Shared Ollama (`:11434`): Smart-Library uses `qwen2.5-coder:7b`; REL steward uses `qwen3:4b-instruct`.

## Configuration (JanusPrime)

`janus.config.json`:

```json
"cognition": {
  "root": "C:/REL_Codex_Variant",
  "rest_url": "http://localhost:8080",
  "api_key_env": "JANUS_REL_API_KEY",
  "bearer_token_env": "JANUS_REL_BEARER_TOKEN",
  "log_loop_outcomes": true
}
```

## Repositories

- REL: https://github.com/MrWizard94-Compile/REL
- JanusPrime: https://github.com/MrWizard94-Compile/JanusPrime