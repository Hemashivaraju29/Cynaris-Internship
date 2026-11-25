import pandas as pd
from pathlib import Path

base = Path("Pristyn-Care-Health")
output = base / "outputs"

# Read analysis outputs
no_show = pd.read_csv(output / "appointment_no_show_summary.csv")
satisfaction = pd.read_csv(output / "satisfaction_rating_summary.csv")
resource_quality = pd.read_csv(output / "resource_data_quality_report.csv")

# Read statistical test results
significance = pd.read_csv(output / "no_show_significance_tests.csv")

print("\n========== PRISTYN CARE PROJECT SUMMARY ==========")

print("\n1. APPOINTMENT ANALYSIS")
print(no_show.to_string(index=False))

print("\n2. PATIENT SATISFACTION")
print(satisfaction.to_string())

print("\n3. STATISTICAL SIGNIFICANCE")
print(significance.to_string(index=False))

print("\n4. RESOURCE DATA QUALITY")
print(resource_quality.to_string(index=False))

# Create combined summary
summary = pd.DataFrame([
    {
        "area": "Appointments",
        "metric": "No-show rate (%)",
        "value": no_show.loc[0, "no_show_rate_pct"],
        "status": "Analysed"
    },
    {
        "area": "Patient Satisfaction",
        "metric": "Average overall satisfaction (/5)",
        "value": float(satisfaction.iloc[4, 1]),
        "status": "Analysed"
    },
    {
        "area": "Patient Satisfaction",
        "metric": "Average waiting time (minutes)",
        "value": 91.43,
        "status": "Analysed"
    },
    {
        "area": "Resource Utilisation",
        "metric": "Records with validation issues (%)",
        "value": resource_quality.loc[
            resource_quality["validation_check"]
            == "Records with at least one validation issue",
            "percentage_of_records"
        ].iloc[0],
        "status": "Data quality warning"
    }
])

summary.to_csv(output / "combined_project_summary.csv", index=False)

print("\nCombined project summary saved successfully.")
