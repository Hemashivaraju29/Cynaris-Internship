import pandas as pd
import sweetviz as sv
from pathlib import Path

data_path = Path("Week 07/Day 1/nifty500_combined_eda.csv")
output_path = Path("Week 07/Day 2/sweetviz_report.html")

df = pd.read_csv(data_path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("Dataset shape:", df.shape)
print("Starting SweetViz report generation...")

report = sv.analyze(df, pairwise_analysis="off")
report.show_html(
    filepath=str(output_path),
    open_browser=False
)

print("SweetViz report generated successfully!")
print("Report location:", output_path.resolve())
print("Report size:", output_path.stat().st_size, "bytes")
