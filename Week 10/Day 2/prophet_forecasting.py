
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = (
    BASE_DIR.parent.parent
    / "Week 07"
    / "Day 1"
    / "nifty500_combined_eda.csv"
)
OUTPUT_DIR = BASE_DIR / "output"


def load_and_prepare_data(file_path=DATA_PATH):
    """Load and prepare Reliance stock data for Prophet."""

    df = pd.read_csv(file_path)

    df = df[df["Company"] == "Reliance"].copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date")

    prophet_df = df[["Date", "Close"]].rename(
        columns={
            "Date": "ds",
            "Close": "y"
        }
    )

    return prophet_df.reset_index(drop=True)


def evaluate_model(data):
    """Evaluate Prophet using the final 20% of historical data."""

    split_index = int(len(data) * 0.8)

    train = data.iloc[:split_index].copy()
    test = data.iloc[split_index:].copy()

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(train)

    predictions = model.predict(test[["ds"]])

    # Convert Series to NumPy arrays to avoid index alignment issues.
    actual = test["y"].to_numpy()
    predicted = predictions["yhat"].to_numpy()

    mae = mean_absolute_error(actual, predicted)

    rmse = mean_squared_error(
        actual,
        predicted
    ) ** 0.5

    # Avoid division by zero when calculating MAPE.
    non_zero_mask = actual != 0

    mape = (
        abs(
            (actual[non_zero_mask] - predicted[non_zero_mask])
            / actual[non_zero_mask]
        ).mean()
        * 100
    )

    metrics = pd.DataFrame([{
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape
    }])

    return metrics


def forecast_future(data):
    """Train on all historical data and forecast 30 business days."""

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(data)

    future_dates = pd.bdate_range(
        start=data["ds"].max() + pd.Timedelta(days=1),
        periods=30
    )

    future = pd.DataFrame({
        "ds": future_dates
    })

    forecast = model.predict(future)

    return model, forecast


def save_outputs(data, metrics, model, forecast):
    """Save evaluation results, forecasts and visualizations."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Save evaluation metrics.
    metrics.to_csv(
        OUTPUT_DIR / "evaluation_metrics.csv",
        index=False
    )

    # Save future forecast.
    forecast.to_csv(
        OUTPUT_DIR / "future_forecast.csv",
        index=False
    )

    # Historical stock price visualization.
    plt.figure(figsize=(12, 6))

    plt.plot(
        data["ds"],
        data["y"],
        label="Actual Closing Price"
    )

    plt.title("Reliance Historical Stock Prices (2012–2021)")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "historical_trend.png"
    )

    plt.close()

    # Prophet forecast visualization.
    forecast_plot = model.plot(forecast)

    forecast_plot.savefig(
        OUTPUT_DIR / "prophet_forecast.png"
    )

    plt.close(forecast_plot)

    # Forecast trend and seasonality components.
    components_plot = model.plot_components(forecast)

    components_plot.savefig(
        OUTPUT_DIR / "forecast_components.png"
    )

    plt.close(components_plot)


def main():
    """Execute the complete Prophet forecasting pipeline."""

    print("Loading Reliance stock data...")

    data = load_and_prepare_data()

    if len(data) < 10:
        raise ValueError("Insufficient historical data for forecasting.")

    print(f"Total records: {len(data)}")

    print(
        f"Date range: {data['ds'].min().date()} "
        f"to {data['ds'].max().date()}"
    )

    print("\nEvaluating Prophet model...")

    metrics = evaluate_model(data)

    print(metrics.to_string(index=False))

    print("\nGenerating 30-business-day forecast...")

    model, forecast = forecast_future(data)

    save_outputs(
        data,
        metrics,
        model,
        forecast
    )

    print("\nForecast preview:")

    print(
        forecast[
            ["ds", "yhat", "yhat_lower", "yhat_upper"]
        ].head()
    )

    print(f"\nAll outputs saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
