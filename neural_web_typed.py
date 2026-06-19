"""
REL Neural Web - Learning System (Type-Safe Version)
Neurons, Synapses, Connection Strengthening, Pattern Emergence

This is MY (Corwin's) learning brain - concepts as neurons, connections as synapses.
Connections strengthen with use, weaken over time. Patterns emerge automatically.
Over time, I predict what Rob needs before he asks.
"""

import json
import logging
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger("REL.NeuralWeb")


class Neuron:
    """Represents a concept in the neural web
    
    A neuron encapsulates a single concept and tracks its activation history.
    Neurons are activated when their concept appears in learned text, and
    their activation count indicates importance.
    
    Attributes:
        id: Unique identifier for the neuron
        concept: The concept this neuron represents
        activation_count: Number of times this neuron has been activated
        last_activated: ISO timestamp of last activation
        created: ISO timestamp of neuron creation
        tags: Set of tags for categorization
    """

    def __init__(self, neuron_id: str, concept: str, created: Optional[str] = None) -> None:
        """Initialize a neuron
        
        Args:
            neuron_id: Unique identifier for this neuron
            concept: The concept this neuron represents
            created: Optional ISO timestamp of creation, defaults to now
        """
        self.id: str = neuron_id
        self.concept: str = concept
        self.activation_count: int = 0
        self.last_activated: str = created or datetime.now().isoformat()
        self.created: str = created or datetime.now().isoformat()
        self.tags: Set[str] = set()

    def activate(self) -> None:
        """Activate this neuron
        
        Increments the activation count and updates the last activation timestamp.
        Called when this concept appears in learned text.
        """
        self.activation_count += 1
        self.last_activated = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "id": self.id,
            "concept": self.concept,
            "activation_count": self.activation_count,
            "last_activated": self.last_activated,
            "created": self.created,
            "tags": list(self.tags),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Neuron":
        """Create neuron from dictionary
        
        Args:
            data: Dictionary containing neuron data
            
        Returns:
            Neuron instance reconstructed from dictionary
        """
        neuron = Neuron(data["id"], data["concept"], data.get("created"))
        neuron.activation_count = data.get("activation_count", 0)
        neuron.last_activated = data.get("last_activated", neuron.created)
        neuron.tags = set(data.get("tags", []))
        return neuron


