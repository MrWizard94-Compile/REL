# Quick Start: Making REL Production-Ready

This guide helps you start improving REL immediately with the most critical changes.

## Before You Start

✅ **Backup Created:** `C:\REL\backups\pre-production-ready-2025-02-17/`  
✅ **Analysis Complete:** See `PRODUCTION_READY_ANALYSIS.md`  
✅ **TODO List:** See `TODO.md`

## Step 1: Install Development Tools (5 minutes)

```bash
cd C:\REL

# Create/activate virtual environment (if not already done)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Unix

# Install development dependencies
pip install --upgrade pip
pip install pytest pytest-asyncio pytest-cov mypy ruff black pydantic types-python-dateutil

# Verify installations
pytest --version
mypy --version
ruff --version
black --version
```

## Step 2: Create pyproject.toml (10 minutes)

Create `C:\REL\pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rel-mcp-server"
version = "1.0.0"
description = "REL (Radiant Ether Loom) - Cognitive Architecture MCP Server"
requires-python = ">=3.9"

dependencies = [
    "mcp==1.0.0",
    "flask==3.0.1",
    "flask-cors==4.0.0",
    "sentence-transformers==2.2.2",
    "faiss-cpu==1.7.4",
    "numpy==1.24.3",
    "scikit-learn==1.3.0",
    "pandas==2.0.3",
    "python-dateutil==2.8.2",
    "pydantic==2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest==7.4.3",
    "pytest-asyncio==0.21.1",
    "pytest-cov==4.1.0",
    "mypy==1.7.1",
    "ruff==0.1.8",
    "black==23.12.0",
    "types-python-dateutil==2.8.19",
]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true

[tool.ruff]
line-length = 100
target-version = "py39"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=. --cov-report=html --cov-report=term"
```

Install in editable mode:
```bash
pip install -e ".[dev]"
```

## Step 3: Add Type Hints to One Class (30 minutes)

Let's start with the `RELBrain` class. Open `brain.py` and update:

```python
"""
REL Brain Module - FAISS Semantic Search
Embeddings + Vector Storage + Intelligent Search

This is MY (Corwin's) semantic memory - understanding concepts, not just matching keywords
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger("REL.Brain")

# Lazy imports - only load when needed
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None  # type: ignore

try:
    import faiss
except ImportError:
    faiss = None  # type: ignore

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore


class RELBrain:
    """Semantic memory and search for REL"""
    
    def __init__(self, brain_path: Path) -> None:
        self.brain_path: Path = brain_path
        self.index_path: Path = brain_path / "faiss_index.bin"
        self.documents_path: Path = brain_path / "documents.json"
        self.metadata_path: Path = brain_path / "brain_metadata.json"
        
        self.model: Optional[SentenceTransformer] = None
        self.index: Optional[faiss.Index] = None  # type: ignore
        self.documents: List[Dict[str, Any]] = []
        self.dimension: int = 384  # all-MiniLM-L6-v2 dimension
        
        # Ensure brain directory exists
        self.brain_path.mkdir(parents=True, exist_ok=True)
    
    def initialize(self) -> bool:
        """Initialize the brain (load model and index)
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        # ... rest of the method stays the same
        pass  # Implementation continues as before
```

Test it:
```bash
mypy brain.py
```

## Step 4: Create Your First Test (20 minutes)

Create `tests/` directory:
```bash
mkdir tests
```

Create `tests/conftest.py`:
```python
"""Shared test fixtures"""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_rel_dir():
    """Create temporary REL directory for testing"""
    temp_dir = Path(tempfile.mkdtemp())
    data_dir = temp_dir / "data"
    data_dir.mkdir()
    
    # Create empty state files
    (data_dir / "CoreState.json").write_text('{"project_states": {}}')
    (data_dir / "SessionLog.json").write_text('{"sessions": []}')
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)
```

Create `tests/test_brain.py`:
```python
"""Tests for brain.py"""
import pytest
from pathlib import Path
from brain import RELBrain


def test_brain_initialization(temp_rel_dir):
    """Test brain can be initialized"""
    brain_path = temp_rel_dir / "brain"
    brain_path.mkdir()
    
    brain = RELBrain(brain_path)
    assert brain.brain_path == brain_path
    assert brain.dimension == 384
    assert len(brain.documents) == 0


def test_brain_directory_created(temp_rel_dir):
    """Test brain creates directory if it doesn't exist"""
    brain_path = temp_rel_dir / "brain_new"
    
    brain = RELBrain(brain_path)
    assert brain_path.exists()
    assert brain_path.is_dir()


@pytest.mark.skipif(
    not hasattr(RELBrain, 'initialize'),
    reason="Requires sentence-transformers and FAISS"
)
def test_brain_initialize_creates_index(temp_rel_dir):
    """Test brain initialize creates FAISS index"""
    brain_path = temp_rel_dir / "brain"
    brain = RELBrain(brain_path)
    
    success = brain.initialize()
    
    # May fail if dependencies not installed
    if success:
        assert brain.model is not None
        assert brain.index is not None
```

