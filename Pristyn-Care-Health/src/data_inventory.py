import pandas as pd
from pathlib import Path

data_dir = Path("Pristyn-Care-Health/data")
output_dir = Path("Pristyn-Care-Health/outputs")
output_dir.mkdir(exist_ok=True)

inventory = []

for file in data_dir.glob("*.csv"):
    df = pd.read_csv(file)

    inventory.append({
        "Dataset": file.name,
        "Rows": len(df),
        "Columns": len(df.columns),
        "Missing_Values": int(df.isnull().sum().sum()),
        "Duplicate_Rows": int(df.duplicated().sum()),
        "Column_Names": ", ".join(df.columns)
    })

report = pd.DataFrame(inventory)
report.to_csv(output_dir / "data_inventory.csv", index=False)

print(report[["Dataset", "Rows", "Columns", "Missing_Values", "Duplicate_Rows"]])
print("\nData inventory saved successfully!")
