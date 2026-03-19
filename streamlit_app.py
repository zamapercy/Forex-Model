from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent


def _bootstrap_src_path() -> None:
	# Streamlit Cloud may launch from different working directories, so try a few common src paths.
	candidates = [
		ROOT / "src",
		Path.cwd() / "src",
		ROOT.parent / "src",
	]
	for candidate in candidates:
		if candidate.exists() and candidate.is_dir():
			candidate_str = str(candidate)
			if candidate_str not in sys.path:
				sys.path.insert(0, candidate_str)


_bootstrap_src_path()

try:
	from forex_model.config import load_settings
	from forex_model.pipeline import predict_latest, run_training_pipeline
except ModuleNotFoundError:
	_bootstrap_src_path()
	from forex_model.config import load_settings
	from forex_model.pipeline import predict_latest, run_training_pipeline

st.set_page_config(page_title="Forex Multi-Timeframe Predictor", layout="wide")

st.title("Forex Multi-Timeframe Predictor")
st.caption("Forecast probabilities and expected returns for 5m, 10m, 15m, 1h, and 24h horizons.")


def _format_percent(value: float) -> str:
	return f"{value * 100:.2f}%"


settings = load_settings()

with st.sidebar:
	st.header("Configuration")
	st.write(f"Pair: {settings.forex_pair}")
	st.write(f"Base Interval: {settings.base_interval}")
	st.write(f"Train Period: {settings.train_period}")
	st.write(f"Transaction Cost: {settings.cost_bps} bps")

	retrain_clicked = st.button("Train / Retrain Models", type="primary")


if retrain_clicked:
	with st.spinner("Training models and running walk-forward backtests..."):
		try:
			results = run_training_pipeline(settings)
			st.success("Training complete.")
			st.json(results)
		except Exception as exc:
			st.error(f"Training failed: {exc}")


st.subheader("Latest Predictions")

try:
	predictions = predict_latest(settings)
	df = pd.DataFrame(predictions)

	if not df.empty:
		df["prob_up_pct"] = df["prob_up"].apply(_format_percent)
		df["prob_down_pct"] = df["prob_down"].apply(_format_percent)
		df["expected_return_pct"] = df["expected_return"].apply(_format_percent)

		display_cols = [
			"horizon",
			"timestamp",
			"direction",
			"prob_up_pct",
			"prob_down_pct",
			"expected_return_pct",
		]
		st.dataframe(df[display_cols], use_container_width=True, hide_index=True)

		c1, c2, c3 = st.columns(3)
		c1.metric("Avg Prob Up", _format_percent(float(df["prob_up"].mean())))
		c2.metric("Avg Expected Return", _format_percent(float(df["expected_return"].mean())))
		c3.metric("Generated At", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))

		st.markdown("### Raw JSON")
		st.code(json.dumps(predictions, indent=2), language="json")
	else:
		st.warning("No predictions available.")
except FileNotFoundError:
	st.info("Models not found yet. Click 'Train / Retrain Models' in the sidebar.")
except Exception as exc:
	st.error(f"Prediction failed: {exc}")

