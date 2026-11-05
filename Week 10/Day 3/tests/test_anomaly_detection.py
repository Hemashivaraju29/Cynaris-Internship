
from pathlib import Path
import sys

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from anomaly_detection import (
    load_and_prepare_data,
    detect_statistical_anomalies,
    detect_isolation_forest,
)

DATASET_PATH = (
    PROJECT_DIR.parent.parent
    / "Week 07"
    / "Day 1"
    / "nifty500_combined_eda.csv"
)


def test_load_and_prepare_data():
    df = load_and_prepare_data(DATASET_PATH)

    assert not df.empty
    assert "Date" in df.columns
    assert "Close" in df.columns
    assert df["Date"].notna().all()
    assert df["Close"].notna().all()


def test_reliance_record_count():
    df = load_and_prepare_data(DATASET_PATH)

    assert len(df) == 2465
    assert (df["Company"] == "Reliance").all()


def test_statistical_anomaly_detection():
    df = pd.DataFrame({
        "Close": [100, 101, 99, 100, 500]
    })

    result = detect_statistical_anomalies(df, threshold=1.9)

    assert "Z_Score" in result.columns
    assert "Statistical_Anomaly" in result.columns
    assert result["Statistical_Anomaly"].iloc[-1]

def test_isolation_forest_detection():
    df = pd.DataFrame({
        "Close": [100] * 50 + [500]
    })

    result = detect_isolation_forest(df, contamination=0.02)

    assert "IF_Anomaly" in result.columns
    assert result["IF_Anomaly"].iloc[-1]


def test_constant_values():
    df = pd.DataFrame({
        "Close": [100, 100, 100, 100]
    })

    result = detect_statistical_anomalies(df)

    assert (result["Z_Score"] == 0).all()
    assert not result["Statistical_Anomaly"].any()
