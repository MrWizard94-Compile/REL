from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional


def run(payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    request = payload.get("request", {})
    repo = request.get("repo", "owner/repository")
    branch = request.get("branch", "main")
    return {
        "plugin": "github_integration",
        "status": "ok",
        "message": "Template plugin executed successfully.",
        "repo": repo,
        "branch": branch,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "context": {"sandboxed": bool((context or {}).get("sandboxed", False))},
    }
