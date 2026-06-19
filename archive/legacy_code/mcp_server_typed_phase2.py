#!/usr/bin/env python3
"""
REL MCP Server - Type-Safe Version
Phase 2: Cognitive Modules Complete

Includes:
- Phase 1: Infrastructure (imports, file locking, atomic updates, utilities)
- Phase 2: Cognitive modules (context pressure, contradiction detection, narrative arc, affective trends)
"""

# [Phase 1 code would be inserted here - keeping separate for clarity]
# For now, this file contains ONLY the cognitive modules with full type hints

from datetime import datetime
from typing import Any, Dict, List, Set, Tuple
import re


# ============================================================================
# COGNITIVE MODULE 1: CONTEXT PRESSURE ANALYSIS
# ============================================================================


def get_priority_weight(priority: str) -> float:
    """Get numeric weight for priority level
    
    Maps priority strings to numeric weights for urgency calculation.
    
    Args:
        priority: Priority level string (critical/high/medium/low)
        
    Returns:
        Numeric weight (3.0 for critical, 2.0 for high, 1.0 for medium, 0.5 for low)
        Returns 1.0 as default for unknown priorities
    """
    weights: Dict[str, float] = {
        "critical": 3.0,
        "high": 2.0,
        "medium": 1.0,
        "low": 0.5,
    }
    return weights.get(priority, 1.0)


def get_staleness_multiplier(project: Dict[str, Any]) -> float:
    """Calculate staleness multiplier based on project state
    
    Applies multipliers to urgency based on how stale a project is.
    Projects near completion that haven't been touched are especially urgent.
    
    Args:
        project: Project dictionary with completion, last_worked, and status
        
    Returns:
        Staleness multiplier (0.0 to 2.0)
        - 2.0: DANGER ZONE (>=70% complete, >7 days stale)
        - 1.5: Active but stale (>3 days)
        - 0.3: On hold
        - 0.0: Complete or archived
        - 1.0: Default
    """
    completion: int = project.get("completion", 0)
    days_since: int = calculate_days_since(project.get("last_worked", ""))
    status: str = project.get("status", "active")

    if completion >= 70 and days_since > 7:
        return 2.0  # DANGER ZONE
    if status == "active" and days_since > 3:
        return 1.5
    if status == "on-hold":
        return 0.3
    if status in ["complete", "archived"]:
        return 0.0
    return 1.0


def calculate_urgency(project: Dict[str, Any]) -> float:
    """Calculate urgency score for a project
    
    Combines days since last touch, priority weight, and staleness
    to create a composite urgency score.
    
    Formula: days_since * priority_weight * staleness_multiplier
    
    Args:
        project: Project dictionary
        
    Returns:
        Urgency score rounded to 1 decimal place
    """
    days_since: int = calculate_days_since(project.get("last_worked", ""))
    priority_weight: float = get_priority_weight(project.get("priority", "medium"))
    staleness: float = get_staleness_multiplier(project)
    return round(days_since * priority_weight * staleness, 1)


def classify_urgency(score: float) -> str:
    """Classify urgency score into level
    
    Args:
        score: Numeric urgency score
        
    Returns:
        Urgency level string (CRITICAL/HIGH/MEDIUM/LOW/NONE)
    """
    if score >= 20:
        return "CRITICAL"
    if score >= 10:
        return "HIGH"
    if score >= 5:
        return "MEDIUM"
    if score > 0:
        return "LOW"
    return "NONE"


