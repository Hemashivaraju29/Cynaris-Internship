"""
Checkpoint 2 - Repeatable data pipeline and baseline metrics
Run: python src/pipeline.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

sales = pd.read_csv(DATA / "da_sales_transactions.csv")
customers = pd.read_csv(DATA / "da_customer_data.csv")
products = pd.read_csv(DATA / "da_product_catalogue.csv")

# Standardize data types
sales["Date"] = pd.to_datetime(sales["Date"], errors="coerce")
sales["Units"] = pd.to_numeric(sales["Units"], errors="coerce")
sales["Unit_Price"] = pd.to_numeric(sales["Unit_Price"], errors="coerce")
sales["Discount_Pct"] = pd.to_numeric(sales["Discount_Pct"], errors="coerce")
sales["Return_Flag"] = pd.to_numeric(sales["Return_Flag"], errors="coerce").fillna(0).astype(int)

products["MRP"] = pd.to_numeric(products["MRP"], errors="coerce")
products["COGS"] = pd.to_numeric(products["COGS"], errors="coerce")

# Join reference data
df = (
    sales.merge(
        customers[["Customer_ID", "Age_Band", "Gender", "Acquisition_Channel", "Churned"]],
        on="Customer_ID", how="left", validate="many_to_one"
    )
    .merge(
        products[["Product_ID", "Name", "Category", "MRP", "COGS"]],
        on="Product_ID", how="left", validate="many_to_one",
        suffixes=("_sales", "_product")
    )
)

# Reproducible transaction-level metrics
df["Gross_Sales"] = df["Units"] * df["Unit_Price"]
df["Discount_Amount"] = df["Gross_Sales"] * df["Discount_Pct"] / 100
df["Net_Sales_Before_Returns"] = df["Gross_Sales"] - df["Discount_Amount"]
df["Realized_Sales"] = df["Net_Sales_Before_Returns"] * (1 - df["Return_Flag"])

# Data-quality checks
quality = pd.DataFrame([
    ["sales_rows", len(sales), "Expected 1000 rows in supplied dataset"],
    ["customer_rows", len(customers), "Expected 200 rows in supplied dataset"],
    ["product_rows", len(products), "Expected 50 rows in supplied dataset"],
    ["sales_missing_values", int(sales.isna().sum().sum()), "Should be 0"],
    ["customer_missing_values", int(customers.isna().sum().sum()), "Should be 0"],
    ["product_missing_values", int(products.isna().sum().sum()), "Should be 0"],
    ["sales_duplicate_rows", int(sales.duplicated().sum()), "Should be 0"],
    ["customer_duplicate_rows", int(customers.duplicated().sum()), "Should be 0"],
    ["product_duplicate_rows", int(products.duplicated().sum()), "Should be 0"],
    ["sales_to_customer_unmatched", int((~sales["Customer_ID"].isin(customers["Customer_ID"])).sum()), "Should be 0"],
    ["sales_to_product_unmatched", int((~sales["Product_ID"].isin(products["Product_ID"])).sum()), "Should be 0"],
], columns=["check", "value", "interpretation"])

quality.to_csv(OUT / "data_quality_report.csv", index=False)

# Baseline metrics available from the supplied datasets.
baseline = pd.DataFrame([
    ["Transaction count", len(df)],
    ["Unique customers in transactions", df["Customer_ID"].nunique()],
    ["Units sold", int(df["Units"].sum())],
    ["Gross sales", round(df["Gross_Sales"].sum(), 2)],
    ["Discount amount", round(df["Discount_Amount"].sum(), 2)],
    ["Net sales before returns", round(df["Net_Sales_Before_Returns"].sum(), 2)],
    ["Realized sales after returns", round(df["Realized_Sales"].sum(), 2)],
    ["Transaction return rate", round(df["Return_Flag"].mean() * 100, 2)],
    ["Average transaction value before returns", round(df["Net_Sales_Before_Returns"].mean(), 2)],
    ["Average realized transaction value", round(df["Realized_Sales"].mean(), 2)],
    ["Data start date", df["Date"].min().date()],
    ["Data end date", df["Date"].max().date()],
], columns=["metric", "value"])

baseline.to_csv(OUT / "baseline_metrics.csv", index=False)

# Channel-level baseline
channel = (
    df.groupby("Channel", as_index=False)
      .agg(
          transactions=("Transaction_ID", "count"),
          units=("Units", "sum"),
          realized_sales=("Realized_Sales", "sum"),
          return_rate=("Return_Flag", "mean")
      )
)
channel["return_rate"] = (channel["return_rate"] * 100).round(2)
channel["realized_sales"] = channel["realized_sales"].round(2)
channel.to_csv(OUT / "channel_baseline.csv", index=False)

print("Pipeline completed successfully.")
print(f"Rows after joins: {len(df)}")
print("Outputs written to outputs/")

if __name__ == "__main__":
    pass
