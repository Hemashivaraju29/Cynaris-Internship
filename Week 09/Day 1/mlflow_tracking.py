
import os
from pathlib import Path

import mlflow
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configure MLflow experiment
mlflow.set_tracking_uri(
    "sqlite:///" + str((OUTPUT_DIR / "mlflow.db").resolve()).replace("\\", "/")
)
mlflow.set_experiment("W9D1-Data-Analysis-Experiments")


def run_experiment(experiment_name, df, strategy):
    """Log data analysis parameters, metrics, and an output artifact."""
    with mlflow.start_run(run_name=experiment_name):
        mlflow.log_param("strategy", strategy)
        mlflow.log_param("rows", len(df))
        mlflow.log_param("columns", len(df.columns))

        missing_cells = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        mlflow.log_metric("missing_cells", missing_cells)
        mlflow.log_metric("duplicate_rows", duplicate_rows)

        numeric_cols = df.select_dtypes(include="number").columns
        mlflow.log_param("numeric_columns", len(numeric_cols))

        if "Sales" in df.columns:
            sales = pd.to_numeric(df["Sales"], errors="coerce")
            mlflow.log_metric("total_sales", float(sales.sum()))
            mlflow.log_metric("average_sales", float(sales.mean()))
            mlflow.log_metric("max_sales", float(sales.max()))

        report_path = OUTPUT_DIR / f"{experiment_name.replace(' ', '_')}.csv"
        df.describe(include="all").transpose().to_csv(report_path)
        mlflow.log_artifact(str(report_path), artifact_path="reports")

        print(f"Completed: {experiment_name}")
        print(f"  Rows: {len(df)}")
        print(f"  Missing cells: {missing_cells}")
        print(f"  Duplicate rows: {duplicate_rows}")


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Experiment 1: Analyze the original dataset
    run_experiment("Original Dataset", df, "original")

    # Experiment 2: Analyze after removing duplicate rows
    cleaned_df = df.drop_duplicates()
    run_experiment("After Duplicate Removal", cleaned_df, "drop_duplicates")

    print("\nExperiments logged successfully.")
    print(f"MLflow tracking files: {OUTPUT_DIR / 'mlruns'}")


if __name__ == "__main__":
    main()
