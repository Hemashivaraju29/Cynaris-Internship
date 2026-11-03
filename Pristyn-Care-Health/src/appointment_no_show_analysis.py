import pandas as pd
from pathlib import Path

data_path = Path("Pristyn-Care-Health/data/da_healthcare_appointments.csv")
output_dir = Path("Pristyn-Care-Health/outputs")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

# Overall no-show analysis
total = len(df)
no_shows = df["no_show"].sum()
attended = total - no_shows
no_show_rate = (no_shows / total) * 100

print("\n===== OVERALL APPOINTMENT ANALYSIS =====")
print("Total appointments:", total)
print("Attended appointments:", attended)
print("No-show appointments:", no_shows)
print(f"No-show rate: {no_show_rate:.2f}%")

# Group-wise analysis
group_columns = [
    "department",
    "specialty",
    "patient_age_group",
    "insurance_type",
    "booking_hour"
]

for column in group_columns:
    result = (
        df.groupby(column)
        .agg(
            total_appointments=("no_show", "count"),
            no_shows=("no_show", "sum")
        )
        .reset_index()
    )

    result["no_show_rate_pct"] = (
        result["no_shows"] / result["total_appointments"] * 100
    ).round(2)

    result = result.sort_values("no_show_rate_pct", ascending=False)

    output_file = output_dir / f"no_show_by_{column}.csv"
    result.to_csv(output_file, index=False)

    print(f"\n===== NO-SHOW BY {column.upper()} =====")
    print(result.to_string(index=False))

# Save overall summary
summary = pd.DataFrame([{
    "total_appointments": total,
    "attended_appointments": attended,
    "no_show_appointments": int(no_shows),
    "no_show_rate_pct": round(no_show_rate, 2)
}])

summary.to_csv(output_dir / "appointment_no_show_summary.csv", index=False)

print("\nAnalysis completed. Results saved in outputs folder.")
