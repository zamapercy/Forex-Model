from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from forex_model.config import load_settings
from forex_model.pipeline import run_training_pipeline


if __name__ == "__main__":
    settings = load_settings()
    results = run_training_pipeline(settings)
    print(json.dumps(results, indent=2))