def analyze_context_pressure(state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze context pressure across all projects
    
    Performs comprehensive urgency analysis on all projects to identify
    which need immediate attention and assess overall cognitive load.
    
    Args:
        state: CoreState dictionary containing project_states
        
    Returns:
        Dictionary containing:
        - project_urgency: Dict mapping project keys to urgency details
        - overall_pressure: Overall pressure level and counts
        - recommended_focus: Top 3 recommended projects to focus on
    """
    projects: Dict[str, Any] = state.get("project_states", {})
    project_urgency: Dict[str, Dict[str, Any]] = {}

    for key, project in projects.items():
        urgency: float = calculate_urgency(project)
        level: str = classify_urgency(urgency)
        days: int = calculate_days_since(project.get("last_worked", ""))

        project_urgency[key] = {
            "urgency_score": urgency,
            "urgency_level": level,
            "days_since_touch": days,
            "priority": project.get("priority", "medium"),
            "completion": project.get("completion", 0),
            "status": project.get("status", "active"),
        }

    sorted_urgency: List[Tuple[str, Dict[str, Any]]] = sorted(
        project_urgency.items(),
        key=lambda x: x[1]["urgency_score"],
        reverse=True
    )

    critical_count: int = sum(
        1 for _, p in sorted_urgency if p["urgency_level"] == "CRITICAL"
    )
    high_count: int = sum(
        1 for _, p in sorted_urgency if p["urgency_level"] == "HIGH"
    )

    # Determine overall pressure level
    pressure_level: str
    if critical_count >= 2:
        pressure_level = "CRITICAL"
    elif critical_count >= 1 or high_count >= 3:
        pressure_level = "HIGH"
    elif high_count >= 1:
        pressure_level = "MEDIUM"
    else:
        pressure_level = "LOW"

    # Get top 3 recommended projects (excluding completed/archived/on-hold)
    recommended: List[Dict[str, str]] = [
        {"project": k, "urgency": p["urgency_level"]}
        for k, p in sorted_urgency
        if p["status"] not in ["complete", "archived", "on-hold"]
    ][:3]

    return {
        "project_urgency": dict(sorted_urgency),
        "overall_pressure": {
            "level": pressure_level,
            "critical_projects": critical_count,
            "high_urgency_projects": high_count,
        },
        "recommended_focus": recommended,
    }


# ============================================================================
# COGNITIVE MODULE 2: CONTRADICTION DETECTION
# ============================================================================

# Decision patterns for extraction
DECISION_PATTERNS: List[Tuple[str, str]] = [
    (r"(?:decided to|will|going to|planning to|committed to)\s+(.+)", "commitment"),
    (r"(?:completed|done|finished|✅)\s+(.+)", "completion"),
    (r"(?:priority|critical|urgent|must|need to)\s+(.+)", "priority"),
    (r"(?:stopping|pausing|putting on hold|abandoning)\s+(.+)", "abandonment"),
    (r"(?:switching to|pivoting to|going with)\s+(.+)", "pivot"),
]


def extract_decisions(sessions: List[Dict[str, Any]], lookback_days: int = 30) -> List[Dict[str, Any]]:
    """Extract decisions from session history
    
    Scans session summaries and achievements for decision patterns
    using regex matching.
    
    Args:
        sessions: List of session dictionaries
        lookback_days: Number of days to look back (unused currently, kept for API compatibility)
        
    Returns:
        List of decision dictionaries with date, type, and text
    """
    decisions: List[Dict[str, Any]] = []

    for session in sessions[-20:]:  # Last 20 sessions
        text: str = session.get("summary", "") + " " + " ".join(
            session.get("achievements", [])
        )

        for pattern, decision_type in DECISION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decision_text: str = (
                    match.group(1).strip() if match.groups() else match.group(0).strip()
                )
                decisions.append({
                    "date": session.get("date"),
                    "type": decision_type,
                    "text": decision_text,
                })

    return decisions


def check_statement_conflict(statement: str, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Check if statement conflicts with past decisions
    
    Analyzes a new statement against historical decisions to detect
    potential contradictions or pivots.
    
    Args:
        statement: New statement to check for conflicts
        sessions: List of session dictionaries
        
    Returns:
        Dictionary containing:
        - conflicts_found: Boolean indicating if conflicts detected
        - conflict_count: Number of conflicts found
        - conflicts: List of conflict details (max 5)
    """
    decisions: List[Dict[str, Any]] = extract_decisions(sessions)
    statement_words: Set[str] = set(statement.lower().split())
    conflicts: List[Dict[str, Any]] = []

    for dec in decisions:
        dec_words: Set[str] = set(dec["text"].lower().split())
        overlap: Set[str] = statement_words & dec_words

        if len(overlap) >= 2:
            conflict_detected: bool = False
            reason: str = ""

            # Check for negation conflicts
            if any(word in statement.lower() for word in ["don't", "won't"]):
                if dec["type"] in ["commitment", "priority"]:
                    conflict_detected = True
                    reason = f"Contradicts past {dec['type']}"

            # Check for pivot conflicts
            if any(word in statement.lower() for word in ["switching", "instead"]):
                if dec["type"] in ["commitment", "focus"]:
                    conflict_detected = True
                    reason = "Pivots from past commitment"

            if conflict_detected:
                conflicts.append({
                    "past_decision": dec,
                    "reason": reason,
                    "overlap": list(overlap),
                })

    return {
        "conflicts_found": len(conflicts) > 0,
        "conflict_count": len(conflicts),
        "conflicts": conflicts[:5],  # Return max 5 conflicts
    }


# ============================================================================
# COGNITIVE MODULE 3: NARRATIVE ARC ANALYSIS
# ============================================================================


def calculate_momentum(sessions: List[Dict[str, Any]], days: int = 7) -> str:
    """Calculate momentum from recent sessions
    
    Analyzes session frequency to determine work momentum.
    
    Args:
        sessions: List of all sessions
        days: Number of days to analyze (default 7)
        
    Returns:
        Momentum level string (accelerating/steady/slow/stalled/starting)
    """
    if not sessions:
        return "starting"

    recent: List[Dict[str, Any]] = sessions[-days:] if len(sessions) > days else sessions

    if len(recent) == 0:
        return "stalled"

    sessions_per_day: float = len(recent) / days

    if sessions_per_day > 1.5:
        return "accelerating"
    if sessions_per_day > 0.8:
        return "steady"
    if sessions_per_day > 0.3:
        return "slow"
    return "stalled"


def detect_arc_type(sessions: List[Dict[str, Any]]) -> str:
    """Detect current narrative arc type
    
    Analyzes recent session summaries to classify the current story arc.
    
    Args:
        sessions: List of all sessions
        
    Returns:
        Arc type string (beginning/building_momentum/overcoming_obstacles/
        exploration/recovery/plateau/steady_progress)
    """
    if not sessions:
        return "beginning"

    recent: List[Dict[str, Any]] = sessions[-5:]
    summaries: str = " ".join([s.get("summary", "").lower() for s in recent])

    # Pattern matching for arc detection
    if any(word in summaries for word in ["complete", "finished", "deployed"]):
        return "building_momentum"
    if any(word in summaries for word in ["stuck", "blocked", "debugging"]):
        return "overcoming_obstacles"
    if any(word in summaries for word in ["exploring", "researching", "learning"]):
        return "exploration"
    if any(word in summaries for word in ["back to", "resuming"]):
        return "recovery"

    # Fall back to momentum-based classification
    momentum: str = calculate_momentum(sessions)
    if momentum in ["accelerating", "steady"]:
        return "building_momentum"
    if momentum == "stalled":
        return "plateau"

    return "steady_progress"


def get_story_arc_analysis(state: Dict[str, Any], log: Dict[str, Any]) -> Dict[str, Any]:
    """Get complete narrative arc analysis
    
    Provides a comprehensive story arc analysis including arc type,
    momentum, and narrative description.
    
    Args:
        state: CoreState dictionary
        log: SessionLog dictionary
        
    Returns:
        Dictionary containing:
        - current_arc: Arc type classification
        - momentum: Momentum level
        - narrative: Human-readable narrative description
        - total_sessions: Total session count
        - active_threads: Number of active projects
    """
    sessions: List[Dict[str, Any]] = log.get("sessions", [])
    arc_type: str = detect_arc_type(sessions)
    momentum: str = calculate_momentum(sessions)

    total_sessions: int = len(sessions)
    active_projects: int = len([
        p for p in state.get("project_states", {}).values()
        if p.get("status") == "active"
    ])
    wins: int = len(state.get("recent_wins", []))

    # Build narrative description
    narrative_parts: List[str] = []

    if total_sessions == 0:
        narrative_parts.append("The journey begins.")
    else:
        narrative_parts.append(f"{total_sessions} sessions into the journey.")

    if active_projects == 1:
        narrative_parts.append("Focused on a single quest.")
    elif active_projects > 1:
        narrative_parts.append(f"Juggling {active_projects} parallel quests.")

    narrative_parts.append(f"Arc: {arc_type}.")

    if momentum == "accelerating":
        narrative_parts.append("Velocity increasing.")
    elif momentum == "stalled":
        narrative_parts.append("Momentum paused.")

    if wins > 0:
        narrative_parts.append(f"{wins} victories claimed.")

    return {
        "current_arc": arc_type,
        "momentum": momentum,
        "narrative": " ".join(narrative_parts),
        "total_sessions": total_sessions,
        "active_threads": active_projects,
    }


# ============================================================================
# COGNITIVE MODULE 4: AFFECTIVE TRENDS ANALYSIS
# ============================================================================


def infer_energy_level(sessions: List[Dict[str, Any]]) -> str:
    """Infer energy level from recent activity
    
    Uses achievement count as a proxy for energy/productivity.
    
    Args:
        sessions: List of all sessions
        
    Returns:
        Energy level string (unknown/low/medium/high)
    """
    if not sessions:
        return "unknown"

    recent: List[Dict[str, Any]] = sessions[-7:] if len(sessions) > 7 else sessions

    if len(recent) == 0:
        return "low"

    total_achievements: int = sum(len(s.get("achievements", [])) for s in recent)
    avg_achievements: float = total_achievements / len(recent)

    if avg_achievements > 5:
        return "high"
    if avg_achievements > 3:
        return "medium"
    return "low"


def detect_work_state(sessions: List[Dict[str, Any]], state: Dict[str, Any]) -> str:
    """Detect current work state from session patterns
    
    Analyzes recent session summaries to classify current work mode.
    
    Args:
        sessions: List of all sessions
        state: CoreState dictionary (unused currently, kept for API compatibility)
        
    Returns:
        Work state string (starting/deep_focus/problem_solving/creation/
        learning/planning/steady_work)
    """
    if not sessions:
        return "starting"

    recent: List[Dict[str, Any]] = sessions[-3:]
    summaries: str = " ".join([s.get("summary", "").lower() for s in recent])

    # Pattern matching for work state
    if "deep work" in summaries or "focused" in summaries:
        return "deep_focus"
    if "debugging" in summaries or "stuck" in summaries:
        return "problem_solving"
    if "building" in summaries or "creating" in summaries:
        return "creation"
    if "learning" in summaries or "exploring" in summaries:
        return "learning"
    if "planning" in summaries or "designing" in summaries:
        return "planning"

    return "steady_work"


def get_affective_trends_analysis(state: Dict[str, Any], log: Dict[str, Any]) -> Dict[str, Any]:
    """Get affective trends analysis
    
    Analyzes behavioral and productivity trends over time.
    
    Args:
        state: CoreState dictionary
        log: SessionLog dictionary
        
    Returns:
        Dictionary containing:
        - current_state: Current work state classification
        - energy_level: Inferred energy level
        - productivity_trend: Trend direction (increasing/stable/decreasing/insufficient_data)
        - sessions_analyzed: Number of sessions analyzed
    """
    sessions: List[Dict[str, Any]] = log.get("sessions", [])
    energy: str = infer_energy_level(sessions)
    work_state: str = detect_work_state(sessions, state)

    # Calculate productivity trend
    trend: str
    if len(sessions) >= 4:
        mid: int = len(sessions) // 2
        first_half: List[Dict[str, Any]] = sessions[:mid]
        second_half: List[Dict[str, Any]] = sessions[mid:]

        first_rate: int = len(first_half)
        second_rate: int = len(second_half)

        if second_rate > first_rate * 1.2:
            trend = "increasing"
        elif second_rate < first_rate * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"

    return {
        "current_state": work_state,
        "energy_level": energy,
        "productivity_trend": trend,
        "sessions_analyzed": len(sessions),
    }


# ============================================================================
# PHASE 2 COGNITIVE MODULES - COMPLETE
# ============================================================================

# Helper function needed by cognitive modules (defined in Phase 1)
def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Number of days since the date, or 0 if date is invalid
    """
    if not date_str:
        return 0
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - date
        return delta.days
    except (ValueError, TypeError):
        return 0
