"""Tests for neural_web_typed.py"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest

# Import the typed version
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from neural_web_typed import Neuron, NeuralWeb, Synapse, get_neural_web


class TestNeuron:
    """Tests for Neuron class"""

    def test_neuron_initialization(self) -> None:
        """Test neuron initialization with defaults"""
        neuron = Neuron("n_0001", "python")

        assert neuron.id == "n_0001"
        assert neuron.concept == "python"
        assert neuron.activation_count == 0
        assert isinstance(neuron.last_activated, str)
        assert isinstance(neuron.created, str)
        assert neuron.tags == set()

    def test_neuron_initialization_with_created_date(self) -> None:
        """Test neuron initialization with custom created date"""
        created_date = "2026-01-01T00:00:00"
        neuron = Neuron("n_0001", "python", created=created_date)

        assert neuron.created == created_date
        assert neuron.last_activated == created_date

    def test_neuron_activate(self) -> None:
        """Test neuron activation"""
        neuron = Neuron("n_0001", "python")
        initial_count = neuron.activation_count
        initial_activated = neuron.last_activated

        neuron.activate()

        assert neuron.activation_count == initial_count + 1
        assert neuron.last_activated >= initial_activated

    def test_neuron_multiple_activations(self) -> None:
        """Test multiple neuron activations"""
        neuron = Neuron("n_0001", "python")

        for i in range(5):
            neuron.activate()

        assert neuron.activation_count == 5

    def test_neuron_to_dict(self) -> None:
        """Test neuron serialization to dictionary"""
        neuron = Neuron("n_0001", "python")
        neuron.activate()
        neuron.tags.add("programming")

        result = neuron.to_dict()

        assert result["id"] == "n_0001"
        assert result["concept"] == "python"
        assert result["activation_count"] == 1
        assert "programming" in result["tags"]

    def test_neuron_from_dict(self) -> None:
        """Test neuron deserialization from dictionary"""
        data = {
            "id": "n_0001",
            "concept": "python",
            "activation_count": 5,
            "last_activated": "2026-01-01T00:00:00",
            "created": "2026-01-01T00:00:00",
            "tags": ["programming", "language"],
        }

        neuron = Neuron.from_dict(data)

        assert neuron.id == "n_0001"
        assert neuron.concept == "python"
        assert neuron.activation_count == 5
        assert "programming" in neuron.tags
        assert "language" in neuron.tags

    def test_neuron_roundtrip(self) -> None:
        """Test neuron serialization and deserialization roundtrip"""
        original = Neuron("n_0001", "python")
        original.activate()
        original.activate()
        original.tags.add("test")

        data = original.to_dict()
        restored = Neuron.from_dict(data)

        assert restored.id == original.id
        assert restored.concept == original.concept
        assert restored.activation_count == original.activation_count
        assert restored.tags == original.tags


class TestSynapse:
    """Tests for Synapse class"""

    def test_synapse_initialization(self) -> None:
        """Test synapse initialization"""
        synapse = Synapse("n_0001", "n_0002")

        assert synapse.source_id == "n_0001"
        assert synapse.target_id == "n_0002"
        assert synapse.weight == 0.1
        assert synapse.frequency == 0
        assert isinstance(synapse.last_activated, str)
        assert isinstance(synapse.created, str)

    def test_synapse_strengthen(self) -> None:
        """Test synapse strengthening"""
        synapse = Synapse("n_0001", "n_0002")
        initial_weight = synapse.weight
        initial_frequency = synapse.frequency

        synapse.strengthen()

        assert synapse.weight > initial_weight
        assert synapse.frequency == initial_frequency + 1

    def test_synapse_strengthen_with_amount(self) -> None:
        """Test synapse strengthening with custom amount"""
        synapse = Synapse("n_0001", "n_0002")

        synapse.strengthen(amount=0.5)

        assert synapse.weight == 0.6  # 0.1 initial + 0.5

    def test_synapse_strengthen_max_weight(self) -> None:
        """Test synapse cannot exceed weight of 1.0"""
        synapse = Synapse("n_0001", "n_0002")

        for _ in range(20):  # Strengthen many times
            synapse.strengthen()

        assert synapse.weight <= 1.0
        assert synapse.weight == 1.0  # Should be capped at max

    def test_synapse_decay(self) -> None:
        """Test synapse decay"""
        synapse = Synapse("n_0001", "n_0002")
        synapse.weight = 0.5

        synapse.decay()

        assert synapse.weight < 0.5

    def test_synapse_decay_min_weight(self) -> None:
        """Test synapse cannot decay below 0.0"""
        synapse = Synapse("n_0001", "n_0002")
        synapse.weight = 0.05

        for _ in range(10):  # Decay many times
            synapse.decay()

        assert synapse.weight >= 0.0
        assert synapse.weight == 0.0  # Should be at minimum

    def test_synapse_to_dict(self) -> None:
        """Test synapse serialization to dictionary"""
        synapse = Synapse("n_0001", "n_0002")
        synapse.strengthen()

        result = synapse.to_dict()

        assert result["source_id"] == "n_0001"
        assert result["target_id"] == "n_0002"
        assert result["weight"] > 0.1
        assert result["frequency"] == 1

    def test_synapse_from_dict(self) -> None:
        """Test synapse deserialization from dictionary"""
        data = {
            "source_id": "n_0001",
            "target_id": "n_0002",
            "weight": 0.75,
            "frequency": 10,
            "last_activated": "2026-01-01T00:00:00",
            "created": "2026-01-01T00:00:00",
        }

        synapse = Synapse.from_dict(data)

        assert synapse.source_id == "n_0001"
        assert synapse.target_id == "n_0002"
        assert synapse.weight == 0.75
        assert synapse.frequency == 10


class TestNeuralWebInitialization:
    """Tests for NeuralWeb initialization"""

    def test_neural_web_init_creates_directory(self, neural_web_path: Path) -> None:
        """Test neural web creates directory"""
        assert neural_web_path.exists()

        neural_web = NeuralWeb(neural_web_path)

        assert neural_web.web_path == neural_web_path
        assert len(neural_web.neurons) == 0
        assert len(neural_web.synapses) == 0
        assert len(neural_web.concept_to_neuron) == 0

    def test_neural_web_creates_directory_if_not_exists(self, temp_rel_dir: Path) -> None:
        """Test neural web creates directory if it doesn't exist"""
        new_path = temp_rel_dir / "data" / "new_neural_web"
        assert not new_path.exists()

        neural_web = NeuralWeb(new_path)

        assert new_path.exists()
        assert new_path.is_dir()


