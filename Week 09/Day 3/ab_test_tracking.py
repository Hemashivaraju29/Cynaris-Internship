
import os
import pandas as pd
import mlflow
from scipy.stats import chi2_contingency

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Sample A/B testing data
data = pd.DataFrame({
    "group": ["A"] * 10 + ["B"] * 10,
    "visitors": [100, 120, 110, 105, 115, 130, 125, 100, 110, 120,
                 100, 120, 110, 105, 115, 130, 125, 100, 110, 120],
    "conversions": [10, 12, 11, 10, 12, 13, 12, 10, 11, 12,
                    15, 18, 16, 15, 17, 20, 19, 15, 16, 18]
})

# Calculate conversion rates
summary = data.groupby("group")[["visitors", "conversions"]].sum()
summary["conversion_rate"] = (
    summary["conversions"] / summary["visitors"]
)

rate_a = summary.loc["A", "conversion_rate"]
rate_b = summary.loc["B", "conversion_rate"]

# Chi-square significance test
contingency_table = [
    [summary.loc["A", "conversions"],
     summary.loc["A", "visitors"] - summary.loc["A", "conversions"]],
    [summary.loc["B", "conversions"],
     summary.loc["B", "visitors"] - summary.loc["B", "conversions"]]
]

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

# MLflow tracking
tracking_db = os.path.join(OUTPUT_DIR, "mlflow.db")
mlflow.set_tracking_uri(f"sqlite:///{tracking_db.replace(os.sep, '/')}")
mlflow.set_experiment("W9D3-AB-Test-Tracking")

with mlflow.start_run(run_name="AB_Test_Conversion_Comparison"):
    mlflow.log_param("control_group", "A")
    mlflow.log_param("treatment_group", "B")
    mlflow.log_param("statistical_test", "Chi-square")

    mlflow.log_metric("group_A_conversion_rate", rate_a)
    mlflow.log_metric("group_B_conversion_rate", rate_b)
    mlflow.log_metric("chi_square_statistic", chi2)
    mlflow.log_metric("p_value", p_value)

    mlflow.log_metric("visitors_A", int(summary.loc["A", "visitors"]))
    mlflow.log_metric("visitors_B", int(summary.loc["B", "visitors"]))

    results = summary.reset_index()
    results.to_csv(os.path.join(OUTPUT_DIR, "ab_test_results.csv"), index=False)

    mlflow.log_artifact(os.path.join(OUTPUT_DIR, "ab_test_results.csv"))

    print("A/B Test Results")
    print(results.to_string(index=False))
    print(f"\nChi-square statistic: {chi2:.4f}")
    print(f"P-value: {p_value:.4f}")

    if p_value < 0.05:
        print("Result: Statistically significant difference.")
    else:
        print("Result: No statistically significant difference.")
