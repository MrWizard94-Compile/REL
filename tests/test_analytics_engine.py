from __future__ import annotations

from datetime import datetime, timedelta

import analytics_engine as ae


def _sample_sessions() -> list[dict[str, object]]:
    now = datetime.now()
    sessions: list[dict[str, object]] = []
    for i in range(12):
        dt = now - timedelta(days=i // 2)
        sessions.append(
            {
                "date": dt.strftime("%Y-%m-%d"),
                "time": f"{8 + (i % 5):02d}:15:00",
                "summary": "stuck on auth" if i % 4 == 0 else "normal progress",
                "achievements": [] if i % 3 == 0 else ["a1", "a2"],
                "project": "alpha" if i % 2 == 0 else "beta",
            }
        )
    return sessions


def _sample_projects() -> dict[str, dict[str, object]]:
    now = datetime.now()
    old = (now - timedelta(days=40)).strftime("%Y-%m-%d")
    recent = (now - timedelta(days=2)).strftime("%Y-%m-%d")
    return {
        "alpha": {
            "completion": 80,
            "status": "active",
            "created": old,
            "last_worked": old,
        },
        "beta": {
            "completion": 100,
            "status": "complete",
            "created": old,
            "last_worked": recent,
        },
        "gamma": {
            "completion": 30,
            "status": "archived",
            "created": old,
            "last_worked": old,
        },
    }


def test_parse_date_supports_multiple_formats_and_invalid() -> None:
    assert ae._parse_date("2026-02-20") is not None
    assert ae._parse_date("2026-02-20 10:00:00") is not None
    assert ae._parse_date("2026-02-20T10:00:00") is not None
    assert ae._parse_date("2026-02-20T10:00:00+00:00") is not None
    assert ae._parse_date("") is None
    assert ae._parse_date("not-a-date") is None


def test_safe_int_handles_errors() -> None:
    assert ae._safe_int("9") == 9
    assert ae._safe_int(None, default=7) == 7
    assert ae._safe_int("x", default=5) == 5


def test_session_datetimes_and_momentum_timeline() -> None:
    sessions = _sample_sessions()
    datetimes = ae._session_datetimes(sessions)
    assert datetimes == sorted(datetimes)
    assert len(datetimes) == len(sessions)

    timeline = ae._momentum_timeline(sessions * 3)
    assert len(timeline) <= 30
    assert all("date" in point and "sessions" in point for point in timeline)


def test_completion_predictions_cover_active_complete_and_archived() -> None:
    predictions = ae._completion_predictions(_sample_projects(), _sample_sessions())
    by_project = {item["project"]: item for item in predictions}

    assert by_project["beta"]["status"] == "complete"
    assert by_project["beta"]["predicted_days_to_complete"] == 0
    assert by_project["gamma"]["status"] == "complete"
    assert by_project["alpha"]["status"] == "in_progress"
    assert by_project["alpha"]["predicted_days_to_complete"] >= 1
    assert 0.35 <= by_project["alpha"]["confidence"] <= 0.95


def test_burnout_assessment_paths() -> None:
    unknown = ae._burnout_assessment([])
    assert unknown["risk"] == "unknown"

    moderate_or_high = ae._burnout_assessment(_sample_sessions())
    assert moderate_or_high["risk"] in {"low", "moderate", "high"}
    assert 0 <= moderate_or_high["score"] <= 100
    assert isinstance(moderate_or_high["signals"], list)


def test_productivity_patterns_and_correlation() -> None:
    sessions = _sample_sessions()
    patterns = ae._productivity_patterns(sessions)
    assert "sessions_by_hour" in patterns
    assert "sessions_by_weekday" in patterns
    assert "sessions_by_project" in patterns

    corr = ae._project_correlation(sessions)
    assert isinstance(corr, list)
    if corr:
        assert "projects" in corr[0]
        assert "correlation_strength" in corr[0]


def test_recommendations_default_and_signal_driven() -> None:
    default_recs = ae._recommendations(
        {
            "burnout": {"risk": "low"},
            "momentum": {"timeline": []},
            "completion_predictions": [],
            "productivity_patterns": {},
        }
    )
    assert len(default_recs) == 1
    assert "stable" in default_recs[0].lower()

    signal_recs = ae._recommendations(
        {
            "burnout": {"risk": "high"},
            "momentum": {"timeline": [{"sessions": 0}] * 6},
            "completion_predictions": [{"predicted_days_to_complete": 60}],
            "productivity_patterns": {"optimal_work_hour": 9},
        }
    )
    joined = " ".join(signal_recs).lower()
    assert "recovery" in joined
    assert "momentum" in joined
    assert "milestone" in joined
    assert "09:00" in joined


def test_generate_advanced_analytics_structure() -> None:
    state = {"project_states": _sample_projects()}
    session_log = {"sessions": _sample_sessions()}
    analytics = ae.generate_advanced_analytics(state, session_log)

    assert "generated_at" in analytics
    assert "momentum" in analytics
    assert "completion_predictions" in analytics
    assert "burnout" in analytics
    assert "productivity_patterns" in analytics
    assert "cross_project_correlation" in analytics
    assert "ai_recommendations" in analytics


def test_additional_branch_coverage_for_parse_and_burnout_and_recommendations() -> None:
    # _session_datetimes skip invalid date branch
    dates = ae._session_datetimes([{"date": "invalid", "time": "10:00:00"}, {"date": "2026-02-20"}])
    assert len(dates) == 1

    # _completion_predictions path with missing last_worked
    predictions = ae._completion_predictions({"p": {"completion": 10, "status": "active", "created": "2026-01-01"}}, [])
    assert predictions[0]["status"] == "in_progress"

    # Burnout moderate score path
    moderate_sessions = []
    now = datetime.now()
    for i in range(8):
        dt = now - timedelta(days=i)
        moderate_sessions.append(
            {
                "date": dt.strftime("%Y-%m-%d"),
                "time": "10:00:00",
                "summary": "normal work",
                "achievements": [],
            }
        )
    burnout = ae._burnout_assessment(moderate_sessions)
    assert burnout["risk"] in {"low", "moderate", "high"}

    moderate_recs = ae._recommendations(
        {
            "burnout": {"risk": "moderate"},
            "momentum": {"timeline": [{"sessions": 1}] * 5},
            "completion_predictions": [],
            "productivity_patterns": {},
        }
    )
    assert any("shorter sessions" in rec.lower() for rec in moderate_recs)

    moderate_sessions = []
    now = datetime.now()
    for i in range(6):
        dt = now - timedelta(days=i + 1)
        moderate_sessions.append(
            {
                "date": dt.strftime("%Y-%m-%d"),
                "time": "11:00:00",
                "summary": "stuck in blockers",
                "achievements": [],
            }
        )
    moderate = ae._burnout_assessment(moderate_sessions)
    assert moderate["risk"] == "moderate"