class TestNeuralWebConceptExtraction:
    """Tests for concept extraction"""

    def test_extract_concepts_from_simple_text(self, neural_web_path: Path) -> None:
        """Test extracting concepts from simple text"""
        neural_web = NeuralWeb(neural_web_path)

        concepts = neural_web.extract_concepts("Python programming is great for machine learning")

        # Should extract words and filter stop words
        assert "python" in concepts or "programming" in concepts
        assert "machine" in concepts or "learning" in concepts
        # Stop words should be removed
        assert "is" not in concepts
        assert "for" not in concepts

    def test_extract_concepts_filters_short_words(self, neural_web_path: Path) -> None:
        """Test that short words are filtered"""
        neural_web = NeuralWeb(neural_web_path)

        concepts = neural_web.extract_concepts("I am an AI")

        # Words shorter than 3 characters should be filtered
        assert "i" not in concepts
        assert "am" not in concepts
        assert "an" not in concepts

    def test_extract_concepts_extracts_phrases(self, neural_web_path: Path) -> None:
        """Test extraction of multi-word phrases"""
        neural_web = NeuralWeb(neural_web_path)

        concepts = neural_web.extract_concepts("machine learning neural networks")

        # Should include some multi-word phrases
        assert len(concepts) > 0
        # Check if any concepts contain spaces (phrases)
        phrases = [c for c in concepts if " " in c]
        assert len(phrases) > 0 or "machine" in concepts

    def test_extract_concepts_from_empty_text(self, neural_web_path: Path) -> None:
        """Test extracting concepts from empty text"""
        neural_web = NeuralWeb(neural_web_path)

        concepts = neural_web.extract_concepts("")

        assert concepts == []


