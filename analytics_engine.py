"""
Advanced analytics engine for REL.

This module computes higher-level insights from CoreState and SessionLog data.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _session_datetimes(sessions: Iterable[Dict[str, Any]]) -> List[datetime]:
    parsed: List[datetime] = []
    for session in sessions:
        date = _parse_date(str(session.get("date", "")))
        if date is None:
            continue
        time_value = str(session.get("time", "00:00:00"))
        time_parsed = _parse_date(f"{date.strftime('%Y-%m-%d')} {time_value}")
        parsed.append(time_parsed or date)
    return sorted(parsed)


def _momentum_timeline(sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    per_day: Dict[str, int] = defaultdict(int)
    for session in sessions:
        day = str(session.get("date", ""))
        if day:
            per_day[day] += 1
    timeline = [{"date": day, "sessions": count} for day, count in sorted(per_day.items())]
    return timeline[-30:]


def _completion_predictions(
    projects: Dict[str, Dict[str, Any]], sessions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    now = datetime.now()
    predictions: List[Dict[str, Any]] = []
    session_count_by_project: Counter[str] = Counter(
        str(s.get("project", "")) for s in sessions if s.get("project")
    )

    for project_key, project in projects.items():
        completion = float(project.get("completion", 0.0) or 0.0)
        status = str(project.get("status", "active"))
        created = _parse_date(str(project.get("created", "")))
        last_worked = _parse_date(str(project.get("last_worked", "")))
        days_active = max((now - created).days, 1) if created else 1
        touches = max(session_count_by_project.get(project_key, 0), 1)

        if status in {"complete", "archived"} or completion >= 100:
            predictions.append(
                {
                    "project": project_key,
                    "predicted_days_to_complete": 0,
                    "confidence": 0.99,
                    "status": "complete",
                }
            )
            continue

        # Velocity proxy: progress percentage per project touch and time active.
        velocity = max(completion / max(days_active, touches), 0.01)
        remaining = max(100.0 - completion, 0.0)
        predicted_days = int(round(remaining / velocity))
        recency_penalty = 1.0
        if last_worked:
            stale_days = (now - last_worked).days
            if stale_days > 7:
                recency_penalty = 1.25
            if stale_days > 21:
                recency_penalty = 1.5
        predicted_days = int(predicted_days * recency_penalty)
        confidence = min(0.95, max(0.35, touches / 30.0))

        predictions.append(
            {
                "project": project_key,
                "predicted_days_to_complete": max(predicted_days, 1),
                "confidence": round(confidence, 2),
                "status": "in_progress",
            }
        )

    predictions.sort(key=lambda item: item["predicted_days_to_complete"])
    return predictions


def _burnout_assessment(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not sessions:
        return {"risk": "unknown", "score": 0, "signals": []}

    dt = _session_datetimes(sessions)
    signals: List[str] = []
    score = 0

    if len(dt) >= 10:
        span_days = max((dt[-1] - dt[0]).days, 1)
        freq = len(dt) / span_days
        if freq > 2.0:
            score += 35
            signals.append("High sustained session frequency.")

    achievements_per_session = []
    for session in sessions[-14:]:
        achievements = session.get("achievements", [])
        achievements_per_session.append(len(achievements) if isinstance(achievements, list) else 0)
    if achievements_per_session:
        avg_achievements = mean(achievements_per_session)
        if avg_achievements < 1:
            score += 20
            signals.append("Low achievement density in recent sessions.")

    if len(dt) >= 7:
        recent_gaps = [
            (dt[i] - dt[i - 1]).days
            for i in range(max(1, len(dt) - 7), len(dt))
        ]
        if recent_gaps and mean(recent_gaps) <= 0.5:
            score += 25
            signals.append("Minimal recovery time between sessions.")

    summaries = " ".join(str(s.get("summary", "")).lower() for s in sessions[-10:])
    stress_words = ("stuck", "blocked", "exhausted", "overwhelmed", "burnout")
    if any(word in summaries for word in stress_words):
        score += 30
        signals.append("Stress/friction language detected.")

    if score >= 70:
        risk = "high"
    elif score >= 40:
        risk = "moderate"
    else:
        risk = "low"

    return {"risk": risk, "score": min(score, 100), "signals": signals}


def _productivity_patterns(sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    hourly: Counter[int] = Counter()
    weekday: Counter[str] = Counter()
    project: Counter[str] = Counter()

    for session in sessions:
        day_dt = _parse_date(str(session.get("date", "")))
        if day_dt:
            weekday[day_dt.strftime("%A")] += 1
        time_value = str(session.get("time", "00:00:00"))
        time_dt = _parse_date(f"2000-01-01 {time_value}")
        if time_dt:
            hourly[time_dt.hour] += 1
        if session.get("project"):
            project[str(session["project"])] += 1

    top_hour = hourly.most_common(1)[0][0] if hourly else None
    return {
        "sessions_by_hour": dict(sorted(hourly.items())),
        "sessions_by_weekday": dict(weekday),
        "sessions_by_project": dict(project),
        "optimal_work_hour": top_hour,
    }


def _project_correlation(sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Correlate projects by appearing on adjacent days in the session stream.
    pairs: Counter[Tuple[str, str]] = Counter()
    valid = [s for s in sessions if s.get("project")]
    for i in range(1, len(valid)):
        left = str(valid[i - 1]["project"])
        right = str(valid[i]["project"])
        if left == right:
            continue
        key = (left, right) if left < right else (right, left)
        pairs[key] += 1
    output = [
        {"projects": [left, right], "correlation_strength": count}
        for (left, right), count in pairs.most_common(10)
    ]
    return output


def _recommendations(analytics: Dict[str, Any]) -> List[str]:
    recs: List[str] = []
    burnout = analytics.get("burnout", {})
    momentum = analytics.get("momentum", {})
    predictions = analytics.get("completion_predictions", [])

    if burnout.get("risk") == "high":
        recs.append("Schedule a recovery block and reduce context switching for 24-48 hours.")
    elif burnout.get("risk") == "moderate":
        recs.append("Introduce shorter sessions with explicit breaks to avoid escalation.")

    timeline = momentum.get("timeline", [])
    if timeline and len(timeline) >= 5:
        recent_total = sum(day.get("sessions", 0) for day in timeline[-5:])
        if recent_total < 3:
            recs.append("Momentum is slipping; prioritize one critical project for rapid wins.")

    stalled = [p for p in predictions if p.get("predicted_days_to_complete", 0) > 45]
    if stalled:
        recs.append("Break long-horizon projects into milestone-sized tasks to improve velocity.")

    optimal_hour = analytics.get("productivity_patterns", {}).get("optimal_work_hour")
    if optimal_hour is not None:
        recs.append(f"Protect hour {optimal_hour:02d}:00 as your highest-yield focus window.")

    if not recs:
        recs.append("Current system appears stable; continue monitoring weekly trend deltas.")
    return recs


def generate_advanced_analytics(state: Dict[str, Any], session_log: Dict[str, Any]) -> Dict[str, Any]:
    sessions = list(session_log.get("sessions", []))
    projects = dict(state.get("project_states", {}))
    momentum = {"timeline": _momentum_timeline(sessions)}
    analytics = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "momentum": momentum,
        "completion_predictions": _completion_predictions(projects, sessions),
        "burnout": _burnout_assessment(sessions),
        "productivity_patterns": _productivity_patterns(sessions),
        "cross_project_correlation": _project_correlation(sessions),
    }
    analytics["ai_recommendations"] = _recommendations(analytics)
    return analytics