class Synapse:
    """Represents a connection between two neurons
    
    A synapse connects two neurons and tracks the strength of their relationship.
    Strength increases when concepts co-occur and decreases over time without use.
    
    Attributes:
        source_id: ID of the source neuron
        target_id: ID of the target neuron
        weight: Connection strength (0.0 to 1.0)
        frequency: Number of times this connection was strengthened
        last_activated: ISO timestamp of last activation
        created: ISO timestamp of synapse creation
    """

    def __init__(self, source_id: str, target_id: str) -> None:
        """Initialize a synapse
        
        Args:
            source_id: ID of the source neuron
            target_id: ID of the target neuron
        """
        self.source_id: str = source_id
        self.target_id: str = target_id
        self.weight: float = 0.1  # Initial weight
        self.frequency: int = 0
        self.last_activated: str = datetime.now().isoformat()
        self.created: str = datetime.now().isoformat()

    def strengthen(self, amount: float = 0.1) -> None:
        """Strengthen this connection
        
        Increases the weight (up to 1.0) and increments frequency counter.
        
        Args:
            amount: Amount to increase weight by (default 0.1)
        """
        self.weight = min(1.0, self.weight + amount)
        self.frequency += 1
        self.last_activated = datetime.now().isoformat()

    def decay(self, amount: float = 0.01) -> None:
        """Decay this connection over time
        
        Decreases the weight (down to 0.0) to simulate forgetting.
        
        Args:
            amount: Amount to decrease weight by (default 0.01)
        """
        self.weight = max(0.0, self.weight - amount)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization
        
        Returns:
            Dictionary representation suitable for JSON serialization
        """
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "weight": self.weight,
            "frequency": self.frequency,
            "last_activated": self.last_activated,
            "created": self.created,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Synapse":
        """Create synapse from dictionary
        
        Args:
            data: Dictionary containing synapse data
            
        Returns:
            Synapse instance reconstructed from dictionary
        """
        synapse = Synapse(data["source_id"], data["target_id"])
        synapse.weight = data.get("weight", 0.1)
        synapse.frequency = data.get("frequency", 0)
        synapse.last_activated = data.get("last_activated", synapse.created)
        synapse.created = data.get("created", synapse.created)
        return synapse


class NeuralWeb:
    """The complete neural web learning system
    
    A neural network-inspired learning system that extracts concepts from text,
    creates neurons for concepts, and strengthens connections between co-occurring
    concepts. Enables pattern detection and related concept discovery.
    
    Attributes:
        web_path: Directory path for storing neural web data
        neurons: Dictionary mapping neuron IDs to Neuron objects
        synapses: Dictionary mapping (source_id, target_id) tuples to Synapse objects
        concept_to_neuron: Dictionary mapping concepts to neuron IDs for fast lookup
    """

    def __init__(self, web_path: Path) -> None:
        """Initialize neural web
        
        Args:
            web_path: Directory path where neural web data will be stored
        """
        self.web_path: Path = web_path
        self.neurons: Dict[str, Neuron] = {}
        self.synapses: Dict[Tuple[str, str], Synapse] = {}
        self.concept_to_neuron: Dict[str, str] = {}  # Concept -> Neuron ID lookup

        # Ensure directory exists
        self.web_path.mkdir(parents=True, exist_ok=True)

    def load(self) -> None:
        """Load neural web from disk
        
        Loads neurons and synapses from neural_web.json file.
        If file doesn't exist, initializes empty neural web.
        """
        web_file = self.web_path / "neural_web.json"

        if web_file.exists():
            try:
                with open(web_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load neurons
                for neuron_data in data.get("neurons", []):
                    neuron = Neuron.from_dict(neuron_data)
                    self.neurons[neuron.id] = neuron
                    self.concept_to_neuron[neuron.concept.lower()] = neuron.id

                # Load synapses
                for synapse_data in data.get("synapses", []):
                    synapse = Synapse.from_dict(synapse_data)
                    key = (synapse.source_id, synapse.target_id)
                    self.synapses[key] = synapse

                logger.info(
                    f"✅ Loaded neural web: {len(self.neurons)} neurons, "
                    f"{len(self.synapses)} synapses"
                )

            except Exception as e:
                logger.error(f"Failed to load neural web: {e}")
        else:
            logger.info("✅ Initialized empty neural web")

    def save(self) -> None:
        """Save neural web to disk
        
        Persists neurons and synapses to neural_web.json file with metadata.
        """
        web_file = self.web_path / "neural_web.json"

        try:
            data: Dict[str, Any] = {
                "neurons": [n.to_dict() for n in self.neurons.values()],
                "synapses": [s.to_dict() for s in self.synapses.values()],
                "metadata": {
                    "total_neurons": len(self.neurons),
                    "total_synapses": len(self.synapses),
                    "last_updated": datetime.now().isoformat(),
                },
            }

            with open(web_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            logger.info(
                f"✅ Saved neural web: {len(self.neurons)} neurons, "
                f"{len(self.synapses)} synapses"
            )

        except Exception as e:
            logger.error(f"Failed to save neural web: {e}")

    def extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text
        
        Extracts meaningful words and phrases from text by:
        1. Removing common stop words
        2. Extracting single words (3+ characters)
        3. Extracting multi-word phrases (2-3 words)
        4. Deduplicating results
        
        Args:
            text: Text to extract concepts from
            
        Returns:
            List of extracted concepts (words and phrases)
        """
        # Remove common stop words
        stop_words: Set[str] = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "was",
            "are",
            "were",
            "be",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "my",
            "your",
            "his",
            "her",
            "its",
            "our",
            "their",
        }

        # Extract words (alphanumeric sequences, 3+ characters)
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())

        # Filter out stop words
        concepts = [w for w in words if w not in stop_words]

        # Also extract multi-word phrases (2-3 words)
        phrases = re.findall(r"\b[a-z]+\s+[a-z]+(?:\s+[a-z]+)?\b", text.lower())

        # Combine and deduplicate
        all_concepts = list(set(concepts + phrases))

        return all_concepts

    def get_or_create_neuron(self, concept: str) -> str:
        """Get existing neuron ID or create new neuron for concept
        
        Looks up neuron by concept name (case-insensitive). If not found,
        creates a new neuron with auto-generated ID.
        
        Args:
            concept: The concept to find or create a neuron for
            
        Returns:
            Neuron ID (existing or newly created)
        """
        concept_lower = concept.lower()

        if concept_lower in self.concept_to_neuron:
            return self.concept_to_neuron[concept_lower]

        # Create new neuron
        neuron_id = f"n_{len(self.neurons):04d}"
        neuron = Neuron(neuron_id, concept)
        self.neurons[neuron_id] = neuron
        self.concept_to_neuron[concept_lower] = neuron_id

        logger.info(f"Created new neuron: {neuron_id} for '{concept}'")
        return neuron_id

    def activate_neurons(self, concepts: List[str]) -> List[str]:
        """Activate neurons for given concepts
        
        For each concept, gets or creates a neuron and activates it.
        
        Args:
            concepts: List of concepts to activate
            
        Returns:
            List of activated neuron IDs
        """
        neuron_ids: List[str] = []

        for concept in concepts:
            neuron_id = self.get_or_create_neuron(concept)
            self.neurons[neuron_id].activate()
            neuron_ids.append(neuron_id)

        return neuron_ids

    def strengthen_connections(self, neuron_ids: List[str]) -> None:
        """Strengthen connections between co-activated neurons
        
        Creates or strengthens bidirectional synapses between all pairs
        of neurons in the provided list. This implements Hebbian learning:
        "neurons that fire together, wire together."
        
        Args:
            neuron_ids: List of neuron IDs that were activated together
        """
        # Create or strengthen synapses between all pairs
        for i, source_id in enumerate(neuron_ids):
            for target_id in neuron_ids[i + 1 :]:
                # Bidirectional connections
                self._strengthen_synapse(source_id, target_id)
                self._strengthen_synapse(target_id, source_id)

    def _strengthen_synapse(self, source_id: str, target_id: str) -> None:
        """Strengthen a specific synapse
        
        Internal method to strengthen or create a synapse between two neurons.
        
        Args:
            source_id: Source neuron ID
            target_id: Target neuron ID
        """
        key = (source_id, target_id)

        if key in self.synapses:
            self.synapses[key].strengthen()
        else:
            synapse = Synapse(source_id, target_id)
            synapse.strengthen()
            self.synapses[key] = synapse

    def learn_from_text(self, text: str, context: Optional[str] = None) -> None:
        """Learn from a piece of text
        
        Extracts concepts, activates corresponding neurons, and strengthens
        connections between co-occurring concepts.
        
        Args:
            text: Text to learn from
            context: Optional context string (currently unused, reserved for future)
        """
        # Extract concepts
        concepts = self.extract_concepts(text)

        if not concepts:
            return

        # Activate neurons
        neuron_ids = self.activate_neurons(concepts)

        # Strengthen connections
        self.strengthen_connections(neuron_ids)

        logger.info(
            f"Learned from text: {len(concepts)} concepts, {len(neuron_ids)} neurons activated"
        )

    def apply_decay(self, days_threshold: int = 7, decay_amount: float = 0.01) -> None:
        """Apply decay to connections that haven't been used recently
        
        Implements forgetting by weakening synapses that haven't been activated
        recently. Very weak synapses (weight < 0.05) are removed entirely.
        
        Args:
            days_threshold: Number of days of inactivity before decay applies
            decay_amount: Amount to decrease synapse weight by (default 0.01)
        """
        cutoff_date = datetime.now() - timedelta(days=days_threshold)

        decayed_count = 0
        removed_count = 0

        synapses_to_remove: List[Tuple[str, str]] = []

        for key, synapse in self.synapses.items():
            try:
                last_activated = datetime.fromisoformat(synapse.last_activated)

                if last_activated < cutoff_date:
                    synapse.decay(decay_amount)
                    decayed_count += 1

                    # Remove very weak synapses
                    if synapse.weight < 0.05:
                        synapses_to_remove.append(key)
                        removed_count += 1
            except (ValueError, TypeError):
                # Skip synapses with invalid timestamps
                pass

        # Remove weak synapses
        for key in synapses_to_remove:
            del self.synapses[key]

        if decayed_count > 0:
            logger.info(
                f"Applied decay: {decayed_count} synapses weakened, {removed_count} removed"
            )

    def get_related_concepts(self, concept: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get concepts related to a given concept
        
        Finds concepts connected to the given concept via synapses,
        sorted by connection strength.
        
        Args:
            concept: Concept to find relations for
            limit: Maximum number of related concepts to return
            
        Returns:
            List of dictionaries containing related concepts with weights and frequencies
        """
        concept_lower = concept.lower()

        if concept_lower not in self.concept_to_neuron:
            return []

        neuron_id = self.concept_to_neuron[concept_lower]

        # Find all synapses from this neuron
        related: List[Dict[str, Any]] = []

        for (source_id, target_id), synapse in self.synapses.items():
            if source_id == neuron_id:
                target_neuron = self.neurons.get(target_id)
                if target_neuron:
                    related.append(
                        {
                            "concept": target_neuron.concept,
                            "weight": synapse.weight,
                            "frequency": synapse.frequency,
                        }
                    )

        # Sort by weight
        related.sort(key=lambda x: x["weight"], reverse=True)

        return related[:limit]

    def get_strongest_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the strongest patterns in the neural web
        
        Returns the most strongly connected concept pairs, ranked by
        combined weight and frequency.
        
        Args:
            limit: Maximum number of patterns to return
            
        Returns:
            List of dictionaries containing pattern information
        """
        # Sort synapses by weight * frequency
        sorted_synapses = sorted(
            self.synapses.values(), key=lambda s: s.weight * s.frequency, reverse=True
        )

        patterns: List[Dict[str, Any]] = []
        for synapse in sorted_synapses[:limit]:
            source = self.neurons.get(synapse.source_id)
            target = self.neurons.get(synapse.target_id)

            if source and target:
                patterns.append(
                    {
                        "source": source.concept,
                        "target": target.concept,
                        "weight": synapse.weight,
                        "frequency": synapse.frequency,
                        "strength": synapse.weight * synapse.frequency,
                    }
                )

        return patterns

    def get_stats(self) -> Dict[str, Any]:
        """Get neural web statistics
        
        Returns:
            Dictionary containing statistics about the neural web state
        """
        total_activation = sum(n.activation_count for n in self.neurons.values())
        avg_activation = total_activation / len(self.neurons) if self.neurons else 0.0

        total_weight = sum(s.weight for s in self.synapses.values())
        avg_weight = total_weight / len(self.synapses) if self.synapses else 0.0

        return {
            "total_neurons": len(self.neurons),
            "total_synapses": len(self.synapses),
            "total_activations": total_activation,
            "avg_activations_per_neuron": round(avg_activation, 2),
            "avg_synapse_weight": round(avg_weight, 3),
            "strongest_connections": len([s for s in self.synapses.values() if s.weight > 0.5]),
        }


# Global neural web instance
_neural_web: Optional[NeuralWeb] = None


def get_neural_web(web_path: Path) -> NeuralWeb:
    """Get or create global neural web instance
    
    Implements singleton pattern to ensure only one neural web exists.
    Loads neural web data from disk on first call.
    
    Args:
        web_path: Directory path for neural web storage
        
    Returns:
        Global NeuralWeb instance
    """
    global _neural_web
    if _neural_web is None:
        _neural_web = NeuralWeb(web_path)
        _neural_web.load()
    return _neural_web
