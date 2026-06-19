"""Tests for validation_models.py"""

import pytest
from pydantic import ValidationError

from validation_models import (
    AnalyzeProductivityRequest,
    ArchiveProjectRequest,
    CaptureIdeaRequest,
    CheckForConflictRequest,
    CreateProjectRequest,
    CreateSnapshotRequest,
    EndSessionRequest,
    GetLoadingPreviewRequest,
    GetProjectRequest,
    GetProjectStatsRequest,
    GetRecommendationsRequest,
    GetSessionHistoryRequest,
    ListProjectsRequest,
    LoadContextRequest,
    LogProgressRequest,
    LogSessionRequest,
    LogWinRequest,
    NeuralApplyDecayRequest,
    NeuralGetPatternsRequest,
    NeuralGetRelatedRequest,
    NeuralLearnRequest,
    SearchFilesRequest,
    SearchSessionsRequest,
    SemanticSearchRequest,
    SetActiveProjectRequest,
    SmartLoadRequest,
    UpdateFocusRequest,
    UpdateProjectRequest,
    UpdateStateRequest,
)


class TestCreateProjectRequest:
    """Tests for CreateProjectRequest validation"""

    def test_valid_project_creation(self) -> None:
        """Test valid project creation request"""
        req = CreateProjectRequest(
            key="my-project", name="My Project", description="A test project"
        )

        assert req.key == "my-project"
        assert req.name == "My Project"
        assert req.description == "A test project"

    def test_valid_project_with_underscore(self) -> None:
        """Test valid project key with underscore (not at start)"""
        req = CreateProjectRequest(key="my_project", name="My Project")

        assert req.key == "my_project"

    def test_invalid_key_with_spaces(self) -> None:
        """Test invalid project key with spaces"""
        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key="my project", name="My Project")

        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)

    def test_invalid_key_with_uppercase(self) -> None:
        """Test invalid project key with uppercase letters"""
        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key="MyProject", name="My Project")

        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)

    def test_invalid_key_starts_with_underscore(self) -> None:
        """Test invalid project key starting with underscore"""
        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key="_private", name="My Project")

        errors = exc_info.value.errors()
        assert any("underscore" in str(e).lower() for e in errors)

    def test_invalid_key_starts_with_dash(self) -> None:
        """Test invalid project key starting with dash"""
        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key="-project", name="My Project")

        errors = exc_info.value.errors()
        assert any("dash" in str(e).lower() for e in errors)

    def test_invalid_empty_name(self) -> None:
        """Test invalid empty project name"""
        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key="project", name="   ")

        errors = exc_info.value.errors()
        assert any("whitespace" in str(e).lower() for e in errors)

    def test_key_too_long(self) -> None:
        """Test project key that's too long"""
        long_key = "a" * 101

        with pytest.raises(ValidationError) as exc_info:
            CreateProjectRequest(key=long_key, name="My Project")

        errors = exc_info.value.errors()
        assert any("max_length" in str(e).lower() for e in errors)


