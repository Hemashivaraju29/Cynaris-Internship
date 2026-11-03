import pandas as pd
from pathlib import Path

path = Path("Pristyn-Care-Health/data/sunrise_resource_utilisation.csv")
df = pd.read_csv(path)

checks = {
    "Occupied beds exceed total beds":
        df["occupied_beds"] > df["total_beds"],

    "ICU occupied beds exceed ICU total":
        df["icu_beds_occupied"] > df["icu_beds_total"],

    "Completed surgeries exceed scheduled":
        df["surgeries_completed"] > df["surgeries_scheduled"],

    "Zero scheduled surgeries":
        df["surgeries_scheduled"] == 0
}

print("\n===== RESOURCE DATA VALIDATION =====")

for name, condition in checks.items():
    print(f"\n{name}: {condition.sum()} records")

    if condition.any():
        print(
            df.loc[
                condition,
                [
                    "hospital",
                    "department",
                    "date",
                    "total_beds",
                    "occupied_beds",
                    "icu_beds_total",
                    "icu_beds_occupied",
                    "surgeries_scheduled",
                    "surgeries_completed"
                ]
            ].head(10).to_string(index=False)
        )

print("\n===== VALUE RANGES =====")

columns = [
    "total_beds",
    "occupied_beds",
    "icu_beds_total",
    "icu_beds_occupied",
    "surgeries_scheduled",
    "surgeries_completed"
]

print(df[columns].describe().round(2).to_string())

print("\nValidation inspection completed.")
