import pandas as pd
from pathlib import Path
from scipy.stats import chi2_contingency

data_path = Path("Pristyn-Care-Health/data/da_healthcare_appointments.csv")
output_dir = Path("Pristyn-Care-Health/outputs")

df = pd.read_csv(data_path)

columns = [
    "department",
    "specialty",
    "patient_age_group",
    "insurance_type",
    "booking_hour"
]

results = []

for column in columns:
    table = pd.crosstab(df[column], df["no_show"])
    chi2, p_value, dof, expected = chi2_contingency(table)

    significant = "Yes" if p_value < 0.05 else "No"

    results.append({
        "factor": column,
        "chi_square": round(chi2, 4),
        "degrees_of_freedom": dof,
        "p_value": round(p_value, 6),
        "significant_at_0.05": significant
    })

    print("\nFactor:", column)
    print("Chi-square:", round(chi2, 4))
    print("P-value:", round(p_value, 6))
    print("Statistically significant:", significant)

result_df = pd.DataFrame(results)
result_df.to_csv(
    output_dir / "no_show_significance_tests.csv",
    index=False
)

print("\nStatistical test results saved successfully.")
