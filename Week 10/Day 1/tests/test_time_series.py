import pandas as pd
import pytest

from time_series_analysis import (
    load_data,
    prepare_monthly_series,
    check_stationarity,
    fit_arima_and_forecast,
)


def test_load_data():
    df = load_data()
    assert not df.empty
    assert "Date" in df.columns
    assert "Sales" in df.columns


def test_prepare_monthly_series():
    df = pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-05",
            "2026-01-12",
            "2026-02-03",
        ]),
        "Sales": [1000, 2000, 3000],
    })

    monthly = prepare_monthly_series(df)

    assert len(monthly) == 2
    assert monthly.iloc[0] == 3000
    assert monthly.iloc[1] == 3000
    assert monthly.index.freqstr == "MS"


def test_check_stationarity():
    series = pd.Series([
        10, 12, 9, 11, 8, 10, 7, 9, 6, 8,
        5, 7, 4, 6, 3, 5, 2, 4, 1, 3
    ])

    result = check_stationarity(series)

    assert "p_value" in result
    assert "stationary" in result


def test_arima_forecast():
    index = pd.date_range(
        start="2025-01-01",
        periods=12,
        freq="MS",
    )
    series = pd.Series(
        [100, 110, 105, 115, 108, 120,
         112, 125, 118, 130, 122, 135],
        index=index,
    )

    model, forecast = fit_arima_and_forecast(series, steps=3)

    assert len(forecast) == 3
    assert forecast.notna().all()
    assert model is not None


def test_arima_requires_six_observations():
    series = pd.Series(
        [100, 110, 105, 115, 108],
        index=pd.date_range("2025-01-01", periods=5, freq="MS"),
    )

    with pytest.raises(ValueError):
        fit_arima_and_forecast(series)
