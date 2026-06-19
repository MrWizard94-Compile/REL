"""
REL Brain Module - FAISS Semantic Search
Embeddings + Vector Storage + Intelligent Search

This is MY (Corwin's) semantic memory - understanding concepts, not just matching keywords
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger("REL.Brain")

# Lazy imports - only load when needed
_sentence_transformer = None
_faiss = None
_np = None

def get_sentence_transformer():
    """Lazy load sentence transformer"""
    global _sentence_transformer
    if _sentence_transformer is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence transformer loaded: all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            _sentence_transformer = None
    return _sentence_transformer

def get_faiss():
    """Lazy load FAISS"""
    global _faiss
    if _faiss is None:
        try:
            import faiss
            _faiss = faiss
            logger.info("✅ FAISS loaded")
        except Exception as e:
            logger.error(f"Failed to load FAISS: {e}")
            _faiss = None
    return _faiss

def get_numpy():
    """Lazy load numpy"""
    global _np
    if _np is None:
        try:
            import numpy as np
            _np = np
            logger.info("✅ NumPy loaded")
        except Exception as e:
            logger.error(f"Failed to load NumPy: {e}")
            _np = None
    return _np


class RELBrain:
    """Semantic memory and search for REL"""
    
    def __init__(self, brain_path: Path):
        self.brain_path = brain_path
        self.index_path = brain_path / "faiss_index.bin"
        self.documents_path = brain_path / "documents.json"
        self.metadata_path = brain_path / "brain_metadata.json"
        
        self.model = None
        self.index = None
        self.documents = []
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        # Ensure brain directory exists
        self.brain_path.mkdir(parents=True, exist_ok=True)
    
    def initialize(self) -> bool:
        """Initialize the brain (load model and index)"""
        try:
            # Load sentence transformer
            self.model = get_sentence_transformer()
            if self.model is None:
                logger.error("Cannot initialize brain - sentence transformer failed to load")
                return False
            
            # Load or create FAISS index
            faiss_lib = get_faiss()
            np = get_numpy()
            
            if faiss_lib is None or np is None:
                logger.error("Cannot initialize brain - FAISS or NumPy failed to load")
                return False
            
            if self.index_path.exists():
                # Load existing index
                self.index = faiss_lib.read_index(str(self.index_path))
                logger.info(f"✅ Loaded FAISS index with {self.index.ntotal} vectors")
            else:
                # Create new index
                self.index = faiss_lib.IndexFlatL2(self.dimension)
                logger.info("✅ Created new FAISS index")
            
            # Load documents
            if self.documents_path.exists():
                with open(self.documents_path, 'r') as f:
                    self.documents = json.load(f)
                logger.info(f"✅ Loaded {len(self.documents)} documents")
            else:
                self.documents = []
                logger.info("✅ Initialized empty document store")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize brain: {e}")
            return False
    
    def save_index(self):
        """Save FAISS index and documents to disk"""
        try:
            faiss_lib = get_faiss()
            if faiss_lib and self.index:
                faiss_lib.write_index(self.index, str(self.index_path))
                logger.info("✅ Saved FAISS index")
            
            if self.documents:
                with open(self.documents_path, 'w') as f:
                    json.dump(self.documents, f, indent=2)
                logger.info(f"✅ Saved {len(self.documents)} documents")
                
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
    def ingest_text(self, text: str, metadata: Dict[str, Any]) -> bool:
        """Ingest text into the brain"""
        try:
            if not self.model or not self.index:
                if not self.initialize():
                    return False
            
            np = get_numpy()
            if np is None:
                return False
            
            # Generate embedding
            embedding = self.model.encode([text])[0]
            
            # Add to FAISS index
            embedding_array = np.array([embedding], dtype='float32')
            self.index.add(embedding_array)
            
            # Store document
            doc = {
                "text": text,
                "metadata": metadata,
                "id": len(self.documents)
            }
            self.documents.append(doc)
            
            # Save periodically
            if len(self.documents) % 10 == 0:
                self.save_index()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to ingest text: {e}")
            return False
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Semantic search for similar content"""
        try:
            if not self.model or not self.index:
                if not self.initialize():
                    return []
            
            if self.index.ntotal == 0:
                logger.info("Brain is empty - no vectors to search")
                return []
            
            np = get_numpy()
            if np is None:
                return []
            
            # Generate query embedding
            query_embedding = self.model.encode([query])[0]
            query_array = np.array([query_embedding], dtype='float32')
            
            # Search FAISS index
            k = min(limit, self.index.ntotal)
            distances, indices = self.index.search(query_array, k)
            
            # Retrieve documents
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if idx < len(self.documents):
                    doc = self.documents[idx]
                    results.append({
                        "text": doc["text"],
                        "metadata": doc["metadata"],
                        "similarity_score": float(1.0 / (1.0 + distance)),  # Convert distance to similarity
                        "rank": i + 1
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get brain statistics"""
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "total_documents": len(self.documents),
            "dimension": self.dimension,
            "model": "all-MiniLM-L6-v2",
            "index_type": "FAISS IndexFlatL2",
        }
    
    def ingest_from_state_and_log(self, state: Dict, log: Dict) -> int:
        """Ingest content from state and session log"""
        count = 0
        
        try:
            # Ingest wins
            for win in state.get("recent_wins", []):
                text = f"Win: {win.get('win', '')}"
                metadata = {"type": "win", "date": win.get("date"), "impact": win.get("impact")}
                if self.ingest_text(text, metadata):
                    count += 1
            
            # Ingest ideas
            for idea in state.get("active_ideas", []):
                text = f"Idea: {idea}"
                metadata = {"type": "idea"}
                if self.ingest_text(text, metadata):
                    count += 1
            
            # Ingest session summaries
            for session in log.get("sessions", []):
                text = f"Session {session.get('session')}: {session.get('summary', '')}"
                metadata = {
                    "type": "session",
                    "session_num": session.get("session"),
                    "date": session.get("date"),
                }
                if self.ingest_text(text, metadata):
                    count += 1
                
                # Ingest achievements from session
                for achievement in session.get("achievements", []):
                    text = f"Achievement: {achievement}"
                    metadata = {
                        "type": "achievement",
                        "session_num": session.get("session"),
                        "date": session.get("date"),
                    }
                    if self.ingest_text(text, metadata):
                        count += 1
            
            # Ingest project descriptions
            for key, project in state.get("project_states", {}).items():
                text = f"Project {project.get('name')}: {project.get('description', '')}"
                metadata = {
                    "type": "project",
                    "project_key": key,
                    "status": project.get("status"),
                    "completion": project.get("completion"),
                }
                if self.ingest_text(text, metadata):
                    count += 1
            
            # Save after batch ingestion
            self.save_index()
            
            logger.info(f"✅ Ingested {count} items into brain")
            return count
            
        except Exception as e:
            logger.error(f"Failed to ingest from state/log: {e}")
            return count


# Global brain instance
_brain_instance = None

def get_brain(brain_path: Path) -> RELBrain:
    """Get or create global brain instance"""
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = RELBrain(brain_path)
    return _brain_instance
