import pandas as pd
from pathlib import Path
from autoviz import AutoViz_Class

data_path = Path("Week 07/Day 1/nifty500_combined_eda.csv")
output_dir = Path("Week 07/Day 2/autoviz_plots")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data_path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("Dataset shape:", df.shape)
print("Starting AutoViz. This may take a few minutes...")

AV = AutoViz_Class()
result = AV.AutoViz(
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
    save_plot_dir=str(output_dir)
)

print("AutoViz finished.")
print("Check the output folder:", output_dir.resolve())
print("Returned object type:", type(result).__name__)