class TestUpdateProjectRequest:
    """Tests for UpdateProjectRequest validation"""

    def test_valid_update_completion(self) -> None:
        """Test valid project update with completion"""
        req = UpdateProjectRequest(project="my-project", updates={"completion": 75})

        assert req.project == "my-project"
        assert req.updates["completion"] == 75

    def test_valid_update_status(self) -> None:
        """Test valid project update with status"""
        req = UpdateProjectRequest(project="my-project", updates={"status": "active"})

        assert req.updates["status"] == "active"

    def test_valid_update_priority(self) -> None:
        """Test valid project update with priority"""
        req = UpdateProjectRequest(project="my-project", updates={"priority": "high"})

        assert req.updates["priority"] == "high"

    def test_invalid_empty_updates(self) -> None:
        """Test invalid empty updates dictionary"""
        with pytest.raises(ValidationError) as exc_info:
            UpdateProjectRequest(project="my-project", updates={})

        errors = exc_info.value.errors()
        assert any("empty" in str(e).lower() for e in errors)

    def test_invalid_completion_range(self) -> None:
        """Test invalid completion value out of range"""
        with pytest.raises(ValidationError) as exc_info:
            UpdateProjectRequest(project="my-project", updates={"completion": 150})

        errors = exc_info.value.errors()
        assert any("between" in str(e).lower() for e in errors)

    def test_invalid_status_value(self) -> None:
        """Test invalid status value"""
        with pytest.raises(ValidationError) as exc_info:
            UpdateProjectRequest(project="my-project", updates={"status": "invalid"})

        errors = exc_info.value.errors()
        assert any("invalid status" in str(e).lower() for e in errors)

    def test_invalid_priority_value(self) -> None:
        """Test invalid priority value"""
        with pytest.raises(ValidationError) as exc_info:
            UpdateProjectRequest(project="my-project", updates={"priority": "super-high"})

        errors = exc_info.value.errors()
        assert any("invalid priority" in str(e).lower() for e in errors)

    def test_invalid_update_field(self) -> None:
        """Test invalid update field"""
        with pytest.raises(ValidationError) as exc_info:
            UpdateProjectRequest(project="my-project", updates={"invalid_field": "value"})

        errors = exc_info.value.errors()
        assert any("invalid update fields" in str(e).lower() for e in errors)


class TestLogSessionRequest:
    """Tests for LogSessionRequest validation"""

    def test_valid_session_log(self) -> None:
        """Test valid session log request"""
        req = LogSessionRequest(
            summary="Completed feature X", achievements=["Added tests", "Fixed bug"]
        )

        assert req.summary == "Completed feature X"
        assert len(req.achievements) == 2

    def test_valid_session_without_achievements(self) -> None:
        """Test valid session log without achievements"""
        req = LogSessionRequest(summary="Daily standup")

        assert req.summary == "Daily standup"
        assert req.achievements == []

    def test_invalid_empty_summary(self) -> None:
        """Test invalid empty summary"""
        with pytest.raises(ValidationError) as exc_info:
            LogSessionRequest(summary="   ")

        errors = exc_info.value.errors()
        assert any("whitespace" in str(e).lower() for e in errors)

    def test_invalid_too_many_achievements(self) -> None:
        """Test invalid too many achievements"""
        achievements = [f"Achievement {i}" for i in range(51)]

        with pytest.raises(ValidationError) as exc_info:
            LogSessionRequest(summary="Test", achievements=achievements)

        errors = exc_info.value.errors()
        assert any("50" in str(e) for e in errors)

    def test_achievements_strips_whitespace(self) -> None:
        """Test that achievements are stripped of whitespace"""
        req = LogSessionRequest(
            summary="Test", achievements=["  Achievement 1  ", "Achievement 2", "   ", ""]
        )

        # Should strip whitespace and filter empty strings
        assert len(req.achievements) == 2


class TestSemanticSearchRequest:
    """Tests for SemanticSearchRequest validation"""

    def test_valid_semantic_search(self) -> None:
        """Test valid semantic search request"""
        req = SemanticSearchRequest(query="machine learning", limit=10)

        assert req.query == "machine learning"
        assert req.limit == 10

    def test_valid_semantic_search_default_limit(self) -> None:
        """Test valid semantic search with default limit"""
        req = SemanticSearchRequest(query="neural networks")

        assert req.query == "neural networks"
        assert req.limit == 5

    def test_invalid_empty_query(self) -> None:
        """Test invalid empty query"""
        with pytest.raises(ValidationError) as exc_info:
            SemanticSearchRequest(query="   ")

        errors = exc_info.value.errors()
        assert any("whitespace" in str(e).lower() for e in errors)

    def test_invalid_limit_too_large(self) -> None:
        """Test invalid limit that's too large"""
        with pytest.raises(ValidationError) as exc_info:
            SemanticSearchRequest(query="test", limit=100)

        errors = exc_info.value.errors()
        assert any("less than or equal to" in str(e).lower() for e in errors)

    def test_invalid_limit_too_small(self) -> None:
        """Test invalid limit that's too small"""
        with pytest.raises(ValidationError) as exc_info:
            SemanticSearchRequest(query="test", limit=0)

        errors = exc_info.value.errors()
        assert any("greater than or equal to" in str(e).lower() for e in errors)


