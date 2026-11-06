
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dashboard_utils import (
    load_historical_data,
    load_forecast,
    load_metrics,
)


def test_load_historical_data(tmp_path):
    file_path = tmp_path / "historical.csv"

    data = pd.DataFrame({
        "Date": ["2021-01-02", "2021-01-01", "2021-01-03"],
        "Close": [200, 100, 300],
        "Company": ["Reliance", "Reliance", "TCS"],
    })

    data.to_csv(file_path, index=False)

    result = load_historical_data(file_path)

    assert len(result) == 2
    assert list(result.columns) == ["Date", "Close"]
    assert result["Close"].tolist() == [100, 200]


def test_load_forecast(tmp_path):
    file_path = tmp_path / "forecast.csv"

    data = pd.DataFrame({
        "ds": ["2022-01-02", "2022-01-01"],
        "yhat": [110, 100],
        "yhat_lower": [90, 80],
        "yhat_upper": [130, 120],
    })

    data.to_csv(file_path, index=False)

    result = load_forecast(file_path)

    assert len(result) == 2
    assert result["yhat"].tolist() == [100, 110]
    assert pd.api.types.is_datetime64_any_dtype(result["ds"])


def test_load_metrics(tmp_path):
    file_path = tmp_path / "metrics.csv"

    data = pd.DataFrame({
        "MAE": [319.42],
        "RMSE": [368.27],
        "MAPE": [15.98],
    })

    data.to_csv(file_path, index=False)

    result = load_metrics(file_path)

    assert result["MAE"] == pytest.approx(319.42)
    assert result["RMSE"] == pytest.approx(368.27)
    assert result["MAPE"] == pytest.approx(15.98)


def test_load_forecast_rejects_missing_columns(tmp_path):
    file_path = tmp_path / "invalid_forecast.csv"

    data = pd.DataFrame({
        "ds": ["2022-01-01"],
        "yhat": [100],
    })

    data.to_csv(file_path, index=False)

    with pytest.raises(ValueError):
        load_forecast(file_path)
