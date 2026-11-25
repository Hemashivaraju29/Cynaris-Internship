import os
import pandas as pd
import sweetviz as sv

DATASET = r"Week 05\Day 1\india_districts_census_2011.csv"
OUTPUT = r"Week 05\Day 2\sweetviz_report.html"

# Load dataset
df = pd.read_csv(DATASET)

print("Dataset loaded successfully")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Generate SweetViz report
report = sv.analyze(df)

# Save report
report.show_html(OUTPUT, open_browser=False)

print("\nSweetViz analysis completed.")
print("Report saved at:", OUTPUT)