class TestListProjectsRequest:
    """Tests for ListProjectsRequest validation"""

    def test_valid_filter_active(self) -> None:
        """Test valid filter for active projects"""
        req = ListProjectsRequest(filter="active")

        assert req.filter == "active"

    def test_valid_no_filter(self) -> None:
        """Test valid request without filter"""
        req = ListProjectsRequest()

        assert req.filter is None

    def test_valid_filter_blocked(self) -> None:
        """Test valid filter for blocked projects"""
        req = ListProjectsRequest(filter="blocked")

        assert req.filter == "blocked"

    def test_invalid_filter_value(self) -> None:
        """Test invalid filter value"""
        with pytest.raises(ValidationError) as exc_info:
            ListProjectsRequest(filter="invalid")

        errors = exc_info.value.errors()
        assert any("pattern" in str(e).lower() for e in errors)


class TestCreateSnapshotRequest:
    """Tests for CreateSnapshotRequest validation"""

    def test_valid_snapshot_name(self) -> None:
        """Test valid snapshot name"""
        req = CreateSnapshotRequest(name="backup-2026-02-17")

        assert req.name == "backup-2026-02-17"

    def test_invalid_snapshot_with_colon(self) -> None:
        """Test invalid snapshot name with colon"""
        with pytest.raises(ValidationError) as exc_info:
            CreateSnapshotRequest(name="backup:2026")

        errors = exc_info.value.errors()
        assert any("invalid characters" in str(e).lower() for e in errors)

    def test_invalid_snapshot_with_slash(self) -> None:
        """Test invalid snapshot name with slash"""
        with pytest.raises(ValidationError) as exc_info:
            CreateSnapshotRequest(name="backup/2026")

        errors = exc_info.value.errors()
        assert any("invalid characters" in str(e).lower() for e in errors)


class TestGetSessionHistoryRequest:
    """Tests for GetSessionHistoryRequest validation"""

    def test_valid_session_history_count(self) -> None:
        """Test valid session history count"""
        req = GetSessionHistoryRequest(count=10)

        assert req.count == 10

    def test_valid_session_history_default(self) -> None:
        """Test valid session history with default count"""
        req = GetSessionHistoryRequest()

        assert req.count == 5

    def test_invalid_count_too_large(self) -> None:
        """Test invalid count that's too large"""
        with pytest.raises(ValidationError) as exc_info:
            GetSessionHistoryRequest(count=101)

        errors = exc_info.value.errors()
        assert any("less than or equal to" in str(e).lower() for e in errors)

    def test_invalid_count_zero(self) -> None:
        """Test invalid count of zero"""
        with pytest.raises(ValidationError) as exc_info:
            GetSessionHistoryRequest(count=0)

        errors = exc_info.value.errors()
        assert any("greater than or equal to" in str(e).lower() for e in errors)


class TestLoadContextRequest:
    """Tests for LoadContextRequest validation"""

    def test_valid_load_context(self) -> None:
        """Test valid load context request"""
        req = LoadContextRequest(query="neural networks", max_tokens=5000)

        assert req.query == "neural networks"
        assert req.max_tokens == 5000

    def test_valid_load_context_default_tokens(self) -> None:
        """Test valid load context with default max_tokens"""
        req = LoadContextRequest(query="machine learning")

        assert req.query == "machine learning"
        assert req.max_tokens == 2000

    def test_invalid_max_tokens_too_large(self) -> None:
        """Test invalid max_tokens that's too large"""
        with pytest.raises(ValidationError) as exc_info:
            LoadContextRequest(query="test", max_tokens=200000)

        errors = exc_info.value.errors()
        assert any("less than or equal to" in str(e).lower() for e in errors)


