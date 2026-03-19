from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from forex_model.config import load_settings
from forex_model.pipeline import predict_latest

app = FastAPI(title="Forex Multi-Timeframe Predictor", version="1.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/predict")
def predict() -> dict:
    try:
        settings = load_settings()
        return {
            "pair": settings.forex_pair,
            "predictions": predict_latest(settings),
        }
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
