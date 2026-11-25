"""
Shared utilities for pipeline stages:
- Schema validation
- Hash-based caching
- runs.jsonl logging
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STORYBOARD_PATH = PROJECT_ROOT / "storyboard.json"
SCHEMA_PATH = PROJECT_ROOT / "schema" / "storyboard.schema.json"
RUNS_LOG_PATH = PROJECT_ROOT / "runs.jsonl"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def load_env_file() -> None:
    """Load key-value pairs from .env into os.environ."""
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip().strip("'\"")

load_env_file()


def load_storyboard() -> Dict[str, Any]:
    """Load and return the central storyboard contract."""
    if not STORYBOARD_PATH.exists():
        raise FileNotFoundError(f"Storyboard contract not found at {STORYBOARD_PATH}")
    with open(STORYBOARD_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_storyboard(storyboard: Optional[Dict[str, Any]] = None) -> bool:
    """Validate storyboard against JSON Schema."""
    if storyboard is None:
        storyboard = load_storyboard()
    
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    try:
        import jsonschema
        jsonschema.validate(instance=storyboard, schema=schema)
        return True
    except ImportError:
        # Fallback basic structural validation if jsonschema package is not installed yet
        required_keys = ["title", "logline", "total_duration_seconds", "language", "shots", "characters"]
        for key in required_keys:
            if key not in storyboard:
                raise ValueError(f"Missing required key in storyboard: {key}")
        if not (60.0 <= storyboard["total_duration_seconds"] <= 90.0):
            raise ValueError("Duration must be between 60 and 90 seconds")
        if len(storyboard["shots"]) < 8:
            raise ValueError("Storyboard must contain at least 8 shots")
        return True


def compute_hash(payload: Any) -> str:
    """Compute deterministic SHA-256 hash of any JSON-serializable dictionary or string."""
    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def log_run(
    stage: str,
    model: str,
    parameters: Dict[str, Any],
    seed: int,
    latency_seconds: float,
    cost_usd: float = 0.0,
    status: str = "success",
    extra: Optional[Dict[str, Any]] = None
) -> None:
    """Log model execution line to runs.jsonl."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "model": model,
        "parameters": parameters,
        "seed": seed,
        "latency_seconds": round(latency_seconds, 3),
        "cost_usd": cost_usd,
        "status": status
    }
    if extra:
        entry.update(extra)
    
    with open(RUNS_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
