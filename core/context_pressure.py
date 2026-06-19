"""
Context Pressure Module
Transforms "what exists" into "what matters NOW" through dynamic urgency scoring
"""

from datetime import datetime
from typing import Dict, List, Tuple


def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date"""
    if not date_str:
        return 0
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - date
        return delta.days
    except:
        return 0


def get_priority_weight(priority: str) -> float:
    """Get numeric weight for priority level"""
    weights = {
        "critical": 3.0,
        "high": 2.0,
        "medium": 1.0,
        "low": 0.5,
    }
    return weights.get(priority, 1.0)


def get_staleness_multiplier(project: Dict) -> float:
    """Calculate staleness multiplier based on project state"""
    completion = project.get("completion", 0)
    days_since = calculate_days_since(project.get("last_worked", ""))
    status = project.get("status", "active")
    
    # High completion but stalled = DANGER ZONE
    if completion >= 70 and days_since > 7:
        return 2.0
    
    # Active but cold
    if status == "active" and days_since > 3:
        return 1.5
    
    # On hold
    if status == "on-hold":
        return 0.3
    
    # Complete or archived
    if status in ["complete", "archived"]:
        return 0.0
    
    return 1.0


def calculate_urgency(project: Dict) -> float:
    """Calculate urgency score for a project"""
    days_since = calculate_days_since(project.get("last_worked", ""))
    priority_weight = get_priority_weight(project.get("priority", "medium"))
    staleness = get_staleness_multiplier(project)
    
    urgency = days_since * priority_weight * staleness
    return round(urgency, 1)


def classify_urgency(score: float) -> str:
    """Classify urgency level"""
    if score >= 20:
        return "CRITICAL"  # Drop everything
    if score >= 10:
        return "HIGH"      # Address soon
    if score >= 5:
        return "MEDIUM"    # Monitor
    if score > 0:
        return "LOW"       # Background
    return "NONE"         # Inactive


def get_urgency_reason(project: Dict, urgency: float, days: int) -> str:
    """Generate human-readable urgency reason"""
    completion = project.get("completion", 0)
    status = project.get("status", "active")
    priority = project.get("priority", "medium")
    
    if status in ["complete", "archived"]:
        return "Project complete"
    
    if status == "on-hold":
        return "Intentionally on hold"
    
    if completion >= 90 and days > 7:
        return f"DANGER: {completion}% done but {days} days cold - finish this!"
    
    if completion >= 70 and days > 7:
        return f"High completion ({completion}%) but stalled {days} days"
    
    if priority == "critical" and days > 3:
        return f"Critical priority but {days} days without progress"
    
    if days > 14:
        return f"Very stale - {days} days since last touch"
    
    return f"{days} days since last worked"


def analyze_context_pressure(state: Dict) -> Dict:
    """Analyze context pressure across all projects"""
    projects = state.get("project_states", {})
    project_urgency = {}
    
    # Calculate urgency for each project
    for key, project in projects.items():
        urgency = calculate_urgency(project)
        level = classify_urgency(urgency)
        days = calculate_days_since(project.get("last_worked", ""))
        
        project_urgency[key] = {
            "urgency_score": urgency,
            "urgency_level": level,
            "days_since_touch": days,
            "priority": project.get("priority", "medium"),
            "completion": project.get("completion", 0),
            "status": project.get("status", "active"),
            "reason": get_urgency_reason(project, urgency, days)
        }
    
    # Sort by urgency descending
    sorted_urgency = sorted(
        project_urgency.items(),
        key=lambda x: x[1]["urgency_score"],
        reverse=True
    )
    
    # Calculate overall pressure
    critical_count = sum(1 for _, p in sorted_urgency if p["urgency_level"] == "CRITICAL")
    high_count = sum(1 for _, p in sorted_urgency if p["urgency_level"] == "HIGH")
    
    if critical_count >= 2:
        pressure_level = "CRITICAL"
    elif critical_count >= 1 or high_count >= 3:
        pressure_level = "HIGH"
    elif high_count >= 1:
        pressure_level = "MEDIUM"
    else:
        pressure_level = "LOW"
    
    # Recommended focus (top 3 active projects)
    recommended_focus = [
        {
            "project": key,
            "urgency": p["urgency_level"],
            "reason": p["reason"]
        }
        for key, p in sorted_urgency
        if p["status"] not in ["complete", "archived", "on-hold"]
    ][:3]
    
    return {
        "project_urgency": dict(sorted_urgency),
        "overall_pressure": {
            "level": pressure_level,
            "critical_projects": critical_count,
            "high_urgency_projects": high_count
        },
        "recommended_focus": recommended_focus
    }
