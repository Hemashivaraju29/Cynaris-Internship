import pandas as pd
from pathlib import Path

data_path = Path("Pristyn-Care-Health/data/sunrise_resource_utilisation.csv")
output_dir = Path("Pristyn-Care-Health/outputs")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

# Calculate operational KPIs
df["bed_occupancy_pct"] = (
    df["occupied_beds"] / df["total_beds"] * 100
)

df["icu_occupancy_pct"] = (
    df["icu_beds_occupied"] / df["icu_beds_total"] * 100
)

df["surgery_completion_pct"] = (
    df["surgeries_completed"] /
    df["surgeries_scheduled"].replace(0, pd.NA) * 100
)

print("\n===== OVERALL RESOURCE UTILISATION =====")

metrics = {
    "Average bed occupancy (%)": df["bed_occupancy_pct"].mean(),
    "Average ICU occupancy (%)": df["icu_occupancy_pct"].mean(),
    "Average surgery completion (%)": df["surgery_completion_pct"].mean(),
    "Average doctor attendance (%)": df["doctor_attendance_pct"].mean(),
    "Average nurse attendance (%)": df["nurse_attendance_pct"].mean(),
    "Average patient waiting time (mins)": df["avg_patient_wait_mins"].mean(),
    "Total readmissions": df["readmission_count"].sum()
}

for name, value in metrics.items():
    print(f"{name}: {value:.2f}")

# Hospital-wise analysis
hospital_summary = df.groupby("hospital").agg(
    bed_occupancy_pct=("bed_occupancy_pct", "mean"),
    icu_occupancy_pct=("icu_occupancy_pct", "mean"),
    surgery_completion_pct=("surgery_completion_pct", "mean"),
    doctor_attendance_pct=("doctor_attendance_pct", "mean"),
    nurse_attendance_pct=("nurse_attendance_pct", "mean"),
    avg_wait_mins=("avg_patient_wait_mins", "mean"),
    total_readmissions=("readmission_count", "sum")
).round(2)

print("\n===== HOSPITAL-WISE ANALYSIS =====")
print(hospital_summary.to_string())

hospital_summary.to_csv(
    output_dir / "resource_by_hospital.csv"
)

# Department-wise analysis
department_summary = df.groupby("department").agg(
    bed_occupancy_pct=("bed_occupancy_pct", "mean"),
    icu_occupancy_pct=("icu_occupancy_pct", "mean"),
    surgery_completion_pct=("surgery_completion_pct", "mean"),
    doctor_attendance_pct=("doctor_attendance_pct", "mean"),
    nurse_attendance_pct=("nurse_attendance_pct", "mean"),
    avg_wait_mins=("avg_patient_wait_mins", "mean"),
    total_readmissions=("readmission_count", "sum")
).round(2)

print("\n===== DEPARTMENT-WISE ANALYSIS =====")
print(department_summary.to_string())

department_summary.to_csv(
    output_dir / "resource_by_department.csv"
)

# Save detailed records with calculated KPIs
df.to_csv(
    output_dir / "resource_utilisation_kpis.csv",
    index=False
)

print("\nResource utilisation analysis completed successfully.")
