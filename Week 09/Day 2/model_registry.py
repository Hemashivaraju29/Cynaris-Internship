
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parents[1]
DATA_PATH = PROJECT_DIR / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Keep the W9D2 tracking database separate from W9D1.
mlflow.set_tracking_uri(
    "sqlite:///" + str((OUTPUT_DIR / "mlflow.db").resolve()).replace("\\", "/")
)
mlflow.set_experiment("W9D2-Analyst-Model-Registry")

MODEL_NAME = "W9D2-Sales-Prediction-Model"


def main():
    df = pd.read_csv(DATA_PATH)

    required_columns = {"Sales", "Units Sold"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Dataset must contain: {required_columns}")

    df = df[["Units Sold", "Sales"]].dropna()

    if len(df) < 5:
        raise ValueError("At least five valid rows are required.")

    X = df[["Units Sold"]]
    y = df["Sales"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = LinearRegression()

    with mlflow.start_run(run_name="Sales Regression Model") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse**0.5
        r2 = r2_score(y_test, predictions)

        mlflow.log_param("model_type", "LinearRegression")
        mlflow.log_param("feature", "Units Sold")
        mlflow.log_param("target", "Sales")
        mlflow.log_param("test_size", 0.25)
        mlflow.log_param("random_state", 42)
        mlflow.log_metric("mae", float(mae))
        mlflow.log_metric("mse", float(mse))
        mlflow.log_metric("rmse", float(rmse))
        mlflow.log_metric("r2_score", float(r2))

        signature = infer_signature(X_train, model.predict(X_train))

        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            name="sales-regression-model",
            signature=signature,
            input_example=X_train.head(3),
        )

        # Register the logged model in the MLflow Model Registry.
        registered_model = mlflow.register_model(
            model_uri=model_info.model_uri,
            name=MODEL_NAME,
        )

        results = pd.DataFrame(
            {
                "metric": ["MAE", "MSE", "RMSE", "R2"],
                "value": [mae, mse, rmse, r2],
            }
        )
        results.to_csv(OUTPUT_DIR / "evaluation_metrics.csv", index=False)
        mlflow.log_artifact(str(OUTPUT_DIR / "evaluation_metrics.csv"))

        print("Model training and registration completed.")
        print("Experiment:", "W9D2-Analyst-Model-Registry")
        print("Run ID:", run.info.run_id)
        print("Registered model:", registered_model.name)
        print("Model version:", registered_model.version)
        print(results.to_string(index=False))


if __name__ == "__main__":
    main()
