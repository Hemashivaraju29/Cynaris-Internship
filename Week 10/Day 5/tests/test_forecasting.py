
import pandas as pd
import pytest

from forecasting_utils import (
    load_sales_data,
    filter_sales_data,
    aggregate_monthly_sales,
    forecast_sales,
    evaluate_forecast,
)


@pytest.fixture
def sample_sales():
    return pd.DataFrame({
        "Date": pd.to_datetime([
            "2026-01-05", "2026-02-10",
            "2026-03-15", "2026-04-12",
            "2026-05-20", "2026-06-18"
        ]),
        "Region": [
            "North", "South", "North",
            "West", "South", "East"
        ],
        "Category": [
            "Electronics", "Grocery", "Clothing",
            "Electronics", "Grocery", "Furniture"
        ],
        "Sales": [10000, 12000, 15000, 11000, 14000, 16000],
        "Units Sold": [10, 20, 15, 11, 14, 16]
    })


def test_load_sales_data():
    df = load_sales_data()

    assert len(df) == 24
    assert "Date" in df.columns
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])


def test_filter_sales_data(sample_sales):
    filtered = filter_sales_data(
        sample_sales, region="North"
    )

    assert len(filtered) == 2
    assert all(filtered["Region"] == "North")


def test_filter_by_category(sample_sales):
    filtered = filter_sales_data(
        sample_sales, category="Grocery"
    )

    assert len(filtered) == 2
    assert all(filtered["Category"] == "Grocery")


def test_monthly_aggregation(sample_sales):
    monthly = aggregate_monthly_sales(sample_sales)

    assert len(monthly) == 6
    assert monthly["Sales"].sum() == 78000
    assert list(monthly.columns) == ["Month", "Sales"]


def test_forecast_sales(sample_sales):
    monthly = aggregate_monthly_sales(sample_sales)

    forecast = forecast_sales(
        monthly, periods=3, window=3
    )

    assert len(forecast) == 3
    assert list(forecast.columns) == ["Month", "Forecast Sales"]
    assert forecast["Forecast Sales"].notna().all()
    assert forecast["Forecast Sales"].ge(0).all()


def test_forecast_invalid_window(sample_sales):
    monthly = aggregate_monthly_sales(sample_sales)

    with pytest.raises(ValueError):
        forecast_sales(monthly, periods=3, window=10)


def test_evaluate_forecast(sample_sales):
    monthly = aggregate_monthly_sales(sample_sales)

    metrics = evaluate_forecast(
        monthly, window=3, test_size=3
    )

    assert metrics["MAE"] >= 0
    assert metrics["RMSE"] >= 0


def test_load_invalid_file(tmp_path):
    invalid_file = tmp_path / "invalid.csv"
    pd.DataFrame({"Date": ["2026-01-01"]}).to_csv(
        invalid_file, index=False
    )

    with pytest.raises(ValueError):
        load_sales_data(invalid_file)
