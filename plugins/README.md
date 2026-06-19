# REL Plugins

Directory layout:

- `plugins/installed/`: locally installed plugins
- `plugins/marketplace/`: curated plugin templates and marketplace metadata

Each plugin folder must include:

1. `manifest.json`
2. Entrypoint Python file (default: `main.py`) with `run(payload, context=None)`

Example manifest:

```json
{
  "name": "github_integration",
  "version": "1.0.0",
  "description": "Sync lightweight GitHub project data",
  "entrypoint": "main.py",
  "dependencies": [],
  "enabled": true,
  "sandbox_timeout_seconds": 15
}
```