class TestNeuralWebNeuronManagement:
    """Tests for neuron creation and management"""

    def test_get_or_create_neuron_creates_new(self, neural_web_path: Path) -> None:
        """Test creating a new neuron"""
        neural_web = NeuralWeb(neural_web_path)

        neuron_id = neural_web.get_or_create_neuron("python")

        assert neuron_id.startswith("n_")
        assert "python" in neural_web.concept_to_neuron
        assert neuron_id in neural_web.neurons

    def test_get_or_create_neuron_returns_existing(self, neural_web_path: Path) -> None:
        """Test returning existing neuron"""
        neural_web = NeuralWeb(neural_web_path)

        neuron_id1 = neural_web.get_or_create_neuron("python")
        neuron_id2 = neural_web.get_or_create_neuron("python")

        assert neuron_id1 == neuron_id2
        assert len(neural_web.neurons) == 1

    def test_get_or_create_neuron_case_insensitive(self, neural_web_path: Path) -> None:
        """Test neuron lookup is case-insensitive"""
        neural_web = NeuralWeb(neural_web_path)

        neuron_id1 = neural_web.get_or_create_neuron("Python")
        neuron_id2 = neural_web.get_or_create_neuron("PYTHON")
        neuron_id3 = neural_web.get_or_create_neuron("python")

        assert neuron_id1 == neuron_id2 == neuron_id3

    def test_activate_neurons(self, neural_web_path: Path) -> None:
        """Test activating multiple neurons"""
        neural_web = NeuralWeb(neural_web_path)

        neuron_ids = neural_web.activate_neurons(["python", "programming", "code"])

        assert len(neuron_ids) == 3
        for neuron_id in neuron_ids:
            assert neural_web.neurons[neuron_id].activation_count == 1


class TestNeuralWebConnectionStrengthening:
    """Tests for synapse strengthening"""

    def test_strengthen_connections_creates_synapses(self, neural_web_path: Path) -> None:
        """Test that strengthening creates synapses between neurons"""
        neural_web = NeuralWeb(neural_web_path)

        neuron_ids = ["n_0001", "n_0002", "n_0003"]
        # Create neurons first
        for i, nid in enumerate(neuron_ids):
            neural_web.neurons[nid] = Neuron(nid, f"concept_{i}")

        neural_web.strengthen_connections(neuron_ids)

        # Should create bidirectional connections between all pairs
        # 3 neurons = 3 pairs * 2 directions = 6 synapses
        assert len(neural_web.synapses) == 6

    def test_strengthen_connections_bidirectional(self, neural_web_path: Path) -> None:
        """Test that connections are bidirectional"""
        neural_web = NeuralWeb(neural_web_path)

        n1 = "n_0001"
        n2 = "n_0002"
        neural_web.neurons[n1] = Neuron(n1, "concept1")
        neural_web.neurons[n2] = Neuron(n2, "concept2")

        neural_web.strengthen_connections([n1, n2])

        assert (n1, n2) in neural_web.synapses
        assert (n2, n1) in neural_web.synapses


class TestNeuralWebLearning:
    """Tests for learning from text"""

    def test_learn_from_text(self, neural_web_path: Path) -> None:
        """Test learning from text"""
        neural_web = NeuralWeb(neural_web_path)

        neural_web.learn_from_text("Python programming is awesome")

        # Should have created some neurons
        assert len(neural_web.neurons) > 0
        # Should have created some synapses
        assert len(neural_web.synapses) > 0

    def test_learn_from_empty_text(self, neural_web_path: Path) -> None:
        """Test learning from empty text does nothing"""
        neural_web = NeuralWeb(neural_web_path)

        neural_web.learn_from_text("")

        assert len(neural_web.neurons) == 0
        assert len(neural_web.synapses) == 0

    def test_learn_strengthens_existing_connections(self, neural_web_path: Path) -> None:
        """Test that repeated learning strengthens connections"""
        neural_web = NeuralWeb(neural_web_path)

        neural_web.learn_from_text("Python programming")
        initial_synapse_count = len(neural_web.synapses)

        neural_web.learn_from_text("Python programming")

        # Should not create new synapses, but strengthen existing ones
        assert len(neural_web.synapses) == initial_synapse_count


class TestNeuralWebDecay:
    """Tests for synapse decay"""

    def test_apply_decay(self, neural_web_path: Path) -> None:
        """Test applying decay to old synapses"""
        neural_web = NeuralWeb(neural_web_path)

        # Create a synapse with old timestamp
        synapse = Synapse("n_0001", "n_0002")
        synapse.last_activated = "2020-01-01T00:00:00"
        synapse.weight = 0.5
        neural_web.synapses[("n_0001", "n_0002")] = synapse

        neural_web.apply_decay(days_threshold=7, decay_amount=0.1)

        # Synapse should still exist but be weakened
        assert ("n_0001", "n_0002") in neural_web.synapses
        assert neural_web.synapses[("n_0001", "n_0002")].weight < 0.5

    def test_apply_decay_removes_weak_synapses(self, neural_web_path: Path) -> None:
        """Test that very weak synapses are removed"""
        neural_web = NeuralWeb(neural_web_path)

        # Create a very weak synapse with old timestamp
        synapse = Synapse("n_0001", "n_0002")
        synapse.last_activated = "2020-01-01T00:00:00"
        synapse.weight = 0.04  # Below removal threshold after decay
        neural_web.synapses[("n_0001", "n_0002")] = synapse

        neural_web.apply_decay(days_threshold=7)

        # Synapse should be removed
        assert ("n_0001", "n_0002") not in neural_web.synapses