class TestAdditionalValidationModels:
    """Additional model coverage for less frequently used requests."""

    def test_update_state_rejects_empty_updates(self) -> None:
        with pytest.raises(ValidationError):
            UpdateStateRequest(updates={})

    def test_update_project_completion_must_be_numeric(self) -> None:
        with pytest.raises(ValidationError):
            UpdateProjectRequest(project="demo", updates={"completion": "fifty"})

    def test_get_project_related_models_validate(self) -> None:
        assert GetProjectRequest(project="demo").project == "demo"
        assert SetActiveProjectRequest(project="demo").project == "demo"
        assert ArchiveProjectRequest(project="demo").project == "demo"
        assert GetProjectStatsRequest(project="demo").project == "demo"

    def test_end_session_summary_validation(self) -> None:
        assert EndSessionRequest(summary=None).summary is None
        with pytest.raises(ValidationError):
            EndSessionRequest(summary="   ")

    def test_search_sessions_validation(self) -> None:
        assert SearchSessionsRequest(query="auth").query == "auth"
        with pytest.raises(ValidationError):
            SearchSessionsRequest(query="   ")

    def test_progress_model_whitespace_validation(self) -> None:
        with pytest.raises(ValidationError):
            LogWinRequest(win="   ")
        with pytest.raises(ValidationError):
            CaptureIdeaRequest(idea="   ")
        with pytest.raises(ValidationError):
            UpdateFocusRequest(focus="   ")
        with pytest.raises(ValidationError):
            LogProgressRequest(project="demo", update="   ")

    def test_check_conflict_and_productivity_validation(self) -> None:
        assert CheckForConflictRequest(statement="Use OAuth2").statement == "Use OAuth2"
        with pytest.raises(ValidationError):
            CheckForConflictRequest(statement="   ")

        assert AnalyzeProductivityRequest(days=14).days == 14
        with pytest.raises(ValidationError):
            AnalyzeProductivityRequest(days=0)
        with pytest.raises(ValidationError):
            AnalyzeProductivityRequest(days=366)

    def test_context_related_models_validation(self) -> None:
        assert GetLoadingPreviewRequest(query="deploy").query == "deploy"
        with pytest.raises(ValidationError):
            GetLoadingPreviewRequest(query="   ")

        rec = GetRecommendationsRequest(query="  auth  ")
        assert rec.query == "auth"
        assert GetRecommendationsRequest().query == ""
        assert GetRecommendationsRequest(query=None).query == ""

        assert SearchFilesRequest(query="README").query == "README"
        with pytest.raises(ValidationError):
            SearchFilesRequest(query="   ")

        assert SmartLoadRequest(query="state").query == "state"
        with pytest.raises(ValidationError):
            SmartLoadRequest(query="   ")

    def test_neural_models_validation(self) -> None:
        with pytest.raises(ValidationError):
            NeuralLearnRequest(text="   ")

        assert NeuralGetRelatedRequest(concept="python", limit=5).limit == 5
        with pytest.raises(ValidationError):
            NeuralGetRelatedRequest(concept="   ", limit=5)
        with pytest.raises(ValidationError):
            NeuralGetRelatedRequest(concept="python", limit=101)

        assert NeuralGetPatternsRequest(limit=10).limit == 10
        with pytest.raises(ValidationError):
            NeuralGetPatternsRequest(limit=0)

        assert NeuralApplyDecayRequest(days_threshold=7).days_threshold == 7
        with pytest.raises(ValidationError):
            NeuralApplyDecayRequest(days_threshold=0)

    def test_long_achievement_rejected(self) -> None:
        with pytest.raises(ValidationError):
            LogSessionRequest(summary="x", achievements=["a" * 501])

    def test_achievement_validator_direct_length_guard(self) -> None:
        with pytest.raises(ValueError):
            LogSessionRequest.achievements_must_be_valid(["a"] * 51)

    def test_load_context_rejects_whitespace_query(self) -> None:
        with pytest.raises(ValidationError):
            LoadContextRequest(query="   ")

    def test_snapshot_name_rejects_whitespace_only(self) -> None:
        with pytest.raises(ValidationError):
            CreateSnapshotRequest(name="   ")
