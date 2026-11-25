
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "output"


def load_and_prepare_data(file_path, company="Reliance"):
    """Load and prepare stock data for anomaly detection."""
    df = pd.read_csv(file_path)

    required_columns = {"Date", "Close", "Company"}
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df[df["Company"].str.strip().str.lower() == company.lower()].copy()

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    df = df.dropna(subset=["Date", "Close"])
    df = df.sort_values("Date").reset_index(drop=True)

    if df.empty:
        raise ValueError(f"No valid records found for {company}")

    return df


def detect_statistical_anomalies(df, threshold=3.0):
    """Identify anomalies using the Z-score method."""
    result = df.copy()

    mean = result["Close"].mean()
    std = result["Close"].std(ddof=0)

    if std == 0:
        result["Z_Score"] = 0.0
    else:
        result["Z_Score"] = (result["Close"] - mean) / std

    result["Statistical_Anomaly"] = (
        result["Z_Score"].abs() > threshold
    )

    return result


def detect_isolation_forest(df, contamination=0.02):
    """Identify anomalies using Isolation Forest."""
    result = df.copy()

    model = IsolationForest(
        contamination=contamination,
        random_state=42
    )

    result["Isolation_Forest"] = model.fit_predict(
        result[["Close"]]
    )

    result["IF_Anomaly"] = result["Isolation_Forest"] == -1

    return result


def run_anomaly_detection(file_path):
    """Run both anomaly detection methods and save results."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_and_prepare_data(file_path)

    result = detect_statistical_anomalies(df)
    result = detect_isolation_forest(result)

    result["Anomaly_Agreement"] = (
        result["Statistical_Anomaly"] & result["IF_Anomaly"]
    )

    result.to_csv(
        OUTPUT_DIR / "anomaly_detection_results.csv",
        index=False
    )

    summary = pd.DataFrame({
        "Method": ["Z-Score", "Isolation Forest", "Both Methods"],
        "Anomaly_Count": [
            int(result["Statistical_Anomaly"].sum()),
            int(result["IF_Anomaly"].sum()),
            int(result["Anomaly_Agreement"].sum())
        ]
    })

    summary.to_csv(
        OUTPUT_DIR / "anomaly_summary.csv",
        index=False
    )

    # Plot stock prices and detected anomalies
    plt.figure(figsize=(14, 7))
    plt.plot(
        result["Date"],
        result["Close"],
        label="Closing Price",
        alpha=0.7
    )

    statistical = result[result["Statistical_Anomaly"]]
    isolation = result[result["IF_Anomaly"]]

    plt.scatter(
        statistical["Date"],
        statistical["Close"],
        label="Z-Score Anomalies",
        marker="o"
    )

    plt.scatter(
        isolation["Date"],
        isolation["Close"],
        label="Isolation Forest Anomalies",
        marker="x"
    )

    plt.title("Reliance Stock Price Anomaly Detection")
    plt.xlabel("Date")
    plt.ylabel("Closing Price")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / "anomaly_detection_plot.png", dpi=150)
    plt.close()

    print("\nAnomaly Detection Summary")
    print(summary.to_string(index=False))
    print("\nTotal records:", len(result))
    print("Results saved to:", OUTPUT_DIR)

    return result, summary


if __name__ == "__main__":
    dataset_path = (
        PROJECT_DIR.parent.parent
        / "Week 07"
        / "Day 1"
        / "nifty500_combined_eda.csv"
    )

    run_anomaly_detection(dataset_path)

