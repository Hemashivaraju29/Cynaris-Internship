
import os
import mlflow
import pandas as pd
from mlflow import MlflowClient
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DATA_PATH = os.path.join(
    BASE_DIR, "..", "..", "Week 07", "Day 3", "Sales_Data.csv"
)
DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "Day 2", "output", "mlflow.db")
)

mlflow.set_tracking_uri(
    "sqlite:///" + DB_PATH.replace("\\", "/")
)

client = MlflowClient()
experiment = mlflow.set_experiment("W9D4-Model-Version-Comparison")

data = pd.read_csv(DATA_PATH)
X = data[["Units Sold"]]
y = data["Sales"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train Version 2 using the same algorithm and dataset.
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

metrics = {
    "mae": mean_absolute_error(y_test, predictions),
    "mse": mean_squared_error(y_test, predictions),
    "rmse": mean_squared_error(y_test, predictions) ** 0.5,
    "r2": r2_score(y_test, predictions),
}

with mlflow.start_run(
    experiment_id=experiment.experiment_id,
    run_name="Model_Version_2"
) as run:
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("feature", "Units Sold")
    mlflow.log_param("target", "Sales")
    mlflow.log_param("version", 2)
    mlflow.log_metrics(metrics)

    model_info = mlflow.sklearn.log_model(
        model,
        name="sales_prediction_model"
    )

    registered = mlflow.register_model(
        model_info.model_uri,
        "W9D2-Sales-Prediction-Model"
    )

    print("Registered Version:", registered.version)
    print("Run ID:", run.info.run_id)
    print("Version 2 metrics:", metrics)

# Compare registered model versions.
versions = client.search_model_versions(
    "name='W9D2-Sales-Prediction-Model'"
)

rows = []

for version in versions:
    run = client.get_run(version.run_id)
    rows.append({
        "version": version.version,
        "run_id": version.run_id,
        "mae": run.data.metrics.get("mae", run.data.metrics.get("MAE")),
        "rmse": run.data.metrics.get("rmse", run.data.metrics.get("RMSE")),
        "r2": run.data.metrics.get("r2", run.data.metrics.get("R2")),
        "status": version.status,
    })

comparison = pd.DataFrame(rows).sort_values("version")
comparison.to_csv(
    os.path.join(OUTPUT_DIR, "model_version_comparison.csv"),
    index=False
)

print("\nModel Version Comparison:")
print(comparison.to_string(index=False))

best = comparison.loc[comparison["mae"].idxmin()]
print(f"\nBest version based on MAE: {best['version']}")
