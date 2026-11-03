import pandas as pd
from pathlib import Path

data_path = Path("Pristyn-Care-Health/data/sunrise_resource_utilisation.csv")
output_dir = Path("Pristyn-Care-Health/outputs")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

df["bed_invalid"] = df["occupied_beds"] > df["total_beds"]
df["icu_invalid"] = df["icu_beds_occupied"] > df["icu_beds_total"]
df["surgery_invalid"] = df["surgeries_completed"] > df["surgeries_scheduled"]
df["zero_scheduled"] = df["surgeries_scheduled"] == 0

# A record is invalid if any of the above checks fail.
df["any_validation_issue"] = df[
    ["bed_invalid", "icu_invalid", "surgery_invalid", "zero_scheduled"]
].any(axis=1)

summary = pd.DataFrame({
    "validation_check": [
        "Occupied beds exceed total beds",
        "ICU occupied beds exceed ICU total",
        "Completed surgeries exceed scheduled",
        "Zero scheduled surgeries",
        "Records with at least one validation issue"
    ],
    "affected_records": [
        int(df["bed_invalid"].sum()),
        int(df["icu_invalid"].sum()),
        int(df["surgery_invalid"].sum()),
        int(df["zero_scheduled"].sum()),
        int(df["any_validation_issue"].sum())
    ]
})

summary["percentage_of_records"] = (
    summary["affected_records"] / len(df) * 100
).round(2)

summary.to_csv(
    output_dir / "resource_data_quality_report.csv",
    index=False
)

df.to_csv(
    output_dir / "resource_validation_flags.csv",
    index=False
)

print("\n===== RESOURCE DATA QUALITY REPORT =====")
print(summary.to_string(index=False))

print("\nTotal records:", len(df))
print("Records with at least one issue:", int(df["any_validation_issue"].sum()))
print("Records without flagged issues:", int((~df["any_validation_issue"]).sum()))

print("\nReports saved successfully.")
