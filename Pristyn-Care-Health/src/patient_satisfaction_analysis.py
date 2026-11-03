import pandas as pd
from pathlib import Path

data_path = Path("Pristyn-Care-Health/data/sunrise_patient_satisfaction.csv")
output_dir = Path("Pristyn-Care-Health/outputs")
output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

rating_columns = [
    "doctor_rating",
    "nurse_rating",
    "cleanliness_rating",
    "billing_clarity_rating",
    "overall_satisfaction"
]

print("\n===== OVERALL PATIENT SATISFACTION =====")
print("Total surveys:", len(df))

summary = df[rating_columns].mean().round(2)
print("\nAverage Ratings:")
print(summary.to_string())

summary.to_csv(output_dir / "satisfaction_rating_summary.csv")

# Satisfaction by hospital
hospital_summary = (
    df.groupby("hospital")[rating_columns]
    .mean()
    .round(2)
)

print("\n===== SATISFACTION BY HOSPITAL =====")
print(hospital_summary.to_string())

hospital_summary.to_csv(
    output_dir / "satisfaction_by_hospital.csv"
)

# Satisfaction by department
department_summary = (
    df.groupby("department")[rating_columns]
    .mean()
    .round(2)
)

print("\n===== SATISFACTION BY DEPARTMENT =====")
print(department_summary.to_string())

department_summary.to_csv(
    output_dir / "satisfaction_by_department.csv"
)

# Waiting time and satisfaction relationship
correlation = df[
    ["waiting_time_mins", "overall_satisfaction"]
].corr().iloc[0, 1]

print("\n===== WAITING TIME ANALYSIS =====")
print("Average waiting time:", round(df["waiting_time_mins"].mean(), 2), "minutes")
print("Correlation with satisfaction:", round(correlation, 3))

# Recommendation responses
recommendation = df["would_recommend"].value_counts(dropna=False)

print("\n===== WOULD RECOMMEND =====")
print(recommendation.to_string())

recommendation.to_csv(
    output_dir / "recommendation_responses.csv"
)

print("\nPatient satisfaction analysis completed successfully.")
