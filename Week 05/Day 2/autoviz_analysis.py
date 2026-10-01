import os
import pandas as pd
from autoviz.AutoViz_Class import AutoViz_Class

# Dataset path
DATASET = r"Week 05\Day 1\india_districts_census_2011.csv"

# Output directory
OUTPUT_DIR = r"Week 05\Day 2\AutoViz_Report"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATASET)

# Make duplicate column names unique
new_columns = []
column_counts = {}

for column in df.columns:
    if column in column_counts:
        column_counts[column] += 1
        new_columns.append(f"{column}_{column_counts[column]}")
    else:
        column_counts[column] = 0
        new_columns.append(column)

df.columns = new_columns

# Remove column causing AutoViz/HoloViews duplicate-column error
df = df.select_dtypes(include=["number"]).iloc[:, :20]


print("Dataset loaded successfully")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Run AutoViz
AV = AutoViz_Class()

AV.AutoViz(
    filename="",
    sep=",",
    depVar="",
    dfte=df,
    header=0,
    verbose=1,
    lowess=False,
    chart_format="html",
    max_rows_analyzed=150000,
    max_cols_analyzed=30,
    save_plot_dir=OUTPUT_DIR
)

print("\nAutoViz analysis completed.")
print("Reports saved in:", OUTPUT_DIR)