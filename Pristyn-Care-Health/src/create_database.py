import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
DB_DIR = BASE_DIR / "outputs"

DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "pristyn_healthcare.db"

datasets = {
    "healthcare_appointments": "da_healthcare_appointments.csv",
    "patient_satisfaction": "sunrise_patient_satisfaction.csv",
    "resource_utilisation": "sunrise_resource_utilisation.csv"
}

with sqlite3.connect(DB_PATH) as connection:

    for table_name, filename in datasets.items():

        file_path = DATA_DIR / filename
        df = pd.read_csv(file_path)

        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(f"{table_name}: {len(df)} records imported")

print("\nDatabase created successfully!")
print(f"Location: {DB_PATH}")