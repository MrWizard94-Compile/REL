"""
REL Neural Web - Learning System
Neurons, Synapses, Connection Strengthening, Pattern Emergence

This is MY (Corwin's) learning brain - concepts as neurons, connections as synapses.
Connections strengthen with use, weaken over time. Patterns emerge automatically.
Over time, I predict what Rob needs before he asks.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger("REL.NeuralWeb")


class Neuron:
    """Represents a concept in the neural web"""
    
    def __init__(self, neuron_id: str, concept: str, created: str = None):
        self.id = neuron_id
        self.concept = concept
        self.activation_count = 0
        self.last_activated = created or datetime.now().isoformat()
        self.created = created or datetime.now().isoformat()
        self.tags = set()
    
    def activate(self):
        """Activate this neuron"""
        self.activation_count += 1
        self.last_activated = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "concept": self.concept,
            "activation_count": self.activation_count,
            "last_activated": self.last_activated,
            "created": self.created,
            "tags": list(self.tags)
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Neuron':
        """Create neuron from dictionary"""
        neuron = Neuron(data["id"], data["concept"], data.get("created"))
        neuron.activation_count = data.get("activation_count", 0)
        neuron.last_activated = data.get("last_activated", neuron.created)
        neuron.tags = set(data.get("tags", []))
        return neuron


class Synapse:
    """Represents a connection between two neurons"""
    
    def __init__(self, source_id: str, target_id: str):
        self.source_id = source_id
        self.target_id = target_id
        self.weight = 0.1  # Initial weight
        self.frequency = 0
        self.last_activated = datetime.now().isoformat()
        self.created = datetime.now().isoformat()
    
    def strengthen(self, amount: float = 0.1):
        """Strengthen this connection"""
        self.weight = min(1.0, self.weight + amount)
        self.frequency += 1
        self.last_activated = datetime.now().isoformat()
    
    def decay(self, amount: float = 0.01):
        """Decay this connection over time"""
        self.weight = max(0.0, self.weight - amount)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "weight": self.weight,
            "frequency": self.frequency,
            "last_activated": self.last_activated,
            "created": self.created
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'Synapse':
        """Create synapse from dictionary"""
        synapse = Synapse(data["source_id"], data["target_id"])
        synapse.weight = data.get("weight", 0.1)
        synapse.frequency = data.get("frequency", 0)
        synapse.last_activated = data.get("last_activated", synapse.created)
        synapse.created = data.get("created", synapse.created)
        return synapse


class NeuralWeb:
    """The complete neural web learning system"""
    
    def __init__(self, web_path: Path):
        self.web_path = web_path
        self.neurons: Dict[str, Neuron] = {}
        self.synapses: Dict[Tuple[str, str], Synapse] = {}
        self.concept_to_neuron: Dict[str, str] = {}  # Concept -> Neuron ID lookup
        
        # Ensure directory exists
        self.web_path.mkdir(parents=True, exist_ok=True)
    
    def load(self):
        """Load neural web from disk"""
        web_file = self.web_path / "neural_web.json"
        
        if web_file.exists():
            try:
                with open(web_file, 'r') as f:
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
                
                logger.info(f"✅ Loaded neural web: {len(self.neurons)} neurons, {len(self.synapses)} synapses")
                
            except Exception as e:
                logger.error(f"Failed to load neural web: {e}")
        else:
            logger.info("✅ Initialized empty neural web")
    
    def save(self):
        """Save neural web to disk"""
        web_file = self.web_path / "neural_web.json"
        
        try:
            data = {
                "neurons": [n.to_dict() for n in self.neurons.values()],
                "synapses": [s.to_dict() for s in self.synapses.values()],
                "metadata": {
                    "total_neurons": len(self.neurons),
                    "total_synapses": len(self.synapses),
                    "last_updated": datetime.now().isoformat()
                }
            }
            
            with open(web_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"✅ Saved neural web: {len(self.neurons)} neurons, {len(self.synapses)} synapses")
            
        except Exception as e:
            logger.error(f"Failed to save neural web: {e}")
    
    def extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                     'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
                     'we', 'they', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        
        # Filter out stop words
        concepts = [w for w in words if w not in stop_words]
        
        # Also extract multi-word phrases (2-3 words)
        phrases = re.findall(r'\b[a-z]+\s+[a-z]+(?:\s+[a-z]+)?\b', text.lower())
        
        # Combine and deduplicate
        all_concepts = list(set(concepts + phrases))
        
        return all_concepts
    
    def get_or_create_neuron(self, concept: str) -> str:
        """Get existing neuron ID or create new neuron for concept"""
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
    
    def activate_neurons(self, concepts: List[str]):
        """Activate neurons for given concepts"""
        neuron_ids = []
        
        for concept in concepts:
            neuron_id = self.get_or_create_neuron(concept)
            self.neurons[neuron_id].activate()
            neuron_ids.append(neuron_id)
        
        return neuron_ids
    
    def strengthen_connections(self, neuron_ids: List[str]):
        """Strengthen connections between co-activated neurons"""
        # Create or strengthen synapses between all pairs
        for i, source_id in enumerate(neuron_ids):
            for target_id in neuron_ids[i+1:]:
                # Bidirectional connections
                self._strengthen_synapse(source_id, target_id)
                self._strengthen_synapse(target_id, source_id)
    
    def _strengthen_synapse(self, source_id: str, target_id: str):
        """Strengthen a specific synapse"""
        key = (source_id, target_id)
        
        if key in self.synapses:
            self.synapses[key].strengthen()
        else:
            synapse = Synapse(source_id, target_id)
            synapse.strengthen()
            self.synapses[key] = synapse
    
    def learn_from_text(self, text: str, context: str = None):
        """Learn from a piece of text"""
        # Extract concepts
        concepts = self.extract_concepts(text)
        
        if not concepts:
            return
        
        # Activate neurons
        neuron_ids = self.activate_neurons(concepts)
        
        # Strengthen connections
        self.strengthen_connections(neuron_ids)
        
        logger.info(f"Learned from text: {len(concepts)} concepts, {len(neuron_ids)} neurons activated")
    
    def apply_decay(self, days_threshold: int = 7, decay_amount: float = 0.01):
        """Apply decay to connections that haven't been used recently"""
        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        
        decayed_count = 0
        removed_count = 0
        
        synapses_to_remove = []
        
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
            except:
                pass
        
        # Remove weak synapses
        for key in synapses_to_remove:
            del self.synapses[key]
        
        if decayed_count > 0:
            logger.info(f"Applied decay: {decayed_count} synapses weakened, {removed_count} removed")
    
    def get_related_concepts(self, concept: str, limit: int = 10) -> List[Dict]:
        """Get concepts related to a given concept"""
        concept_lower = concept.lower()
        
        if concept_lower not in self.concept_to_neuron:
            return []
        
        neuron_id = self.concept_to_neuron[concept_lower]
        
        # Find all synapses from this neuron
        related = []
        
        for (source_id, target_id), synapse in self.synapses.items():
            if source_id == neuron_id:
                target_neuron = self.neurons.get(target_id)
                if target_neuron:
                    related.append({
                        "concept": target_neuron.concept,
                        "weight": synapse.weight,
                        "frequency": synapse.frequency
                    })
        
        # Sort by weight
        related.sort(key=lambda x: x["weight"], reverse=True)
        
        return related[:limit]
    
    def get_strongest_patterns(self, limit: int = 10) -> List[Dict]:
        """Get the strongest patterns in the neural web"""
        # Sort synapses by weight
        sorted_synapses = sorted(
            self.synapses.values(),
            key=lambda s: s.weight * s.frequency,
            reverse=True
        )
        
        patterns = []
        for synapse in sorted_synapses[:limit]:
            source = self.neurons.get(synapse.source_id)
            target = self.neurons.get(synapse.target_id)
            
            if source and target:
                patterns.append({
                    "source": source.concept,
                    "target": target.concept,
                    "weight": synapse.weight,
                    "frequency": synapse.frequency,
                    "strength": synapse.weight * synapse.frequency
                })
        
        return patterns
    
    def get_stats(self) -> Dict:
        """Get neural web statistics"""
        total_activation = sum(n.activation_count for n in self.neurons.values())
        avg_activation = total_activation / len(self.neurons) if self.neurons else 0
        
        total_weight = sum(s.weight for s in self.synapses.values())
        avg_weight = total_weight / len(self.synapses) if self.synapses else 0
        
        return {
            "total_neurons": len(self.neurons),
            "total_synapses": len(self.synapses),
            "total_activations": total_activation,
            "avg_activations_per_neuron": round(avg_activation, 2),
            "avg_synapse_weight": round(avg_weight, 3),
            "strongest_connections": len([s for s in self.synapses.values() if s.weight > 0.5])
        }


# Global neural web instance
_neural_web = None

def get_neural_web(web_path: Path) -> NeuralWeb:
    """Get or create global neural web instance"""
    global _neural_web
    if _neural_web is None:
        _neural_web = NeuralWeb(web_path)
        _neural_web.load()
    return _neural_web
