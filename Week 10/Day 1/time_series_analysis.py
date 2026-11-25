from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

warnings.filterwarnings("ignore")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def load_data(file_path=DATA_PATH):
    df = pd.read_csv(file_path)

    required_columns = {"Date", "Sales"}
    if not required_columns.issubset(df.columns):
        raise ValueError("Dataset must contain Date and Sales columns.")

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
    df = df.dropna(subset=["Date", "Sales"])

    if df.empty:
        raise ValueError("No valid date and sales records found.")

    return df.sort_values("Date")


def prepare_monthly_series(df):
    monthly = (
        df.set_index("Date")["Sales"]
        .resample("MS")
        .sum()
        .asfreq("MS", fill_value=0)
    )
    monthly.name = "Sales"
    return monthly


def check_stationarity(series):
    if len(series) < 4 or series.nunique() < 2:
        return {
            "adf_statistic": None,
            "p_value": None,
            "stationary": None,
        }

    result = adfuller(series, autolag="AIC")

    return {
        "adf_statistic": float(result[0]),
        "p_value": float(result[1]),
        "stationary": bool(result[1] < 0.05),
    }


def fit_arima_and_forecast(series, steps=3):
    if len(series) < 6:
        raise ValueError("At least 6 monthly observations are required.")

    model = ARIMA(series, order=(1, 1, 1))
    fitted_model = model.fit()

    forecast = fitted_model.forecast(steps=steps)
    forecast.index = pd.date_range(
        start=series.index[-1] + pd.offsets.MonthBegin(1),
        periods=steps,
        freq="MS",
    )

    return fitted_model, forecast


def save_outputs(monthly, stationarity, forecast):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", header=True)
    forecast.rename("Forecast_Sales").to_csv(
        OUTPUT_DIR / "sales_forecast.csv",
        header=True,
    )

    pd.DataFrame([stationarity]).to_csv(
        OUTPUT_DIR / "stationarity_test.csv",
        index=False,
    )

    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sales_trend.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly.values, marker="o", label="Actual Sales")
    plt.plot(
        forecast.index,
        forecast.values,
        marker="o",
        linestyle="--",
        label="ARIMA Forecast",
    )
    plt.title("Monthly Sales Forecast using ARIMA")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "arima_forecast.png")
    plt.close()


def main():
    print("Loading sales dataset...")
    df = load_data()

    print("Preparing monthly sales data...")
    monthly = prepare_monthly_series(df)

    print("\nMonthly Sales:")
    print(monthly.to_string())

    print("\nChecking stationarity...")
    stationarity = check_stationarity(monthly)
    print(stationarity)

    print("\nFitting ARIMA model...")
    model, forecast = fit_arima_and_forecast(monthly)

    print("\nARIMA Model Summary:")
    print(model.summary())

    print("\nNext 3 Months Sales Forecast:")
    print(forecast.to_string())

    save_outputs(monthly, stationarity, forecast)

    print(f"\nAnalysis completed. Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
