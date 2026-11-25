
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent

HISTORICAL_DATA_PATH = (
    PROJECT_ROOT
    / "Week 07"
    / "Day 1"
    / "nifty500_combined_eda.csv"
)

FORECAST_PATH = (
    PROJECT_ROOT
    / "Week 10"
    / "Day 2"
    / "output"
    / "future_forecast.csv"
)

METRICS_PATH = (
    PROJECT_ROOT
    / "Week 10"
    / "Day 2"
    / "output"
    / "evaluation_metrics.csv"
)


def load_historical_data(file_path=HISTORICAL_DATA_PATH, company="Reliance"):
    """Load and prepare historical stock closing prices."""

    df = pd.read_csv(file_path)

    required = {"Date", "Close", "Company"}

    if not required.issubset(df.columns):
        raise ValueError("Dataset must contain Date, Close and Company columns.")

    df = df[df["Company"].str.lower() == company.lower()].copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date")

    if df.empty:
        raise ValueError(f"No valid historical data found for {company}.")

    return df[["Date", "Close"]].reset_index(drop=True)


def load_forecast(file_path=FORECAST_PATH):
    """Load future forecast with prediction intervals."""

    df = pd.read_csv(file_path)

    required = {"ds", "yhat", "yhat_lower", "yhat_upper"}

    if not required.issubset(df.columns):
        raise ValueError("Forecast file is missing required columns.")

    df["ds"] = pd.to_datetime(df["ds"], errors="coerce")

    for column in ["yhat", "yhat_lower", "yhat_upper"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(
        subset=["ds", "yhat", "yhat_lower", "yhat_upper"]
    )

    return df.sort_values("ds").reset_index(drop=True)


def load_metrics(file_path=METRICS_PATH):
    """Load forecasting evaluation metrics."""

    df = pd.read_csv(file_path)

    required = {"MAE", "RMSE", "MAPE"}

    if not required.issubset(df.columns):
        raise ValueError("Metrics file must contain MAE, RMSE and MAPE.")

    if df.empty:
        raise ValueError("Metrics file contains no evaluation results.")

    return df.iloc[0].to_dict()
