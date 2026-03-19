# Forex Multi-Timeframe Predictor

This project trains forecasting models for forex behavior across multiple horizons:
- 5 minutes
- 10 minutes
- 15 minutes
- 1 hour
- 24 hours

The tool outputs:
- `prob_up` and `prob_down` per horizon
- `expected_return` for the next bar in that horizon
- direction signal (`up` / `down`)
- walk-forward backtest metrics

## How it works
1. Pulls market data from Yahoo Finance (`yfinance`) for a pair like `EURUSD=X`.
2. Builds OHLCV-based and time-based features.
3. Trains two models per horizon:
   - classifier for direction probability
   - regressor for expected return size
4. Runs walk-forward backtesting with transaction cost assumptions.
5. Saves model artifacts and report files.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Train models

```powershell
python train.py
```

Outputs:
- `models/model_<horizon>.joblib`
- `models/meta_<horizon>.json`
- `reports/training_report.json`

## Get latest predictions (CLI)

```powershell
python predict.py
```

## Run API

```powershell
uvicorn api:app --reload
```

Then open:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/predict`

## Run Streamlit app

```powershell
streamlit run streamlit_app.py
```

The app lets you:
- train/retrain all horizon models
- see latest predictions in a table
- view raw JSON outputs

## Deploy on Streamlit Community Cloud
1. Push this project to a GitHub repository.
2. In Streamlit Community Cloud, create a new app.
3. Set the main file path to `streamlit_app.py`.
4. Make sure `requirements.txt` is detected.
5. Add secrets or environment variables if you customize settings.

## Environment variables (`.env`)
- `FOREX_PAIR` default `EURUSD=X`
- `BASE_INTERVAL` default `5m`
- `TRAIN_PERIOD` default `60d`
- `COST_BPS` default `1.0`
- `MODEL_DIR` default `models`
- `DATA_DIR` default `data`
- `REPORT_DIR` default `reports`

## Notes
- This is a probabilistic forecasting tool, not guaranteed prediction.
- Real trading requires slippage, spread, and execution modeling beyond this baseline.
