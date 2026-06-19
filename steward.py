#!/usr/bin/env python3
"""
REL Steward — Local LLM-powered neural web maintenance agent.

Uses Qwen3-4B-Instruct via Ollama to:
  1. Extract domain-specific concepts from session summaries (replacing naive regex extraction)
  2. Run periodic maintenance (decay, noise pruning, reindexing)
  3. Batch-reprocess historical sessions to fix existing noise

Designed to be imported by mcp_server.py for real-time concept extraction,
or run standalone for maintenance tasks.

Dependencies: requests (stdlib-compatible via urllib), json, logging
External: Ollama running at localhost:11434 with qwen3:4b-instruct pulled
"""

import json
import logging
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Optional, Dict, Any

logger = logging.getLogger("REL.Steward")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:4b-instruct")
OLLAMA_TIMEOUT_SECONDS = 45

EXTRACTION_SYSTEM_PROMPT = """You are a concept extraction engine for a personal knowledge system.

Given a session summary, extract ONLY meaningful domain-specific concepts. Return a JSON array of strings.

EXTRACT:
- Project names (e.g., "Living Villages", "FUSE", "REL")
- Technical terms (e.g., "NeoForge", "FAISS", "neural web", "MCP server")
- Specific systems/features (e.g., "gossip propagation", "villager identity", "shift grabber")
- Tools and technologies (e.g., "Playwright", "Kotlin", "Electron", "Ollama")
- Game-specific terms (e.g., "Absolution Guardian", "Storm Secret", "elemental proliferation")
- Named concepts and decisions (e.g., "active memory edit", "steward agent", "cognitive reflex")
- Methodologies (e.g., "atomic writes", "file locking", "semantic search")

DO NOT EXTRACT:
- Common words (session, complete, working, built, started, etc.)
- People's names (Rob, Claude, Corwin, Char)
- Generic verbs and adjectives
- Time references (today, yesterday, March)
- Filler phrases (also, then, next, after)

Return ONLY a JSON array. No explanation, no markdown, no preamble.

Example input: "Built the A to Z Shift Grabber using Playwright browser automation. Three modes: noon burst, daemon, sniper. Successfully grabbed two Sorting shifts on first real run."
Example output: ["A to Z Shift Grabber", "Playwright", "browser automation", "noon burst mode", "daemon mode", "sniper mode", "shift grabbing"]"""

# ---------------------------------------------------------------------------
# Ollama Communication
# ---------------------------------------------------------------------------

def _ollama_available() -> bool:
    """Check if Ollama is running and the model is available."""
    try:
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/tags",
            method="GET"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name", "") for m in data.get("models", [])]
            # Check for the model (ollama may store with or without tag)
            for model_name in models:
                if OLLAMA_MODEL in model_name or model_name.startswith(OLLAMA_MODEL.split(":")[0]):
                    return True
            logger.warning(f"Ollama running but model '{OLLAMA_MODEL}' not found. Available: {models}")
            return False
    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError, OSError) as e:
        logger.debug(f"Ollama not available: {e}")
        return False


def _ollama_chat(system_prompt: str, user_message: str) -> Optional[str]:
    """Send a chat request to Ollama and return the response text."""
    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            content = data.get("message", {}).get("content", "")
            return content
    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError, OSError) as e:
        logger.error(f"Ollama chat request failed: {e}")
        return None


# ---------------------------------------------------------------------------
# Concept Extraction
# ---------------------------------------------------------------------------

def extract_concepts_llm(text: str) -> Optional[List[str]]:
    """
    Extract domain-specific concepts from text using the local LLM.

    Returns a list of concept strings, or None if extraction fails
    (caller should fall back to naive extraction).
    """
    if not text or len(text.strip()) < 10:
        return None

    raw_response = _ollama_chat(EXTRACTION_SYSTEM_PROMPT, text)

    if raw_response is None:
        return None

    # Parse the JSON array from the response
    concepts = _parse_concept_response(raw_response)

    if concepts and len(concepts) > 0:
        logger.info(f"Steward extracted {len(concepts)} concepts from {len(text)} chars of text")
        return concepts

    logger.warning(f"Steward failed to parse concepts from response: {raw_response[:200]}")
    return None


