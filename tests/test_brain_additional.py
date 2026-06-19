"""Additional unit tests for brain_typed.py edge paths."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import pytest

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
import brain_typed as bt


class FakeModel:
    def encode(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2, 0.3] for _ in texts]


class FakeIndex:
    def __init__(self) -> None:
        self.ntotal = 0

    def add(self, arr: List[Any]) -> None:
        self.ntotal += len(arr)

    def search(self, query_array: List[Any], k: int) -> Any:
        distances = [[0.1 for _ in range(k)]]
        indices = [[i for i in range(k)]]
        return distances, indices


class FakeNumpy:
    @staticmethod
    def array(values: List[Any], dtype: str = "float32") -> List[Any]:
        return values


class FakeFaiss:
    def __init__(self) -> None:
        self.saved = False

    def IndexFlatL2(self, dimension: int) -> FakeIndex:
        return FakeIndex()

    def read_index(self, path: str) -> FakeIndex:
        idx = FakeIndex()
        idx.ntotal = 1
        return idx

    def write_index(self, index: FakeIndex, path: str) -> None:
        self.saved = True


def test_get_sentence_transformer_returns_none_when_dependency_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(bt, "_sentence_transformer", None)
    monkeypatch.setattr(bt, "SentenceTransformer", None)

    assert bt.get_sentence_transformer() is None


def test_get_sentence_transformer_handles_constructor_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class BrokenTransformer:
        def __init__(self, _: str) -> None:
            raise RuntimeError("boom")

    monkeypatch.setattr(bt, "_sentence_transformer", None)
    monkeypatch.setattr(bt, "SentenceTransformer", BrokenTransformer)

    assert bt.get_sentence_transformer() is None


def test_initialize_loads_existing_index_and_documents(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.index_path.write_bytes(b"index")
    brain.documents_path.write_text('[{"text": "saved", "metadata": {}, "id": 0}]', encoding="utf-8")

    monkeypatch.setattr(bt, "get_sentence_transformer", lambda: FakeModel())
    monkeypatch.setattr(bt, "get_faiss", lambda: FakeFaiss())
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())

    assert brain.initialize() is True
    assert brain.index is not None
    assert len(brain.documents) == 1


def test_initialize_fails_when_faiss_or_numpy_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)

    monkeypatch.setattr(bt, "get_sentence_transformer", lambda: FakeModel())
    monkeypatch.setattr(bt, "get_faiss", lambda: None)
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())

    assert brain.initialize() is False


def test_initialize_fails_when_model_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)
    monkeypatch.setattr(bt, "get_sentence_transformer", lambda: None)
    assert brain.initialize() is False


def test_initialize_handles_unexpected_exceptions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    monkeypatch.setattr(bt, "get_sentence_transformer", lambda: FakeModel())

    def explode() -> Any:
        raise RuntimeError("unexpected")

    monkeypatch.setattr(bt, "get_faiss", explode)
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())
    assert brain.initialize() is False


def test_ingest_text_triggers_periodic_save(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = FakeIndex()
    brain.documents = [{"text": f"doc-{i}", "metadata": {}, "id": i} for i in range(9)]

    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())

    saved = {"called": False}

    def mark_saved() -> None:
        saved["called"] = True

    monkeypatch.setattr(brain, "save_index", mark_saved)

    assert brain.ingest_text("new text", {"type": "test"}) is True
    assert saved["called"] is True
    assert len(brain.documents) == 10


def test_ingest_text_returns_false_when_initialize_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    monkeypatch.setattr(brain, "initialize", lambda: False)
    assert brain.ingest_text("x", {"type": "t"}) is False


def test_ingest_text_handles_encoding_exception(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class BrokenModel:
        def encode(self, texts: List[str]) -> List[List[float]]:
            raise RuntimeError("encode failed")

    brain = bt.RELBrain(tmp_path)
    brain.model = BrokenModel()
    brain.index = FakeIndex()
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())
    assert brain.ingest_text("x", {"type": "t"}) is False


def test_ingest_text_returns_false_when_numpy_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = FakeIndex()
    monkeypatch.setattr(bt, "get_numpy", lambda: None)
    assert brain.ingest_text("x", {"type": "t"}) is False


def test_search_returns_ranked_results(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = FakeIndex()
    brain.index.ntotal = 2
    brain.documents = [
        {"text": "doc1", "metadata": {"a": 1}, "id": 0},
        {"text": "doc2", "metadata": {"a": 2}, "id": 1},
    ]

    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())

    results = brain.search("query", limit=2)

    assert len(results) == 2
    assert results[0]["rank"] == 1
    assert "similarity_score" in results[0]


def test_search_returns_empty_on_empty_index(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = FakeIndex()
    brain.documents = []
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())
    assert brain.search("query", limit=1) == []


def test_search_returns_empty_when_initialize_fails(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    monkeypatch.setattr(brain, "initialize", lambda: False)
    assert brain.search("query", limit=1) == []


def test_search_returns_empty_when_numpy_missing(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = FakeIndex()
    brain.index.ntotal = 1
    brain.documents = [{"text": "doc", "metadata": {}, "id": 0}]
    monkeypatch.setattr(bt, "get_numpy", lambda: None)
    assert brain.search("query", limit=1) == []


def test_search_skips_invalid_document_indices(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class OutOfRangeIndex(FakeIndex):
        def search(self, query_array: List[Any], k: int) -> Any:
            return [[0.1]], [[99]]

    brain = bt.RELBrain(tmp_path)
    brain.model = FakeModel()
    brain.index = OutOfRangeIndex()
    brain.index.ntotal = 1
    brain.documents = [{"text": "doc", "metadata": {}, "id": 0}]
    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())
    assert brain.search("query", limit=1) == []


def test_search_handles_model_errors(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class BrokenModel:
        def encode(self, _: List[str]) -> List[List[float]]:
            raise RuntimeError("encode failed")

    brain = bt.RELBrain(tmp_path)
    brain.model = BrokenModel()
    brain.index = FakeIndex()
    brain.index.ntotal = 1
    brain.documents = [{"text": "doc", "metadata": {}, "id": 0}]

    monkeypatch.setattr(bt, "get_numpy", lambda: FakeNumpy())

    assert brain.search("query", limit=1) == []


def test_ingest_from_state_and_log_counts_items(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)

    monkeypatch.setattr(brain, "ingest_text", lambda text, metadata: True)
    monkeypatch.setattr(brain, "save_index", lambda: None)

    state: Dict[str, Any] = {
        "recent_wins": [{"win": "done", "date": "2026-01-01", "impact": "high"}],
        "active_ideas": ["idea one"],
        "project_states": {
            "proj": {"name": "Project", "description": "desc", "status": "active", "completion": 10}
        },
    }
    log: Dict[str, Any] = {
        "sessions": [
            {
                "session": 1,
                "summary": "summary",
                "date": "2026-01-01",
                "achievements": ["ach1", "ach2"],
            }
        ]
    }

    # wins(1) + ideas(1) + sessions(1) + achievements(2) + projects(1)
    assert brain.ingest_from_state_and_log(state, log) == 6


def test_ingest_from_state_and_log_handles_false_ingestions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    monkeypatch.setattr(brain, "ingest_text", lambda text, metadata: False)
    monkeypatch.setattr(brain, "save_index", lambda: None)
    state: Dict[str, Any] = {"recent_wins": [{"win": "x"}], "active_ideas": ["i"], "project_states": {}}
    log: Dict[str, Any] = {"sessions": [{"session": 1, "summary": "s", "achievements": []}]}
    assert brain.ingest_from_state_and_log(state, log) == 0


def test_ingest_from_state_and_log_mixed_success_paths(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)
    call_count = {"n": 0}

    def mixed_result(text: str, metadata: Dict[str, Any]) -> bool:
        call_count["n"] += 1
        return call_count["n"] % 2 == 1

    monkeypatch.setattr(brain, "ingest_text", mixed_result)
    monkeypatch.setattr(brain, "save_index", lambda: None)
    state: Dict[str, Any] = {
        "recent_wins": [{"win": "w"}],
        "active_ideas": ["i"],
        "project_states": {"p": {"name": "n", "description": "d", "status": "active", "completion": 0}},
    }
    log: Dict[str, Any] = {"sessions": [{"session": 1, "summary": "s", "date": "2026-01-01", "achievements": ["a"]}]}
    result = brain.ingest_from_state_and_log(state, log)
    assert result >= 1


def test_ingest_from_state_and_log_handles_exceptions(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    brain = bt.RELBrain(tmp_path)

    def explode(text: str, metadata: Dict[str, Any]) -> bool:
        raise RuntimeError("boom")

    monkeypatch.setattr(brain, "ingest_text", explode)
    state: Dict[str, Any] = {"recent_wins": [{"win": "x"}], "active_ideas": [], "project_states": {}}
    log: Dict[str, Any] = {"sessions": []}
    assert brain.ingest_from_state_and_log(state, log) == 0


def test_save_index_handles_write_exceptions(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    class BrokenFaiss(FakeFaiss):
        def write_index(self, index: FakeIndex, path: str) -> None:
            raise RuntimeError("write failed")

    brain = bt.RELBrain(tmp_path)
    brain.index = FakeIndex()
    brain.documents = [{"text": "x", "metadata": {}, "id": 0}]

    monkeypatch.setattr(bt, "get_faiss", lambda: BrokenFaiss())

    # Should be swallowed by method exception handling.
    brain.save_index()


def test_save_index_with_no_documents(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    brain = bt.RELBrain(tmp_path)
    brain.index = FakeIndex()
    brain.documents = []
    monkeypatch.setattr(bt, "get_faiss", lambda: FakeFaiss())
    brain.save_index()
