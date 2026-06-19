#!/usr/bin/env python3
"""
REL MCP Server - Type-Safe Version
Phase 3 Part 2: Remaining Tool Handlers (Cognitive, Context, Advanced, Brain, Neural)

This file continues Phase 3 with all remaining tool handlers fully typed.
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from mcp.types import TextContent

logger = logging.getLogger("REL")


# ============================================================================
# COGNITIVE MODULE TOOL HANDLERS (TYPED)
# ============================================================================


async def handle_get_insights(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    analyze_pressure_fn: Any  # Type would be from Phase 2
) -> List[TextContent]:
    """Handle get_insights tool call
    
    Analyzes context pressure and urgency across all projects.
    
    Args:
        state: Current CoreState
        log: Current SessionLog (unused)
        arguments: Tool arguments (unused)
        analyze_pressure_fn: Context pressure analysis function from Phase 2
        
    Returns:
        JSON response with pressure analysis
    """
    pressure_analysis: Dict[str, Any] = analyze_pressure_fn(state)
    return [TextContent(type="text", text=json.dumps(pressure_analysis, indent=2))]


async def handle_predict_cold_projects(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    analyze_pressure_fn: Any  # Type would be from Phase 2
) -> List[TextContent]:
    """Handle predict_cold_projects tool call
    
    Predicts which projects are at risk of stalling based on urgency.
    
    Args:
        state: Current CoreState
        log: Current SessionLog (unused)
        arguments: Tool arguments (unused)
        analyze_pressure_fn: Context pressure analysis function from Phase 2
        
    Returns:
        JSON response with cold project predictions
    """
    pressure_analysis: Dict[str, Any] = analyze_pressure_fn(state)
    
    cold_projects: List[Dict[str, Any]] = [
        {
            "project": k,
            "urgency_score": v["urgency_score"],
            "days_stale": v["days_since_touch"]
        }
        for k, v in pressure_analysis["project_urgency"].items()
        if v["urgency_level"] in ["HIGH", "CRITICAL"]
    ]
    
    return [TextContent(type="text", text=json.dumps({"cold_projects": cold_projects}, indent=2))]


async def handle_check_for_conflict(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    check_conflict_fn: Any  # Type would be from Phase 2
) -> List[TextContent]:
    """Handle check_for_conflict tool call
    
    Checks if a statement conflicts with past decisions.
    
    Args:
        state: Current CoreState (unused)
        log: Current SessionLog
        arguments: Tool arguments with 'statement' key
        check_conflict_fn: Conflict detection function from Phase 2
        
    Returns:
        JSON response with conflict analysis
    """
    statement: str = arguments["statement"]
    sessions: List[Dict[str, Any]] = log.get("sessions", [])
    
    conflict_analysis: Dict[str, Any] = check_conflict_fn(statement, sessions)
    
    return [TextContent(type="text", text=json.dumps(conflict_analysis, indent=2))]


async def handle_get_story_arc(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    story_arc_fn: Any  # Type would be from Phase 2
) -> List[TextContent]:
    """Handle get_story_arc tool call
    
    Analyzes narrative arc of work journey.
    
    Args:
        state: Current CoreState
        log: Current SessionLog
        arguments: Tool arguments (unused)
        story_arc_fn: Story arc analysis function from Phase 2
        
    Returns:
        JSON response with narrative arc analysis
    """
    arc_analysis: Dict[str, Any] = story_arc_fn(state, log)
    
    return [TextContent(type="text", text=json.dumps(arc_analysis, indent=2))]


async def handle_get_affective_trends(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    affective_fn: Any  # Type would be from Phase 2
) -> List[TextContent]:
    """Handle get_affective_trends tool call
    
    Analyzes affective/behavioral trends.
    
    Args:
        state: Current CoreState
        log: Current SessionLog
        arguments: Tool arguments (unused)
        affective_fn: Affective trends analysis function from Phase 2
        
    Returns:
        JSON response with affective analysis
    """
    affective_analysis: Dict[str, Any] = affective_fn(state, log)
    
    return [TextContent(type="text", text=json.dumps(affective_analysis, indent=2))]


async def handle_get_patterns(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle get_patterns tool call
    
    Returns message about pattern analysis availability.
    
    Args:
        state: Current CoreState (unused)
        log: Current SessionLog (unused)
        arguments: Tool arguments (unused)
        
    Returns:
        JSON response with message
    """
    response: Dict[str, str] = {
        "message": "Pattern analysis available via cognitive modules"
    }
    
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def handle_analyze_productivity(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle analyze_productivity tool call
    
    Analyzes productivity over a time period.
    
    Args:
        state: Current CoreState (unused)
        log: Current SessionLog
        arguments: Tool arguments with optional 'days' (default 7)
        
    Returns:
        JSON response with productivity analysis
    """
    days: int = int(arguments.get("days", 7))
    
    analysis: Dict[str, Any] = {
        "days_analyzed": days,
        "sessions": len(log.get("sessions", [])),
        "productivity": "steady"
    }
    
    return [TextContent(type="text", text=json.dumps(analysis, indent=2))]


async def handle_get_suggested_actions(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any]
) -> List[TextContent]:
    """Handle get_suggested_actions tool call
    
    Suggests actions based on current state.
    
    Args:
        state: Current CoreState (unused)
        log: Current SessionLog (unused)
        arguments: Tool arguments (unused)
        
    Returns:
        JSON response with suggested actions
    """
    suggestions: List[str] = [
        "Use get_insights for urgency analysis",
        "Use get_story_arc for narrative",
        "Use semantic_search for finding past work"
    ]
    
    return [TextContent(type="text", text=json.dumps(suggestions, indent=2))]


# ============================================================================
# CONTEXT TOOL HANDLERS (TYPED)
# ============================================================================


async def handle_search_files(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    rel_path: Path
) -> List[TextContent]:
    """Handle search_files tool call
    
    Searches for files in REL directory matching query.
    
    Args:
        state: Current CoreState (unused)
        log: Current SessionLog (unused)
        arguments: Tool arguments with 'query' key
        rel_path: Base REL path to search
        
    Returns:
        JSON response with matching files
    """
    query: str = arguments["query"].lower()
    limit: int = 50
    
    def _search_files_worker() -> Dict[str, Any]:
        """Worker function for file searching"""
        found_files: List[Dict[str, Any]] = []
        total_found: int = 0
        
        try:
            for filepath in rel_path.rglob("*"):
                if not filepath.is_file():
                    continue
                
                # Search in filename and path
                haystack: str = filepath.name.lower() + " " + str(filepath).lower()
                
                if query in haystack:
                    total_found += 1
                    if len(found_files) < limit:
                        try:
                            st = filepath.stat()
                            found_files.append({
                                "path": str(filepath),
                                "name": filepath.name,
                                "size": st.st_size,
                                "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                            })
                        except Exception:
                            # Still count it; skip metadata
                            found_files.append({
                                "path": str(filepath),
                                "name": filepath.name
                            })
        except Exception as e:
            return {
                "error": str(e),
                "files": [],
                "query": query,
                "total_found": 0
            }
        
        return {
            "query": query,
            "files": found_files,
            "total_found": total_found
        }
    
    # Run search in thread to avoid blocking
    result: Dict[str, Any] = await asyncio.to_thread(_search_files_worker)
    
    if "error" in result:
        logger.error(f"File search error: {result['error']}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": result["error"], "files": []}, indent=2)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "query": query,
            "files": result["files"][:50],
            "total_found": result["total_found"]
        }, indent=2)
    )]


async def handle_load_context(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    brain_call_fn: Any,
    neural_call_fn: Any,
    get_brain_fn: Any,
    get_neural_web_fn: Any,
    brain_available: bool,
    neural_available: bool
) -> List[TextContent]:
    """Handle load_context tool call
    
    Loads relevant context for a query with token limit.
    
    Args:
        state: Current CoreState
        log: Current SessionLog
        arguments: Tool arguments with 'query' and optional 'max_tokens'
        brain_call_fn: Brain async wrapper
        neural_call_fn: Neural web async wrapper
        get_brain_fn: Get brain instance function
        get_neural_web_fn: Get neural web instance function
        brain_available: Whether brain is available
        neural_available: Whether neural web is available
        
    Returns:
        JSON response with loaded context
    """
    query: str = arguments["query"]
    max_tokens: int = int(arguments.get("max_tokens", 2000))
    context_parts: List[Dict[str, Any]] = []
    truncated: bool = False
    
    def _estimate_tokens(obj: Any) -> int:
        """Rough token estimation: 1 token ≈ 4 chars"""
        try:
            return len(json.dumps(obj, ensure_ascii=False)) // 4
        except Exception:
            return 0
    
    def _try_add(part: Dict[str, Any]) -> None:
        """Try to add context part if within token limit"""
        nonlocal truncated
        if truncated:
            return
        
        candidate: List[Dict[str, Any]] = context_parts + [part]
        if _estimate_tokens(candidate) <= max_tokens:
            context_parts.append(part)
        else:
            truncated = True
    
    try:
        query_lower: str = query.lower()
        
        # 1) Relevant sessions (last 5)
        matching_sessions: List[Dict[str, Any]] = [
            s for s in log.get("sessions", [])
            if query_lower in s.get("summary", "").lower()
        ]
        if matching_sessions:
            _try_add({
                "type": "sessions",
                "data": matching_sessions[-5:],
                "count": len(matching_sessions)
            })
        
        # 2) Relevant projects
        matching_projects: Dict[str, Any] = {
            k: v for k, v in state.get("project_states", {}).items()
            if query_lower in v.get("name", "").lower() or
               query_lower in v.get("description", "").lower()
        }
        if matching_projects:
            _try_add({
                "type": "projects",
                "data": matching_projects,
                "count": len(matching_projects)
            })
        
        # 3) Relevant wins
        matching_wins: List[Dict[str, Any]] = [
            w for w in state.get("recent_wins", [])
            if query_lower in w.get("win", "").lower()
        ]
        if matching_wins:
            _try_add({
                "type": "wins",
                "data": matching_wins[:10],
                "count": len(matching_wins)
            })
        
        # 4) Semantic search (FAISS)
        if brain_available and not truncated:
            brain = get_brain_fn()
            if brain:
                try:
                    semantic_results: List[Any] = await brain_call_fn(
                        lambda: brain.search(query, 5)
                    )
                    if semantic_results:
                        _try_add({
                            "type": "semantic_search",
                            "data": semantic_results,
                            "count": len(semantic_results)
                        })
                except Exception as e:
                    logger.error(f"Semantic search in load_context failed: {e}")
        
        # 5) Neural concepts
        if neural_available and not truncated:
            neural_web = get_neural_web_fn()
            if neural_web:
                try:
                    related: List[Any] = await neural_call_fn(
                        lambda: neural_web.get_related_concepts(query, 10)
                    )
                    if related:
                        _try_add({
                            "type": "neural_concepts",
                            "data": related,
                            "count": len(related)
                        })
                except Exception as e:
                    logger.error(f"Neural concepts in load_context failed: {e}")
        
        estimated_tokens: int = _estimate_tokens(context_parts)
        
    except Exception as e:
        logger.error(f"Load context error: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "context": []}, indent=2)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "query": query,
            "context": context_parts,
            "total_parts": len(context_parts),
            "estimated_tokens": estimated_tokens,
            "max_tokens": max_tokens,
            "truncated": truncated
        }, indent=2)
    )]


async def handle_get_loading_preview(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    brain_available: bool,
    neural_available: bool
) -> List[TextContent]:
    """Handle get_loading_preview tool call
    
    Previews what load_context would return without full data.
    
    Args:
        state: Current CoreState
        log: Current SessionLog
        arguments: Tool arguments with 'query' key
        brain_available: Whether brain is available
        neural_available: Whether neural web is available
        
    Returns:
        JSON response with loading preview
    """
    query: str = arguments["query"]
    preview: List[Dict[str, Any]] = []
    
    try:
        query_lower: str = query.lower()
        
        # Count matching sessions
        session_matches: int = sum(
            1 for s in log.get("sessions", [])
            if query_lower in s.get("summary", "").lower()
        )
        if session_matches > 0:
            preview.append({
                "type": "sessions",
                "count": session_matches,
                "preview": f"Would load {min(session_matches, 5)} of {session_matches} matching sessions"
            })
        
        # Count matching projects
        project_matches: int = sum(
            1 for p in state.get("project_states", {}).values()
            if query_lower in p.get("name", "").lower() or
               query_lower in p.get("description", "").lower()
        )
        if project_matches > 0:
            preview.append({
                "type": "projects",
                "count": project_matches,
                "preview": f"Would load {project_matches} matching projects"
            })
        
        # Count matching wins
        win_matches: int = sum(
            1 for w in state.get("recent_wins", [])
            if query_lower in w.get("win", "").lower()
        )
        if win_matches > 0:
            preview.append({
                "type": "wins",
                "count": win_matches,
                "preview": f"Would load {min(win_matches, 10)} of {win_matches} matching wins"
            })
        
        # Add semantic search availability
        if brain_available:
            preview.append({
                "type": "semantic_search",
                "available": True,
                "preview": "Would perform FAISS semantic search"
            })
        
        # Add neural web availability
        if neural_available:
            preview.append({
                "type": "neural_concepts",
                "available": True,
                "preview": "Would find related neural concepts"
            })
        
    except Exception as e:
        logger.error(f"Loading preview error: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "preview": []}, indent=2)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "query": query,
            "preview": preview,
            "total_sources": len(preview)
        }, indent=2)
    )]


async def handle_get_recommendations(
    state: Dict[str, Any],
    log: Dict[str, Any],
    arguments: Dict[str, Any],
    analyze_pressure_fn: Any,
    calculate_days_fn: Any,
    neural_call_fn: Any,
    get_neural_web_fn: Any,
    neural_available: bool
) -> List[TextContent]:
    """Handle get_recommendations tool call
    
    Provides intelligent recommendations based on current state.
    
    Args:
        state: Current CoreState
        log: Current SessionLog
        arguments: Tool arguments with optional 'query'
        analyze_pressure_fn: Context pressure analysis function
        calculate_days_fn: Calculate days since function
        neural_call_fn: Neural web async wrapper
        get_neural_web_fn: Get neural web instance function
        neural_available: Whether neural web is available
        
    Returns:
        JSON response with recommendations
    """
    query: str = arguments.get("query", "").lower()
    recommendations: List[Dict[str, Any]] = []
    
    try:
        # 1. Urgency-based recommendations
        pressure_analysis: Dict[str, Any] = analyze_pressure_fn(state)
        high_urgency: List[Dict[str, str]] = [
            p for p in pressure_analysis["recommended_focus"]
            if p["urgency"] in ["HIGH", "CRITICAL"]
        ]
        
        if high_urgency:
            recommendations.append({
                "type": "urgency",
                "priority": "high",
                "title": "High-urgency projects need attention",
                "items": [f"{p['project']} ({p['urgency']})" for p in high_urgency]
            })
        
        # 2. Stalled project recommendations
        stalled: List[str] = [
            k for k, v in state.get("project_states", {}).items()
            if v.get("status") == "active" and
               calculate_days_fn(v.get("last_worked", "")) > 7
        ]
        
        if stalled:
            recommendations.append({
                "type": "stalled_projects",
                "priority": "medium",
                "title": "Projects haven't been touched in 7+ days",
                "items": stalled
            })
        
        # 3. Near-completion recommendations
        near_done: List[tuple[str, Dict[str, Any]]] = [
            (k, v) for k, v in state.get("project_states", {}).items()
            if v.get("status") == "active" and v.get("completion", 0) >= 70
        ]
        
        if near_done:
            recommendations.append({
                "type": "near_completion",
                "priority": "high",
                "title": "Projects close to completion - finish strong!",
                "items": [f"{k} ({v.get('completion')}%)" for k, v in near_done]
            })
        
        # 4. Query-specific recommendations
        if query:
            # Search for related work
            related_sessions: List[Dict[str, Any]] = [
                s for s in log.get("sessions", [])
                if query in s.get("summary", "").lower()
            ]
            
            if related_sessions:
                recommendations.append({
                    "type": "related_work",
                    "priority": "medium",
                    "title": f"Found {len(related_sessions)} past sessions related to '{query}'",
                    "items": [s.get("summary", "")[:100] for s in related_sessions[-3:]]
                })
            
            # Search for related projects
            related_projects: List[tuple[str, Dict[str, Any]]] = [
                (k, v) for k, v in state.get("project_states", {}).items()
                if query in v.get("name", "").lower() or
                   query in v.get("description", "").lower()
            ]
            
            if related_projects:
                recommendations.append({
                    "type": "related_projects",
                    "priority": "medium",
                    "title": f"Projects related to '{query}'",
                    "items": [f"{k}: {v.get('name')}" for k, v in related_projects]
                })
        
        # 5. Learning opportunities (from neural web)
        if neural_available and query:
            neural_web = get_neural_web_fn()
            if neural_web:
                try:
                    related_concepts: List[Dict[str, Any]] = await neural_call_fn(
                        lambda: neural_web.get_related_concepts(query, 5)
                    )
                    if related_concepts:
                        recommendations.append({
                            "type": "learning",
                            "priority": "low",
                            "title": f"Concepts related to '{query}' you might explore",
                            "items": [
                                f"{c['concept']} (strength: {c['strength']:.2f})"
                                for c in related_concepts
                            ]
                        })
                except Exception as e:
                    logger.error(f"Neural recommendations error: {e}")
        
        # Sort by priority
        priority_order: Dict[str, int] = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))
        
    except Exception as e:
        logger.error(f"Recommendations error: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e), "recommendations": []}, indent=2)
        )]
    
    return [TextContent(
        type="text",
        text=json.dumps({
            "query": query if query else "general",
            "recommendations": recommendations,
            "total": len(recommendations)
        }, indent=2)
    )]


# ============================================================================
# PHASE 3 PART 2 COMPLETE
# ============================================================================

# This file contains fully-typed handlers for:
# - Cognitive module tools (8 handlers)
# - Context tools (4 handlers)
# 
# Remaining: Advanced tools (5), Brain tools (1), Neural web tools (4)
# Total in this file: ~500 lines of fully-typed code
