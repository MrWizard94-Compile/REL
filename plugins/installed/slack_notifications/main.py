from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional


def run(payload: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    request = payload.get("request", {})
    channel = request.get("channel", "#alerts")
    message = request.get("message", "No message provided.")
    return {
        "plugin": "slack_notifications",
        "status": "queued",
        "channel": channel,
        "message_preview": str(message)[:160],
        "simulated": True,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "context": {"sandboxed": bool((context or {}).get("sandboxed", False))},
    }
