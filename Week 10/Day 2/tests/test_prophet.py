import sys
from pathlib import Path

import pandas as pd

# Add the Day 2 project folder to Python's import path.
PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from prophet_forecasting import (
    load_and_prepare_data,
    evaluate_model,
    forecast_future,
    DATA_PATH
)


def test_load_and_prepare_data():
    """Check whether Reliance data loads correctly."""

    data = load_and_prepare_data(DATA_PATH)

    assert not data.empty
    assert list(data.columns) == ["ds", "y"]
    assert data["ds"].isna().sum() == 0
    assert data["y"].isna().sum() == 0
    assert data["ds"].is_monotonic_increasing


def test_reliance_record_count():
    """Verify the number of Reliance records."""

    data = load_and_prepare_data(DATA_PATH)

    assert len(data) == 2465


def test_evaluation_metrics():
    """Check whether model evaluation returns valid metrics."""

    data = load_and_prepare_data(DATA_PATH)
    metrics = evaluate_model(data)

    assert list(metrics.columns) == ["MAE", "RMSE", "MAPE"]
    assert len(metrics) == 1
    assert metrics.notna().all().all()
    assert (metrics >= 0).all().all()


def test_future_forecast():
    """Check whether Prophet generates 30 future forecasts."""

    data = load_and_prepare_data(DATA_PATH)
    model, forecast = forecast_future(data)

    assert len(forecast) == 30
    assert forecast["ds"].is_monotonic_increasing
    assert forecast["yhat"].notna().all()
    assert forecast["yhat_lower"].notna().all()
    assert forecast["yhat_upper"].notna().all()
    assert (forecast["yhat_lower"] <= forecast["yhat_upper"]).all()
    assert forecast["ds"].min() > data["ds"].max()