def _parse_concept_response(response: str) -> Optional[List[str]]:
    """
    Parse the LLM's response into a list of concept strings.
    Handles various response formats: raw JSON, markdown-wrapped JSON,
    thinking-mode output with <think> blocks, etc.
    """
    cleaned = response.strip()

    # Strip <think>...</think> blocks (Qwen3 thinking mode)
    if "<think>" in cleaned:
        import re
        cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()

    # Strip markdown code fences
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        # Remove first and last lines if they're fences
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Try direct JSON parse
    try:
        result = json.loads(cleaned)
        if isinstance(result, list):
            return [str(item).strip() for item in result if isinstance(item, str) and item.strip()]
    except json.JSONDecodeError:
        pass

    # Try to find a JSON array anywhere in the response
    import re
    array_match = re.search(r'\[.*?\]', cleaned, re.DOTALL)
    if array_match:
        try:
            result = json.loads(array_match.group())
            if isinstance(result, list):
                return [str(item).strip() for item in result if isinstance(item, str) and item.strip()]
        except json.JSONDecodeError:
            pass

    return None


# ---------------------------------------------------------------------------
# Maintenance Functions
# ---------------------------------------------------------------------------

def run_maintenance(neural_web_path: Path, days_threshold: int = 7, decay_amount: float = 0.01,
                    prune_threshold: float = 0.05) -> Dict[str, Any]:
    """
    Run periodic maintenance on the neural web:
      1. Apply time decay to stale connections
      2. Prune very weak synapses
      3. Identify and report noise neurons (high frequency, low specificity)

    Returns a summary dict of actions taken.
    """
    # Import neural web (same path resolution as mcp_server.py)
    rel_path = neural_web_path.parent.parent  # data/neural_web -> data -> REL root
    if str(rel_path) not in sys.path:
        sys.path.insert(0, str(rel_path))

    try:
        from neural_web import NeuralWeb, get_neural_web
    except ImportError:
        try:
            from neural_web_typed import NeuralWeb, get_neural_web
        except ImportError:
            return {"error": "Could not import neural web module"}

    nw = get_neural_web(neural_web_path)
    stats_before = nw.get_stats()

    # 1. Apply decay
    nw.apply_decay(days_threshold=days_threshold, decay_amount=decay_amount)

    # 2. Identify noise neurons (high activation count but generic concepts)
    noise_words = {
        "rob", "session", "claude", "corwin", "all", "new", "work", "working",
        "complete", "completed", "built", "building", "also", "using", "used",
        "system", "project", "update", "updated", "added", "based", "still",
        "current", "currently", "ready", "first", "started", "now", "back",
        "need", "needs", "next", "got", "made", "make", "run", "running",
        "set", "test", "testing", "fix", "fixed", "full", "then", "after",
    }

    noise_neurons = []
    for neuron_id, neuron in nw.neurons.items():
        concept = neuron.concept.lower() if hasattr(neuron, 'concept') else ""
        if concept in noise_words and neuron.activations > 5:
            noise_neurons.append({
                "id": neuron_id,
                "concept": concept,
                "activations": neuron.activations
            })

    # 3. Save
    nw.save()
    stats_after = nw.get_stats()

    return {
        "stats_before": stats_before,
        "stats_after": stats_after,
        "noise_neurons_found": len(noise_neurons),
        "noise_neurons": noise_neurons[:20],  # Cap report at 20
        "decay_applied": True,
        "days_threshold": days_threshold,
    }


