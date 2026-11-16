from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR.parents[1] / "Week 07" / "Day 3" / "Sales_Data.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load and validate data
df = pd.read_csv(DATA_FILE)
required_columns = {"Date", "Region", "Category", "Sales", "Units Sold"}

if not required_columns.issubset(df.columns):
    raise ValueError(f"Missing columns: {required_columns - set(df.columns)}")

df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"])
df["Units Sold"] = pd.to_numeric(df["Units Sold"])
df["Month"] = df["Date"].dt.strftime("%b")

# Overall metrics
total_sales = df["Sales"].sum()
total_units = df["Units Sold"].sum()
transactions = len(df)
average_transaction = df["Sales"].mean()

region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
category_units = df.groupby("Category")["Units Sold"].sum().sort_values(ascending=False)
monthly_sales = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()
category_performance = df.groupby("Category").agg(
    Revenue=("Sales", "sum"),
    Units=("Units Sold", "sum")
)
category_performance["Revenue Per Unit"] = (
    category_performance["Revenue"] / category_performance["Units"]
)

# Print business metrics
print("\n========== STAKEHOLDER BUSINESS ANALYSIS ==========")
print(f"Total Revenue: Rs. {total_sales:,.2f}")
print(f"Average Transaction: Rs. {average_transaction:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Number of Transactions: {transactions}")

print("\n1. Regional Sales:")
print(region_sales)

print("\n2. Category Sales:")
print(category_sales)

print("\n3. Monthly Sales:")
print(monthly_sales)

print("\n4. Category Units Sold:")
print(category_units)

print("\n5. Revenue Per Unit:")
print(category_performance.sort_values("Revenue Per Unit", ascending=False))

# Save analysis tables
region_sales.rename("Total Sales").to_csv(OUTPUT_DIR / "regional_sales.csv")
category_sales.rename("Total Sales").to_csv(OUTPUT_DIR / "category_sales.csv")
monthly_sales.rename("Total Sales").to_csv(OUTPUT_DIR / "monthly_sales.csv")
category_performance.to_csv(OUTPUT_DIR / "category_performance.csv")

# Chart 1: Regional sales
region_sales.plot(kind="bar", title="Sales by Region", ylabel="Sales (Rs.)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_by_region.png", dpi=200)
plt.close()

# Chart 2: Category sales
category_sales.plot(kind="bar", title="Sales by Category", ylabel="Sales (Rs.)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "sales_by_category.png", dpi=200)
plt.close()

# Chart 3: Monthly sales trend
monthly_sales.index = monthly_sales.index.astype(str)
monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend",
                   ylabel="Sales (Rs.)", xlabel="Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "monthly_sales_trend.png", dpi=200)
plt.close()

# Chart 4: Category units sold
category_units.plot(kind="bar", title="Units Sold by Category",
                    ylabel="Units Sold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "units_by_category.png", dpi=200)
plt.close()

print(f"\nAnalysis completed. Outputs saved in: {OUTPUT_DIR}")
