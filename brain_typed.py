"""
REL Brain Module - FAISS Semantic Search
Embeddings + Vector Storage + Intelligent Search

This is MY (Corwin's) semantic memory - understanding concepts, not just matching keywords
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("REL.Brain")

# Type stubs for optional dependencies
try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover
    SentenceTransformer = None  # type: ignore

try:
    import faiss
except ImportError:  # pragma: no cover
    faiss = None

try:
    import numpy as np
    import numpy.typing as npt
except ImportError:  # pragma: no cover
    np = None  # type: ignore
    npt = None  # type: ignore


def get_sentence_transformer() -> Optional[Any]:
    """Lazy load sentence transformer

    Returns:
        Optional[SentenceTransformer]: Loaded model or None if unavailable
    """
    global _sentence_transformer
    if _sentence_transformer is None and SentenceTransformer is not None:
        try:
            _sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("✅ Sentence transformer loaded: all-MiniLM-L6-v2")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            _sentence_transformer = None
    return _sentence_transformer


def get_faiss() -> Optional[Any]:
    """Lazy load FAISS

    Returns:
        Optional[faiss]: FAISS module or None if unavailable
    """
    global _faiss
    if _faiss is None and faiss is not None:
        try:
            _faiss = faiss
            logger.info("✅ FAISS loaded")
        except Exception as e:  # pragma: no cover
            logger.error(f"Failed to load FAISS: {e}")
            _faiss = None
    return _faiss


def get_numpy() -> Optional[Any]:
    """Lazy load numpy

    Returns:
        Optional[numpy]: NumPy module or None if unavailable
    """
    global _np
    if _np is None and np is not None:
        try:
            _np = np
            logger.info("✅ NumPy loaded")
        except Exception as e:  # pragma: no cover
            logger.error(f"Failed to load NumPy: {e}")
            _np = None
    return _np


# Global instances for lazy loading
_sentence_transformer: Optional[Any] = None
_faiss: Optional[Any] = None
_np: Optional[Any] = None


class RELBrain:
    """Semantic memory and search for REL using FAISS vector database

    This class provides semantic search capabilities using sentence transformers
    for embedding generation and FAISS for efficient vector similarity search.

    Attributes:
        brain_path: Directory path for storing brain data
        index_path: Path to FAISS index file
        documents_path: Path to documents JSON file
        metadata_path: Path to metadata JSON file
        model: Sentence transformer model for embeddings
        index: FAISS index for vector search
        documents: List of stored documents with metadata
        dimension: Embedding dimension (384 for all-MiniLM-L6-v2)
    """

    def __init__(self, brain_path: Path) -> None:
        """Initialize REL Brain

        Args:
            brain_path: Directory path where brain data will be stored
        """
        self.brain_path: Path = brain_path
        self.index_path: Path = brain_path / "faiss_index.bin"
        self.documents_path: Path = brain_path / "documents.json"
        self.metadata_path: Path = brain_path / "brain_metadata.json"

        self.model: Optional[Any] = None
        self.index: Optional[Any] = None
        self.documents: List[Dict[str, Any]] = []
        self.dimension: int = 384  # all-MiniLM-L6-v2 dimension

        # Ensure brain directory exists
        self.brain_path.mkdir(parents=True, exist_ok=True)

    def initialize(self) -> bool:
        """Initialize the brain (load model and index)

        This method loads the sentence transformer model and FAISS index.
        If the index exists on disk, it loads it; otherwise, creates a new one.

        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Load sentence transformer
            self.model = get_sentence_transformer()
            if self.model is None:
                logger.error("Cannot initialize brain - sentence transformer failed to load")
                return False

            # Load or create FAISS index
            faiss_lib = get_faiss()
            numpy_lib = get_numpy()

            if faiss_lib is None or numpy_lib is None:
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
                with open(self.documents_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
                logger.info(f"✅ Loaded {len(self.documents)} documents")
            else:
                self.documents = []
                logger.info("✅ Initialized empty document store")

            return True

        except Exception as e:
            logger.error(f"Failed to initialize brain: {e}")
            return False

    def save_index(self) -> None:
        """Save FAISS index and documents to disk

        Persists the current state of the brain to disk, including
        the FAISS index and document metadata.
        """
        try:
            faiss_lib = get_faiss()
            if faiss_lib and self.index:
                faiss_lib.write_index(self.index, str(self.index_path))
                logger.info("✅ Saved FAISS index")

            if self.documents:
                with open(self.documents_path, "w", encoding="utf-8") as f:
                    json.dump(self.documents, f, indent=2)
                logger.info(f"✅ Saved {len(self.documents)} documents")

        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def ingest_text(self, text: str, metadata: Dict[str, Any]) -> bool:
        """Ingest text into the brain

        Generates an embedding for the text and adds it to the FAISS index
        along with the document metadata.

        Args:
            text: Text content to ingest
            metadata: Metadata dictionary associated with the text

        Returns:
            bool: True if ingestion successful, False otherwise
        """
        try:
            if not self.model or not self.index:
                if not self.initialize():
                    return False

            assert self.model is not None
            assert self.index is not None

            numpy_lib = get_numpy()
            if numpy_lib is None:
                return False

            # Generate embedding
            embedding = self.model.encode([text])[0]

            # Add to FAISS index
            embedding_array = numpy_lib.array([embedding], dtype="float32")
            self.index.add(embedding_array)

            # Store document
            doc: Dict[str, Any] = {
                "text": text,
                "metadata": metadata,
                "id": len(self.documents),
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
        """Semantic search for similar content

        Performs a semantic similarity search using the query text.
        Returns the most similar documents based on embedding similarity.

        Args:
            query: Search query text
            limit: Maximum number of results to return

        Returns:
            List of dictionaries containing matching documents with similarity scores
        """
        try:
            if not self.model or not self.index:
                if not self.initialize():
                    return []

            assert self.model is not None
            assert self.index is not None

            if self.index.ntotal == 0:
                logger.info("Brain is empty - no vectors to search")
                return []

            numpy_lib = get_numpy()
            if numpy_lib is None:
                return []

            # Generate query embedding
            query_embedding = self.model.encode([query])[0]
            query_array = numpy_lib.array([query_embedding], dtype="float32")

            # Search FAISS index
            k = min(limit, self.index.ntotal)
            distances, indices = self.index.search(query_array, k)

            # Retrieve documents
            results: List[Dict[str, Any]] = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                if 0 <= idx < len(self.documents):
                    doc = self.documents[int(idx)]
                    results.append(
                        {
                            "text": doc["text"],
                            "metadata": doc["metadata"],
                            "similarity_score": float(
                                1.0 / (1.0 + distance)
                            ),  # Convert distance to similarity
                            "rank": i + 1,
                        }
                    )

            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get brain statistics

        Returns:
            Dictionary containing brain statistics including vector count,
            document count, dimension, and configuration details
        """
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "total_documents": len(self.documents),
            "dimension": self.dimension,
            "model": "all-MiniLM-L6-v2",
            "index_type": "FAISS IndexFlatL2",
        }

    def ingest_from_state_and_log(
        self, state: Dict[str, Any], log: Dict[str, Any]
    ) -> int:
        """Ingest content from state and session log

        Processes REL state and session log to extract and ingest
        wins, ideas, sessions, achievements, and projects.

        Args:
            state: REL CoreState dictionary
            log: REL SessionLog dictionary

        Returns:
            int: Number of items successfully ingested
        """
        count = 0

        try:
            # Ingest wins
            for win in state.get("recent_wins", []):
                text = f"Win: {win.get('win', '')}"
                metadata = {
                    "type": "win",
                    "date": win.get("date"),
                    "impact": win.get("impact"),
                }
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
_brain_instance: Optional[RELBrain] = None


def get_brain(brain_path: Path) -> RELBrain:
    """Get or create global brain instance

    Args:
        brain_path: Directory path for brain storage

    Returns:
        RELBrain: Global brain instance
    """
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = RELBrain(brain_path)
    return _brain_instance