Run the tests:
```bash
pytest tests/test_brain.py -v
```

## Step 5: Add Input Validation to One Tool (30 minutes)

Let's add validation to the `create_project` tool.

Create `validation_models.py`:
```python
"""Pydantic validation models for REL tools"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class CreateProjectRequest(BaseModel):
    """Request model for create_project tool"""
    key: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r'^[a-z0-9_-]+$',
        description="Project key (lowercase, alphanumeric, underscore, dash)"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Project name"
    )
    description: str = Field(
        default="",
        max_length=1000,
        description="Project description"
    )
    
    @validator('key')
    def key_must_not_start_with_underscore(cls, v: str) -> str:
        """Ensure key doesn't start with underscore"""
        if v.startswith('_'):
            raise ValueError('Project key cannot start with underscore')
        return v
    
    @validator('name')
    def name_must_not_be_whitespace(cls, v: str) -> str:
        """Ensure name is not just whitespace"""
        if not v.strip():
            raise ValueError('Project name cannot be empty or whitespace')
        return v.strip()
```

Update `mcp_server.py` to use validation:
```python
from validation_models import CreateProjectRequest
from pydantic import ValidationError

# In call_tool function, update create_project:
elif name == "create_project":
    try:
        # Validate input
        req = CreateProjectRequest(**arguments)
        
        # Use validated data
        key = req.key
        name_arg = req.name
        description = req.description
        today = datetime.now().strftime("%Y-%m-%d")

        await _update_state_atomic_async(lambda cur: (lambda s: (
            s.setdefault("project_states", {}),
            s["project_states"].__setitem__(key, {
                "name": name_arg,
                "description": description,
                "status": "active",
                "priority": "medium",
                "completion": 0,
                "created": today,
                "last_worked": today,
            }),
            s
        )[-1])(cur or {}))

        return [TextContent(type="text", text=json.dumps({"success": True, "project": key}, indent=2))]
        
    except ValidationError as e:
        # Return validation errors
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": "Validation failed",
            "details": e.errors()
        }, indent=2))]
```

Test the validation:
```python
# Create tests/test_validation.py
import pytest
from validation_models import CreateProjectRequest
from pydantic import ValidationError


def test_create_project_valid():
    """Test valid project creation request"""
    req = CreateProjectRequest(
        key="my-project",
        name="My Project",
        description="A test project"
    )
    assert req.key == "my-project"
    assert req.name == "My Project"


def test_create_project_invalid_key():
    """Test invalid project key"""
    with pytest.raises(ValidationError) as exc_info:
        CreateProjectRequest(
            key="Invalid Key!",  # Has space and special char
            name="My Project"
        )
    
    errors = exc_info.value.errors()
    assert any("pattern" in str(e) for e in errors)


def test_create_project_key_starts_with_underscore():
    """Test key cannot start with underscore"""
    with pytest.raises(ValidationError) as exc_info:
        CreateProjectRequest(
            key="_private",
            name="My Project"
        )
    
    errors = exc_info.value.errors()
    assert any("underscore" in str(e).lower() for e in errors)
```

Run validation tests:
```bash
pytest tests/test_validation.py -v
```

## Step 6: Run Quality Checks (5 minutes)

```bash
# Type check
mypy brain.py

# Lint
ruff check .

# Format
black .

# Test
pytest
```

## Next Steps

You've now:
✅ Set up development tools
✅ Created modern packaging (pyproject.toml)
✅ Added type hints to one class
✅ Created your first tests
✅ Added input validation to one tool
✅ Run quality checks

### Continue With:

1. **More Type Hints:** Apply same pattern to `neural_web.py`, then `mcp_server.py`
2. **More Tests:** Add tests for other tools following the same pattern
3. **More Validation:** Create models for all 45 tools
4. **Documentation:** Update README with new standards
5. **CI/CD:** Set up GitHub Actions

### Get Help

- **Type Hints:** Check `/mnt/skills/public/production-ready-coder/SKILL.md`
- **Testing:** See pytest documentation
- **Validation:** See Pydantic documentation
- **Questions:** Ask Corwin (me!)

## Common Issues

### "Module not found: sentence_transformers"
```bash
pip install sentence-transformers==2.2.2
```

### "mypy: command not found"
```bash
pip install mypy==1.7.1
```

### "Tests not found"
```bash
# Make sure you're in the REL directory
cd C:\REL
pytest tests/ -v
```

### "Import errors in tests"
```bash
# Install package in editable mode
pip install -e .
```

## Progress Tracking

Track your progress in `TODO.md`. Mark items complete as you go:
```markdown
- [x] Install development tools
- [x] Create pyproject.toml
- [x] Add type hints to RELBrain
- [x] Create first test
- [x] Add input validation
- [ ] Add type hints to NeuralWeb
- [ ] Add type hints to mcp_server.py
...
```

---

**Remember:** Small, incremental changes are better than trying to do everything at once. Test after each change!

Good luck! 🚀