class TestNeuralWebQueries:
    """Tests for querying the neural web"""

    def test_get_related_concepts(self, neural_web_path: Path) -> None:
        """Test getting related concepts"""
        neural_web = NeuralWeb(neural_web_path)

        # Create a small neural web
        neural_web.learn_from_text("Python programming language")
        neural_web.learn_from_text("Python coding framework")

        related = neural_web.get_related_concepts("python", limit=5)

        # Should find related concepts
        assert len(related) > 0
        assert all("concept" in r and "weight" in r for r in related)

    def test_get_related_concepts_for_unknown_concept(self, neural_web_path: Path) -> None:
        """Test getting related concepts for unknown concept"""
        neural_web = NeuralWeb(neural_web_path)

        related = neural_web.get_related_concepts("nonexistent", limit=5)

        assert related == []

    def test_get_strongest_patterns(self, neural_web_path: Path) -> None:
        """Test getting strongest patterns"""
        neural_web = NeuralWeb(neural_web_path)

        # Create patterns by learning similar text multiple times
        for _ in range(5):
            neural_web.learn_from_text("machine learning neural networks")

        patterns = neural_web.get_strongest_patterns(limit=5)

        assert len(patterns) > 0
        assert all("source" in p and "target" in p and "strength" in p for p in patterns)


class TestNeuralWebPersistence:
    """Tests for saving and loading"""

    def test_save_and_load(self, neural_web_path: Path) -> None:
        """Test saving and loading neural web"""
        neural_web1 = NeuralWeb(neural_web_path)
        neural_web1.learn_from_text("Python programming machine learning")
        initial_neuron_count = len(neural_web1.neurons)
        initial_synapse_count = len(neural_web1.synapses)

        neural_web1.save()

        # Create new instance and load
        neural_web2 = NeuralWeb(neural_web_path)
        neural_web2.load()

        assert len(neural_web2.neurons) == initial_neuron_count
        assert len(neural_web2.synapses) == initial_synapse_count

    def test_save_creates_file(self, neural_web_path: Path) -> None:
        """Test that save creates neural_web.json file"""
        neural_web = NeuralWeb(neural_web_path)
        neural_web.learn_from_text("test")

        neural_web.save()

        assert (neural_web_path / "neural_web.json").exists()


class TestNeuralWebStats:
    """Tests for statistics"""

    def test_get_stats_empty_web(self, neural_web_path: Path) -> None:
        """Test stats for empty neural web"""
        neural_web = NeuralWeb(neural_web_path)

        stats = neural_web.get_stats()

        assert stats["total_neurons"] == 0
        assert stats["total_synapses"] == 0
        assert stats["total_activations"] == 0
        assert stats["avg_activations_per_neuron"] == 0
        assert stats["avg_synapse_weight"] == 0

    def test_get_stats_with_data(self, neural_web_path: Path) -> None:
        """Test stats with data"""
        neural_web = NeuralWeb(neural_web_path)
        neural_web.learn_from_text("Python programming machine learning")

        stats = neural_web.get_stats()

        assert stats["total_neurons"] > 0
        assert stats["total_synapses"] > 0
        assert isinstance(stats["avg_activations_per_neuron"], (int, float))
        assert isinstance(stats["avg_synapse_weight"], (int, float))


class TestGetNeuralWebSingleton:
    """Tests for get_neural_web singleton"""

    def test_get_neural_web_returns_instance(self, neural_web_path: Path) -> None:
        """Test that get_neural_web returns NeuralWeb instance"""
        neural_web = get_neural_web(neural_web_path)

        assert isinstance(neural_web, NeuralWeb)

    def test_get_neural_web_returns_same_instance(self, neural_web_path: Path) -> None:
        """Test that get_neural_web returns the same instance (singleton)"""
        neural_web1 = get_neural_web(neural_web_path)
        neural_web2 = get_neural_web(neural_web_path)

        assert neural_web1 is neural_web2

    def test_get_neural_web_loads_data(self, neural_web_path: Path) -> None:
        """Test that get_neural_web loads existing data"""
        # Create and save data
        neural_web1 = NeuralWeb(neural_web_path)
        neural_web1.learn_from_text("test data")
        neural_web1.save()

        # Reset global instance
        import neural_web_typed

        neural_web_typed._neural_web = None

        # Get new instance should load data
        neural_web2 = get_neural_web(neural_web_path)

        assert len(neural_web2.neurons) > 0
