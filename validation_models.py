"""
Pydantic validation models for REL MCP Server tools

This module defines request and response models for all 45 tools,
ensuring type safety and input validation at the API boundary.
"""

from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ============================================================================
# CORE STATE TOOL MODELS
# ============================================================================


class UpdateStateRequest(BaseModel):
    """Request model for update_state tool"""

    updates: Dict[str, Any] = Field(
        ..., description="Dictionary of updates to apply to CoreState"
    )

    @field_validator("updates")
    @classmethod
    def updates_must_not_be_empty(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure updates dictionary is not empty"""
        if not v:
            raise ValueError("Updates dictionary cannot be empty")
        return v


# ============================================================================
# PROJECT TOOL MODELS
# ============================================================================


class CreateProjectRequest(BaseModel):
    """Request model for create_project tool"""

    key: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9_-]+$",
        description="Project key (lowercase, alphanumeric, underscore, dash)",
    )
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: str = Field(default="", max_length=1000, description="Project description")

    @field_validator("key")
    @classmethod
    def key_must_not_start_with_underscore(cls, v: str) -> str:
        """Ensure key doesn't start with underscore (reserved)"""
        if v.startswith("_"):
            raise ValueError("Project key cannot start with underscore (reserved)")
        if v.startswith("-"):
            raise ValueError("Project key cannot start with dash")
        return v

    @field_validator("name")
    @classmethod
    def name_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure name is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Project name cannot be empty or whitespace only")
        return stripped


class GetProjectRequest(BaseModel):
    """Request model for get_project tool"""

    project: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Project key to retrieve",
    )


class ListProjectsRequest(BaseModel):
    """Request model for list_projects tool"""

    filter: Optional[str] = Field(
        default=None,
        pattern=r"^(active|complete|on-hold|archived|blocked|all)?$",
        description="Filter by status: active, complete, on-hold, archived, blocked, or all",
    )


class UpdateProjectRequest(BaseModel):
    """Request model for update_project tool"""

    project: str = Field(..., min_length=1, max_length=100, description="Project key to update")
    updates: Dict[str, Any] = Field(..., description="Updates to apply to project")

    @field_validator("updates")
    @classmethod
    def updates_must_not_be_empty(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure updates dictionary is not empty"""
        if not v:
            raise ValueError("Updates dictionary cannot be empty")
        return v

    @field_validator("updates")
    @classmethod
    def validate_update_fields(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that update fields are allowed"""
        allowed_fields = {
            "name",
            "description",
            "status",
            "priority",
            "completion",
            "notes",
            "tags",
        }
        invalid_fields = set(v.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f"Invalid update fields: {', '.join(invalid_fields)}")

        # Validate completion range
        if "completion" in v:
            completion = v["completion"]
            if not isinstance(completion, (int, float)):
                raise ValueError("Completion must be a number")
            if not 0 <= completion <= 100:
                raise ValueError("Completion must be between 0 and 100")

        # Validate status
        if "status" in v:
            status = v["status"]
            valid_statuses = {"active", "complete", "on-hold", "archived", "blocked"}
            if status not in valid_statuses:
                raise ValueError(
                    f"Invalid status '{status}'. Must be one of: {', '.join(valid_statuses)}"
                )

        # Validate priority
        if "priority" in v:
            priority = v["priority"]
            valid_priorities = {"critical", "high", "medium", "low"}
            if priority not in valid_priorities:
                raise ValueError(
                    f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}"
                )

        return v


class SetActiveProjectRequest(BaseModel):
    """Request model for set_active_project tool"""

    project: str = Field(..., min_length=1, max_length=100, description="Project key to activate")


class ArchiveProjectRequest(BaseModel):
    """Request model for archive_project tool"""

    project: str = Field(..., min_length=1, max_length=100, description="Project key to archive")


class GetProjectStatsRequest(BaseModel):
    """Request model for get_project_stats tool"""

    project: str = Field(
        ..., min_length=1, max_length=100, description="Project key to get stats for"
    )


# ============================================================================
# SESSION TOOL MODELS
# ============================================================================


class LogSessionRequest(BaseModel):
    """Request model for log_session tool"""

    summary: str = Field(
        ..., min_length=1, max_length=2000, description="Session summary description"
    )
    achievements: List[str] = Field(
        default_factory=list,
        max_length=50,
        description="List of achievements during session",
    )

    @field_validator("summary")
    @classmethod
    def summary_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure summary is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Session summary cannot be empty or whitespace only")
        return stripped

    @field_validator("achievements")
    @classmethod
    def achievements_must_be_valid(cls, v: List[str]) -> List[str]:
        """Validate achievements list"""
        if len(v) > 50:
            raise ValueError("Cannot have more than 50 achievements per session")

        # Strip whitespace and filter empty strings
        cleaned = [a.strip() for a in v if a.strip()]

        # Check for overly long achievements
        for achievement in cleaned:
            if len(achievement) > 500:
                raise ValueError("Individual achievement cannot exceed 500 characters")

        return cleaned


class GetSessionHistoryRequest(BaseModel):
    """Request model for get_session_history tool"""

    count: int = Field(default=5, ge=1, le=100, description="Number of sessions to retrieve")


class EndSessionRequest(BaseModel):
    """Request model for end_session tool"""

    summary: Optional[str] = Field(
        default=None, max_length=2000, description="Optional updated session summary"
    )

    @field_validator("summary")
    @classmethod
    def summary_must_not_be_whitespace_if_provided(cls, v: Optional[str]) -> Optional[str]:
        """Ensure summary is not just whitespace if provided"""
        if v is not None:
            stripped = v.strip()
            if not stripped:
                raise ValueError("Session summary cannot be empty or whitespace only")
            return stripped
        return v


