import pandas as pd

path = "Week 07/Day 1/nifty500_combined_eda.csv"
df = pd.read_csv(path)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\n--- DATASET OVERVIEW ---")
print("Rows and columns:", df.shape)
print("Date range:", df["Date"].min().date(), "to", df["Date"].max().date())
print("Companies:", df["Company"].nunique())
print("Missing values:", int(df.isna().sum().sum()))

print("\n--- RECORDS PER COMPANY ---")
print(df["Company"].value_counts().to_string())

print("\n--- CLOSING PRICE BY COMPANY ---")
print(df.groupby("Company")["Close"].agg(["mean", "min", "max"]).round(2).to_string())

print("\n--- OVERALL CLOSING PRICE ---")
print("Mean:", round(df["Close"].mean(), 2))
print("Minimum:", round(df["Close"].min(), 2))
print("Maximum:", round(df["Close"].max(), 2))

print("\n--- HIGHEST TOTAL DAILY VOLUME ---")
daily_volume = df.groupby("Date")["Volume"].sum()
print("Date:", daily_volume.idxmax().date())
print("Total volume:", int(daily_volume.max()))
