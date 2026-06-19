"""Additional edge-path tests for neural_web_typed.py."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from neural_web_typed import NeuralWeb, Synapse


def test_load_handles_corrupt_json(tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)
    (tmp_path / "neural_web.json").write_text("{not json}", encoding="utf-8")
    web.load()
    assert web.get_stats()["total_neurons"] == 0


def test_save_handles_json_dump_failure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)

    def fail_dump(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("dump failed")

    monkeypatch.setattr("json.dump", fail_dump)
    web.save()


def test_apply_decay_handles_invalid_timestamps(tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)
    s = Synapse("n_0000", "n_0001")
    s.last_activated = "not-a-date"
    web.synapses[(s.source_id, s.target_id)] = s
    web.apply_decay(days_threshold=1)
    assert len(web.synapses) == 1


def test_apply_decay_no_decay_path(tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)
    s = Synapse("n_0000", "n_0001")
    web.synapses[(s.source_id, s.target_id)] = s
    web.apply_decay(days_threshold=9999)
    assert len(web.synapses) == 1


def test_get_related_concepts_skips_missing_target(tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)
    src_id = web.get_or_create_neuron("python")
    missing_target = "n_9999"
    synapse = Synapse(src_id, missing_target)
    web.synapses[(src_id, missing_target)] = synapse

    related = web.get_related_concepts("python")
    assert related == []


def test_get_strongest_patterns_skips_missing_nodes(tmp_path: Path) -> None:
    web = NeuralWeb(tmp_path)
    src_id = web.get_or_create_neuron("python")
    synapse = Synapse(src_id, "n_9999")
    web.synapses[(src_id, "n_9999")] = synapse

    patterns = web.get_strongest_patterns(limit=10)
    assert patterns == []