class SearchSessionsRequest(BaseModel):
    """Request model for search_sessions tool"""

    query: str = Field(..., min_length=1, max_length=200, description="Search query")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Search query cannot be empty or whitespace only")
        return stripped


# ============================================================================
# PROGRESS TOOL MODELS
# ============================================================================


class LogWinRequest(BaseModel):
    """Request model for log_win tool"""

    win: str = Field(..., min_length=1, max_length=1000, description="Win description")
    impact: str = Field(
        default="medium",
        pattern=r"^(critical|high|medium|low)$",
        description="Impact level: critical, high, medium, or low",
    )

    @field_validator("win")
    @classmethod
    def win_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure win description is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Win description cannot be empty or whitespace only")
        return stripped


class CaptureIdeaRequest(BaseModel):
    """Request model for capture_idea tool"""

    idea: str = Field(..., min_length=1, max_length=2000, description="Idea description")

    @field_validator("idea")
    @classmethod
    def idea_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure idea is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Idea cannot be empty or whitespace only")
        return stripped


class UpdateFocusRequest(BaseModel):
    """Request model for update_focus tool"""

    focus: str = Field(..., min_length=1, max_length=500, description="Current focus description")

    @field_validator("focus")
    @classmethod
    def focus_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure focus is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Focus cannot be empty or whitespace only")
        return stripped


class LogProgressRequest(BaseModel):
    """Request model for log_progress tool"""

    project: str = Field(..., min_length=1, max_length=100, description="Project key")
    update: str = Field(..., min_length=1, max_length=1000, description="Progress update")

    @field_validator("update")
    @classmethod
    def update_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure update is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Progress update cannot be empty or whitespace only")
        return stripped


# ============================================================================
# COGNITIVE MODULE MODELS
# ============================================================================


class CheckForConflictRequest(BaseModel):
    """Request model for check_for_conflict tool"""

    statement: str = Field(
        ..., min_length=1, max_length=1000, description="Statement to check for conflicts"
    )

    @field_validator("statement")
    @classmethod
    def statement_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure statement is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Statement cannot be empty or whitespace only")
        return stripped


class AnalyzeProductivityRequest(BaseModel):
    """Request model for analyze_productivity tool"""

    days: int = Field(default=7, ge=1, le=365, description="Number of days to analyze")


# ============================================================================
# CONTEXT LOADING MODELS
# ============================================================================


class LoadContextRequest(BaseModel):
    """Request model for load_context tool"""

    query: str = Field(..., min_length=1, max_length=500, description="Context query")
    max_tokens: int = Field(default=2000, ge=100, le=100000, description="Maximum tokens to load")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query cannot be empty or whitespace only")
        return stripped


class GetLoadingPreviewRequest(BaseModel):
    """Request model for get_loading_preview tool"""

    query: str = Field(..., min_length=1, max_length=500, description="Preview query")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query cannot be empty or whitespace only")
        return stripped


class GetRecommendationsRequest(BaseModel):
    """Request model for get_recommendations tool"""

    query: Optional[str] = Field(
        default="",
        max_length=500,
        description="Recommendations query (optional for general recommendations)",
    )

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: Optional[str]) -> str:
        """Normalize optional query value."""
        if v is None:
            return ""
        stripped = v.strip()
        return stripped


class SearchFilesRequest(BaseModel):
    """Request model for search_files tool"""

    query: str = Field(..., min_length=1, max_length=200, description="File search query")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query cannot be empty or whitespace only")
        return stripped


# ============================================================================
# ADVANCED TOOL MODELS
# ============================================================================


class CreateSnapshotRequest(BaseModel):
    """Request model for create_snapshot tool"""

    name: str = Field(..., min_length=1, max_length=100, description="Snapshot name")

    @field_validator("name")
    @classmethod
    def name_must_be_valid_filename(cls, v: str) -> str:
        """Ensure name is valid for filesystem"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Snapshot name cannot be empty or whitespace only")

        # Check for invalid characters
        invalid_chars = set('<>:"/\\|?*')
        if any(char in stripped for char in invalid_chars):
            raise ValueError(
                f"Snapshot name contains invalid characters: {', '.join(invalid_chars)}"
            )

        return stripped


class SmartLoadRequest(BaseModel):
    """Request model for smart_load tool"""

    query: str = Field(..., min_length=1, max_length=500, description="Smart load query")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query cannot be empty or whitespace only")
        return stripped


# ============================================================================
# BRAIN & NEURAL WEB MODELS
# ============================================================================


class SemanticSearchRequest(BaseModel):
    """Request model for semantic_search tool"""

    query: str = Field(..., min_length=1, max_length=500, description="Semantic search query")
    limit: int = Field(default=5, ge=1, le=50, description="Maximum number of results")

    @field_validator("query")
    @classmethod
    def query_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure query is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Query cannot be empty or whitespace only")
        return stripped


class NeuralLearnRequest(BaseModel):
    """Request model for neural_learn tool"""

    text: str = Field(..., min_length=1, max_length=10000, description="Text to learn from")

    @field_validator("text")
    @classmethod
    def text_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure text is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Text cannot be empty or whitespace only")
        return stripped


class NeuralGetRelatedRequest(BaseModel):
    """Request model for neural_get_related tool"""

    concept: str = Field(..., min_length=1, max_length=200, description="Concept to find relations for")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of related concepts")

    @field_validator("concept")
    @classmethod
    def concept_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure concept is not just whitespace"""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Concept cannot be empty or whitespace only")
        return stripped


class NeuralGetPatternsRequest(BaseModel):
    """Request model for neural_get_patterns tool"""

    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of patterns")


class NeuralApplyDecayRequest(BaseModel):
    """Request model for neural_apply_decay tool"""

    days_threshold: int = Field(
        default=7, ge=1, le=365, description="Days threshold for decay application"
    )
