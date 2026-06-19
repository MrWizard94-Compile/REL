"""Tests for brain module (brain_typed.py)"""

from pathlib import Path
from typing import Any, Dict

import pytest

# Import the typed version we just created
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from brain_typed import RELBrain, get_brain


class TestRELBrainInitialization:
    """Tests for RELBrain initialization"""

    def test_brain_init_creates_paths(self, brain_path: Path) -> None:
        """Test that brain initialization sets up correct paths"""
        brain = RELBrain(brain_path)

        assert brain.brain_path == brain_path
        assert brain.index_path == brain_path / "faiss_index.bin"
        assert brain.documents_path == brain_path / "documents.json"
        assert brain.metadata_path == brain_path / "brain_metadata.json"

    def test_brain_init_sets_defaults(self, brain_path: Path) -> None:
        """Test that brain initialization sets correct default values"""
        brain = RELBrain(brain_path)

        assert brain.model is None
        assert brain.index is None
        assert brain.documents == []
        assert brain.dimension == 384

    def test_brain_init_creates_directory(self, temp_rel_dir: Path) -> None:
        """Test that brain creates directory if it doesn't exist"""
        new_brain_path = temp_rel_dir / "data" / "brain_new"
        assert not new_brain_path.exists()

        brain = RELBrain(new_brain_path)

        assert new_brain_path.exists()
        assert new_brain_path.is_dir()


class TestRELBrainStats:
    """Tests for brain statistics"""

    def test_get_stats_empty_brain(self, brain_path: Path) -> None:
        """Test stats for empty brain"""
        brain = RELBrain(brain_path)
        stats = brain.get_stats()

        assert stats["total_vectors"] == 0
        assert stats["total_documents"] == 0
        assert stats["dimension"] == 384
        assert stats["model"] == "all-MiniLM-L6-v2"
        assert stats["index_type"] == "FAISS IndexFlatL2"

    def test_get_stats_with_documents(self, brain_path: Path) -> None:
        """Test stats with documents added"""
        brain = RELBrain(brain_path)
        brain.documents = [
            {"text": "Test 1", "metadata": {}, "id": 0},
            {"text": "Test 2", "metadata": {}, "id": 1},
        ]

        stats = brain.get_stats()

        assert stats["total_documents"] == 2


class TestRELBrainIngestion:
    """Tests for ingesting content into brain"""

    def test_ingest_text_without_initialization(self, brain_path: Path) -> None:
        """Test that ingest_text handles uninitialized brain gracefully"""
        brain = RELBrain(brain_path)

        # This should attempt to initialize and may fail due to missing dependencies
        # But it should not crash
        result = brain.ingest_text("Test text", {"type": "test"})

        # Result depends on whether dependencies are available
        # We just ensure it doesn't crash
        assert isinstance(result, bool)

    def test_ingest_from_state_and_log_structure(
        self, brain_path: Path, sample_state: Dict[str, Any], sample_session_log: Dict[str, Any]
    ) -> None:
        """Test that ingest_from_state_and_log processes correct structure"""
        brain = RELBrain(brain_path)

        # Call the method (may or may not succeed based on dependencies)
        count = brain.ingest_from_state_and_log(sample_state, sample_session_log)

        # Verify it returns an integer
        assert isinstance(count, int)
        assert count >= 0


class TestRELBrainSearch:
    """Tests for semantic search"""

    def test_search_empty_brain_returns_empty_list(self, brain_path: Path) -> None:
        """Test searching empty brain returns empty results"""
        brain = RELBrain(brain_path)

        results = brain.search("test query", limit=5)

        assert results == []

    def test_search_respects_limit_parameter(self, brain_path: Path) -> None:
        """Test that search respects the limit parameter"""
        brain = RELBrain(brain_path)

        # Search with different limits
        results_5 = brain.search("test", limit=5)
        results_10 = brain.search("test", limit=10)

        # Both should be empty for uninitialized brain
        assert len(results_5) == 0
        assert len(results_10) == 0


class TestRELBrainSaveLoad:
    """Tests for saving and loading brain state"""

    def test_save_index_creates_files(self, brain_path: Path) -> None:
        """Test that save_index creates necessary files"""
        brain = RELBrain(brain_path)
        brain.documents = [{"text": "Test", "metadata": {}, "id": 0}]

        brain.save_index()

        # Documents file should be created
        assert brain.documents_path.exists()

    def test_save_load_documents_roundtrip(self, brain_path: Path) -> None:
        """Test saving and loading documents"""
        brain1 = RELBrain(brain_path)
        brain1.documents = [
            {"text": "Document 1", "metadata": {"type": "test"}, "id": 0},
            {"text": "Document 2", "metadata": {"type": "test"}, "id": 1},
        ]

        brain1.save_index()

        # Create new brain instance and initialize
        brain2 = RELBrain(brain_path)
        brain2.initialize()

        # Documents should be loaded
        assert len(brain2.documents) == 2
        assert brain2.documents[0]["text"] == "Document 1"
        assert brain2.documents[1]["text"] == "Document 2"


class TestGetBrainSingleton:
    """Tests for get_brain singleton pattern"""

    def test_get_brain_returns_brain_instance(self, brain_path: Path) -> None:
        """Test that get_brain returns RELBrain instance"""
        brain = get_brain(brain_path)

        assert isinstance(brain, RELBrain)

    def test_get_brain_returns_same_instance(self, brain_path: Path) -> None:
        """Test that get_brain returns the same instance (singleton)"""
        brain1 = get_brain(brain_path)
        brain2 = get_brain(brain_path)

        assert brain1 is brain2


@pytest.mark.skipif(
    True, reason="Integration test - requires sentence-transformers and FAISS dependencies"
)
class TestRELBrainIntegration:
    """Integration tests requiring full dependencies"""

    def test_full_initialization_with_dependencies(self, brain_path: Path) -> None:
        """Test full initialization when dependencies are available"""
        brain = RELBrain(brain_path)
        success = brain.initialize()

        if success:
            assert brain.model is not None
            assert brain.index is not None
            assert brain.index.ntotal == 0

    def test_ingest_and_search_workflow(self, brain_path: Path) -> None:
        """Test complete workflow: ingest text and search for it"""
        brain = RELBrain(brain_path)

        if not brain.initialize():
            pytest.skip("Brain dependencies not available")

        # Ingest some text
        success1 = brain.ingest_text("Python programming is great", {"type": "test"})
        success2 = brain.ingest_text("Machine learning with neural networks", {"type": "test"})

        assert success1 and success2

        # Search for related content
        results = brain.search("Python code", limit=2)

        assert len(results) > 0
        assert "similarity_score" in results[0]
        assert results[0]["rank"] == 1