def reprocess_history(session_log_path: Path, neural_web_path: Path,
                      clear_existing: bool = False) -> Dict[str, Any]:
    """
    Batch-reprocess all historical sessions through LLM concept extraction.
    This fixes the existing noise problem by re-learning everything with clean concepts.

    Args:
        session_log_path: Path to SessionLog.json
        neural_web_path: Path to neural_web directory
        clear_existing: If True, wipe the neural web before reprocessing
    """
    if not _ollama_available():
        return {"error": "Ollama is not available. Cannot reprocess without LLM."}

    # Load session log
    try:
        with open(session_log_path, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"error": f"Could not read session log: {e}"}

    sessions = log_data.get("sessions", [])
    if not sessions:
        return {"error": "No sessions found in log"}

    # Import neural web
    rel_path = neural_web_path.parent.parent
    if str(rel_path) not in sys.path:
        sys.path.insert(0, str(rel_path))

    try:
        from neural_web import NeuralWeb, get_neural_web
    except ImportError:
        from neural_web_typed import NeuralWeb, get_neural_web

    nw = get_neural_web(neural_web_path)

    # Optionally clear existing data
    if clear_existing:
        nw.neurons.clear()
        nw.synapses.clear()
        nw.concept_to_neuron.clear()
        logger.info("Cleared existing neural web data for fresh reprocessing")

    processed = 0
    failed = 0
    total_concepts = 0

    for session in sessions:
        summary = session.get("summary", "")
        if not summary or len(summary.strip()) < 10:
            continue

        # Also include achievements if present
        achievements = session.get("achievements", [])
        if achievements:
            full_text = summary + " | Achievements: " + "; ".join(achievements)
        else:
            full_text = summary

        concepts = extract_concepts_llm(full_text)

        if concepts:
            neuron_ids = nw.activate_neurons(concepts)
            nw.strengthen_connections(neuron_ids)
            total_concepts += len(concepts)
            processed += 1
        else:
            # Fallback to naive extraction for this session
            nw.learn_from_text(summary)
            failed += 1

        # Small delay to not hammer Ollama
        time.sleep(0.1)

    nw.save()
    stats = nw.get_stats()

    return {
        "sessions_total": len(sessions),
        "sessions_processed_llm": processed,
        "sessions_fallback_naive": failed,
        "total_concepts_extracted": total_concepts,
        "neural_web_stats": stats,
    }


# ---------------------------------------------------------------------------
# CLI Interface (for standalone operation)
# ---------------------------------------------------------------------------

def main():
    """Run steward maintenance tasks from the command line."""
    import argparse

    parser = argparse.ArgumentParser(description="REL Steward — Neural web maintenance agent")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check if Ollama is available and model is pulled")

    # Maintain command
    maintain_parser = subparsers.add_parser("maintain", help="Run decay and noise detection")
    maintain_parser.add_argument("--days", type=int, default=7, help="Days threshold for decay (default: 7)")
    maintain_parser.add_argument("--decay", type=float, default=0.01, help="Decay amount (default: 0.01)")

    # Reprocess command
    reprocess_parser = subparsers.add_parser("reprocess", help="Reprocess all sessions through LLM extraction")
    reprocess_parser.add_argument("--clear", action="store_true", help="Clear neural web before reprocessing")

    # Test extraction command
    test_parser = subparsers.add_parser("test", help="Test concept extraction on sample text")
    test_parser.add_argument("text", nargs="?", default=None, help="Text to extract concepts from")

    args = parser.parse_args()

    # Setup logging for CLI
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # Resolve paths
    rel_path = Path(__file__).resolve().parent
    data_path = rel_path / "data"
    neural_web_path = data_path / "neural_web"
    session_log_path = data_path / "SessionLog.json"

    if args.command == "check":
        available = _ollama_available()
        if available:
            print(f"Ollama is running and '{OLLAMA_MODEL}' is available.")
            # Quick test
            result = extract_concepts_llm("Built a FAISS brain for semantic search using sentence-transformers.")
            if result:
                print(f"Test extraction successful: {result}")
            else:
                print("WARNING: Extraction test failed.")
        else:
            print(f"Ollama is NOT available or '{OLLAMA_MODEL}' is not pulled.")
            print(f"Run: ollama pull {OLLAMA_MODEL}")
        sys.exit(0 if available else 1)

    elif args.command == "maintain":
        print(f"Running maintenance (decay threshold: {args.days} days, decay amount: {args.decay})...")
        result = run_maintenance(neural_web_path, days_threshold=args.days, decay_amount=args.decay)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == "reprocess":
        if args.clear:
            confirm = input("This will CLEAR the neural web and reprocess everything. Are you sure? (yes/no): ")
            if confirm.lower() != "yes":
                print("Cancelled.")
                sys.exit(0)
        print(f"Reprocessing {session_log_path}...")
        print("This may take a few minutes depending on session count...")
        result = reprocess_history(session_log_path, neural_web_path, clear_existing=args.clear)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == "test":
        if not _ollama_available():
            print(f"Ollama not available. Run: ollama pull {OLLAMA_MODEL}")
            sys.exit(1)
        text = args.text or "Built the Living Villages v2 mod using NeoForge and Kotlin. Module 1 Phase 1 complete with villager identity attachments, personality generation, and client-side name rendering."
        print(f"Input: {text}\n")
        concepts = extract_concepts_llm(text)
        if concepts:
            print(f"Extracted {len(concepts)} concepts:")
            for c in concepts:
                print(f"  - {c}")
        else:
            print("Extraction failed.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
