
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = (
    PROJECT_ROOT / "Week 07" / "Day 3" / "Sales_Data.csv"
)


def load_sales_data(file_path=DEFAULT_DATA_PATH):
    """Load and validate the sales dataset."""
    df = pd.read_csv(file_path)

    required_columns = {
        "Date", "Region", "Category", "Sales", "Units Sold"
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df["Units Sold"] = pd.to_numeric(
        df["Units Sold"], errors="coerce"
    )

    df = df.dropna(
        subset=["Date", "Sales", "Units Sold", "Region", "Category"]
    )

    if df.empty:
        raise ValueError("No valid sales records found.")

    return df.sort_values("Date").reset_index(drop=True)


def filter_sales_data(df, region="All", category="All"):
    """Filter sales records by region and category."""
    filtered = df.copy()

    if region != "All":
        filtered = filtered[
            filtered["Region"].astype(str) == region
        ]

    if category != "All":
        filtered = filtered[
            filtered["Category"].astype(str) == category
        ]

    return filtered


def aggregate_monthly_sales(df):
    """Aggregate sales into monthly totals."""
    if df.empty:
        raise ValueError("Cannot aggregate an empty dataset.")

    monthly = (
        df.set_index("Date")["Sales"]
        .resample("MS")
        .sum()
        .asfreq("MS", fill_value=0)
        .reset_index()
    )

    monthly.columns = ["Month", "Sales"]
    return monthly


def forecast_sales(monthly_data, periods=3, window=3):
    """Forecast future sales using a recursive moving average."""
    if periods < 1 or window < 1:
        raise ValueError("Periods and window must be positive.")

    if len(monthly_data) < window:
        raise ValueError(
            f"At least {window} months of data are required."
        )

    history = monthly_data["Sales"].astype(float).tolist()
    last_month = pd.to_datetime(monthly_data["Month"].max())

    forecasts = []

    for step in range(1, periods + 1):
        prediction = float(np.mean(history[-window:]))
        history.append(prediction)

        forecasts.append({
            "Month": last_month + pd.DateOffset(months=step),
            "Forecast Sales": prediction
        })

    return pd.DataFrame(forecasts)


def evaluate_forecast(monthly_data, window=3, test_size=3):
    """Evaluate the moving-average model on historical holdout months."""
    if len(monthly_data) <= window:
        raise ValueError("Insufficient data for forecast evaluation.")

    if test_size < 1 or len(monthly_data) < window + test_size:
        raise ValueError("Insufficient data for the selected test size.")

    train = monthly_data.iloc[:-test_size]
    actual = monthly_data.iloc[-test_size:]["Sales"].astype(float).tolist()

    history = train["Sales"].astype(float).tolist()
    predictions = []

    for _ in actual:
        prediction = float(np.mean(history[-window:]))
        predictions.append(prediction)
        history.append(prediction)

    mae = mean_absolute_error(actual, predictions)
    rmse = float(np.sqrt(mean_squared_error(actual, predictions)))

    return {
        "MAE": float(mae),
        "RMSE": rmse
    }

