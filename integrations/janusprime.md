# JanusPrime Integration Contract

REL (Radiant Ether Loom) layers **above** [JanusPrime](https://github.com/MrWizard94-Compile/JanusPrime) as the orchestrator cognition plane. JanusPrime owns validation-gated execution; REL owns session continuity, project state, and neural concept learning.

## Layering

| Layer | System | Role |
|-------|--------|------|
| Cognition | REL | `get_state_summary`, `log_session`, `load_context`, decisions, neural web |
| Execution | JanusPrime | `janus loop run`, patch validation, assets, Smart-Library heal |
| Engineering memory | Smart-Library | Doctrine, repair patterns, accepted task seeds |

**Invariant:** REL `PowerShell` and filesystem bridge tools are **orchestrator-only**. Executors (Grok) must not use them — all code mutations flow through JanusPrime validation kernel (SOUL §1).

## Evolution: Steward → Smart-Library Sync

On complete `janus loop run` rollups (when `sync_concepts_to_memory: true`):

1. JanusPrime calls REL `get_state_summary`, `load_context`, `get_analytics`
2. Formats steward/neural-web highlights
3. Seeds Smart-Library as category `Project Context`

Manual sync: `janus rel sync -q "your query"`

## `doc:rel-state` Context Ref

Orchestrator tasks (assignee `claude`) may include `doc:rel-state`. JanusPrime injects a live REL state excerpt capped by `token_policy.rel_context_max_chars` (default 800). Never injected into Grok executor briefs.

## Tool inventory

- **88 tools** registered in MCP (`mcp_server.list_tools` / `rest_api.TOOL_NAMES` — discovered from `Tool(name=...)` definitions in `mcp_server.py`).
- **5 bridge tools** callable by non-admin REST principals (see allowlist below). Admin may invoke any registered tool.

## Bridge Tools (REST)

JanusPrime calls these via `POST /api/v1/tools/{tool_name}`:

| Tool | When | Payload |
|------|------|---------|
| `get_state_summary` | `janus rel status` | `{}` |
| `load_context` | Orchestrator context pull | `{ "query": "...", "max_tokens": 800 }` |
| `log_session` | After `janus loop run` | `{ "summary": "...", "achievements": ["..."] }` |
| `neural_learn` | After successful loop rollup | `{ "text": "JanusPrime loop ..." }` |
| `get_analytics` | Steward/neural-web rollup | `{}` |

### REST tool allowlist (H1)

Non-admin principals (`service`, `member`, `manager`, and anonymous when auth is disabled) may invoke **only** the bridge tools above via REST. Dangerous orchestrator-only tools — `PowerShell`, filesystem (`fs_*`), desktop/windows bridge tools (`Screenshot`, `Click`, etc.) — return **403 Forbidden** for those roles.

- **Admin** bypasses the allowlist and may call any registered tool.
- **`GET /api/v1/tools`** lists only allowed bridge tools for non-admin callers.
- Override the allowlist with `REL_REST_BRIDGE_TOOLS` (comma-separated tool names). Default:

  `get_state_summary,load_context,log_session,neural_learn,get_analytics`

### MCP tool policy (H1)

MCP stdio clients (e.g. Claude orchestrator, Grok executor) previously saw all **88** registered tools. Executor-safe mode mirrors the REST invariant: dangerous tools are hidden from `list_tools` and blocked in `call_tool`.

| Env | Default | Effect |
|-----|---------|--------|
| `REL_MCP_EXECUTOR_SAFE` | `true` | Deny dangerous tools via MCP |
| `REL_MCP_EXECUTOR_SAFE` | `false` | Admin/orchestrator bypass — all tools listed and callable |
| `REL_MCP_DENIED_TOOLS` | *(see below)* | Comma-separated denylist override |

When `REL_MCP_EXECUTOR_SAFE=true` (JanusPrime default):

- **`list_tools`** omits denied tools (PowerShell, `fs_*`, Windows desktop bridge tools, `WinFileSystem`, `create_snapshot`, etc.).
- **`call_tool`** returns **403** JSON for denied tools: `{"error": "...", "code": 403}`.
- Bridge tools (`get_state_summary`, `load_context`, `log_session`, `neural_learn`, `get_analytics`) and safe cognition tools remain available.

Default `REL_MCP_DENIED_TOOLS` (30 tools):

`PowerShell,Process,Registry,Screenshot,Click,TypeText,Shortcut,DeskSnapshot,Scroll,Move,PauseSec,WebScrape,AppLaunch,Clipboard,Notification,MultiClick,MultiEdit,WinFileSystem,fs_read_file,fs_write_file,fs_edit_file,fs_list_directory,fs_search_files,fs_directory_tree,fs_move_file,fs_get_file_info,fs_read_multiple,fs_create_directory,fs_allowed_dirs,create_snapshot`

**Orchestrator full access:** set `REL_MCP_EXECUTOR_SAFE=false` in the MCP server environment (e.g. Claude Desktop `mcpServers.REL.env`).

## Authentication

Set one of:

- `JANUS_REL_API_KEY` → `X-API-Key` header (create via `POST /api/v1/api-keys` as admin)
- `JANUS_REL_BEARER_TOKEN` → `Authorization: Bearer` (from `POST /api/v1/auth/token`)

REL REST defaults to `REL_API_AUTH_REQUIRED=true`. For local dev, create a service-role API key.

## Runtime

### JanusPrime Docker Compose (recommended)

When running the [JanusPrime stack](https://github.com/MrWizard94-Compile/JanusPrime), REL is the **`cognition`** service alongside `ollama` and `memory` (Smart-Library):

```powershell
# From JanusPrime workspace root (clone REL to REL_BUILD_CONTEXT or use default path)
docker compose up -d
```

- Service name: `cognition` → container `janusprime-cognition`
- REST API: `http://localhost:8080` (matches default `components.cognition.rest_url`)
- Build context: `REL_BUILD_CONTEXT` env (default `C:/REL_Codex_Variant`)
- Data volume: `REL_DATA_PATH` env (default `C:/REL_Codex_Variant/data`)
- Steward Ollama: `OLLAMA_BASE_URL=http://ollama:11434` inside the stack

Point `janus.config.json` at `http://localhost:8080`. For local dev, JanusPrime compose sets `REL_API_AUTH_REQUIRED=false` by default — unauthenticated requests get an anonymous principal with **service** role so bridge tools (`/api/v1/tools/*`) work without an API key.

### Standalone (two terminals)

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