
import json
from pathlib import Path

import mlflow
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
TRACKING_DB = OUTPUT_DIR / "mlflow.db"

REQUIRED_COLUMNS = ["Date", "Region", "Category", "Sales", "Units Sold"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset(path=DATA_PATH):
    """Load and validate the sales dataset."""
    if not Path(path).exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    return df


def calculate_metrics(df):
    """Calculate data-quality and sales metrics."""
    sales = pd.to_numeric(df["Sales"], errors="coerce")
    units = pd.to_numeric(df["Units Sold"], errors="coerce")

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_sales": float(sales.sum()),
        "average_sales": float(sales.mean()),
        "maximum_sales": float(sales.max()),
        "minimum_sales": float(sales.min()),
        "total_units_sold": float(units.sum()),
    }


def run_experiment(df, experiment_name, strategy):
    """Track one analytics experiment using MLflow."""
    metrics = calculate_metrics(df)

    with mlflow.start_run(run_name=experiment_name):
        mlflow.log_param("strategy", strategy)
        mlflow.log_param("dataset", DATA_PATH.name)
        mlflow.log_param("rows", metrics["rows"])
        mlflow.log_param("columns", metrics["columns"])

        mlflow.log_metrics({
            key: value
            for key, value in metrics.items()
        })

        # Save the dataset used in this experiment
        dataset_path = OUTPUT_DIR / f"{strategy}_dataset.csv"
        df.to_csv(dataset_path, index=False)
        mlflow.log_artifact(
            str(dataset_path),
            artifact_path="datasets"
        )

        # Save descriptive statistics
        report_path = OUTPUT_DIR / f"{strategy}_summary.csv"
        df.describe(include="all").transpose().to_csv(report_path)
        mlflow.log_artifact(
            str(report_path),
            artifact_path="reports"
        )

        # Save experiment metrics as JSON
        metrics_path = OUTPUT_DIR / f"{strategy}_metrics.json"
        with open(metrics_path, "w", encoding="utf-8") as file:
            json.dump(metrics, file, indent=4)

        mlflow.log_artifact(
            str(metrics_path),
            artifact_path="metrics"
        )

        run_id = mlflow.active_run().info.run_id

    print(f"\nCompleted: {experiment_name}")
    print(f"Run ID: {run_id}")
    print(f"Metrics: {metrics}")

    return {
        "experiment": experiment_name,
        "run_id": run_id,
        **metrics,
    }


def main():
    """Execute and compare the analytics experiments."""
    mlflow.set_tracking_uri(
        f"sqlite:///{TRACKING_DB.resolve().as_posix()}"
    )
    mlflow.set_experiment("W9D5-Tracked-DA-Pipeline")

    original_df = load_dataset()

    original_result = run_experiment(
        original_df,
        "Original Dataset",
        "original"
    )

    cleaned_df = original_df.drop_duplicates()

    cleaned_result = run_experiment(
        cleaned_df,
        "After Duplicate Removal",
        "cleaned"
    )

    comparison = pd.DataFrame([
        original_result,
        cleaned_result,
    ])

    comparison_path = OUTPUT_DIR / "experiment_comparison.csv"
    comparison.to_csv(comparison_path, index=False)

    # Log the final comparison report
    with mlflow.start_run(run_name="Pipeline Comparison"):
        mlflow.log_param("experiments_compared", 2)
        mlflow.log_artifact(
            str(comparison_path),
            artifact_path="comparison"
        )

    print("\nAll experiments completed successfully!")
    print(f"Comparison report: {comparison_path}")
    print(f"MLflow database: {TRACKING_DB}")


if __name__ == "__main__":
    main()
