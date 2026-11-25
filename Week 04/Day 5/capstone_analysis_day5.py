# Week 04 - Day 5: Capstone Analysis
# Online Retail Business Dataset

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# --------------------------------------------------
# 1. File paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "OnlineRetail.csv"

CLEANED_FILE = BASE_DIR / "cleaned_online_retail.csv"
SUMMARY_FILE = BASE_DIR / "statistical_analysis.csv"

# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE, encoding="latin1")

print("Original dataset shape:", df.shape)

# --------------------------------------------------
# 3. Data cleaning
# --------------------------------------------------

# Remove duplicate rows
df = df.drop_duplicates()

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Remove cancelled invoices
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove invalid quantities and prices
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# Fill missing descriptions
df["Description"] = df["Description"].fillna("Unknown Product")

# CustomerID is not required for product/country/month analysis.
# Keep only records with CustomerID for customer-level analysis later.
df["CustomerID"] = df["CustomerID"].astype("Int64")

# --------------------------------------------------
# 4. Feature engineering
# --------------------------------------------------

df["Revenue"] = df["Quantity"] * df["UnitPrice"]

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

df["Year"] = df["InvoiceDate"].dt.year

df["InvoiceDateOnly"] = df["InvoiceDate"].dt.date

# --------------------------------------------------
# 5. Save cleaned dataset
# --------------------------------------------------

df.to_csv(CLEANED_FILE, index=False)

print("Cleaned dataset shape:", df.shape)
print("Cleaned dataset saved to:", CLEANED_FILE)

# --------------------------------------------------
# 6. Basic EDA
# --------------------------------------------------

print("\n--- Basic EDA ---")

print("Total revenue:", round(df["Revenue"].sum(), 2))
print("Total invoices:", df["InvoiceNo"].nunique())
print("Total products:", df["StockCode"].nunique())
print("Total countries:", df["Country"].nunique())
print("Total customers:", df["CustomerID"].nunique())

# --------------------------------------------------
# 7. Top products by revenue
# --------------------------------------------------

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 products by revenue:")
print(top_products)

plt.figure(figsize=(10, 6))
top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(BASE_DIR / "top_products_revenue.png", dpi=300)
plt.close()

# --------------------------------------------------
# 8. Revenue by country
# --------------------------------------------------

country_revenue = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 countries by revenue:")
print(country_revenue)

plt.figure(figsize=(10, 6))
country_revenue.sort_values().plot(kind="barh")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(BASE_DIR / "country_revenue.png", dpi=300)
plt.close()

# --------------------------------------------------
# 9. Monthly revenue trend
# --------------------------------------------------

monthly_revenue = df.groupby("Month")["Revenue"].sum()

print("\nMonthly revenue:")
print(monthly_revenue)

plt.figure(figsize=(12, 6))
monthly_revenue.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(BASE_DIR / "monthly_revenue_trend.png", dpi=300)
plt.close()

# --------------------------------------------------
# 10. Customer revenue
# --------------------------------------------------

customer_revenue = (
    df.dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 customers by revenue:")
print(customer_revenue)

# --------------------------------------------------
# 11. Statistical analysis
# --------------------------------------------------

# Compare revenue between the two largest countries
top_two_countries = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(2)
    .index
)

country_1 = df[df["Country"] == top_two_countries[0]]["Revenue"]
country_2 = df[df["Country"] == top_two_countries[1]]["Revenue"]

t_stat, p_value = stats.ttest_ind(
    country_1,
    country_2,
    equal_var=False
)

print("\n--- Statistical Analysis ---")
print("Country 1:", top_two_countries[0])
print("Country 2:", top_two_countries[1])
print("T-statistic:", round(t_stat, 4))
print("P-value:", round(p_value, 6))

if p_value < 0.05:
    conclusion = "Statistically significant difference in average revenue."
else:
    conclusion = "No statistically significant difference in average revenue."

print("Conclusion:", conclusion)

# --------------------------------------------------
# 12. Statistical summary file
# --------------------------------------------------

statistics = pd.DataFrame({
    "Metric": [
        "Original rows",
        "Cleaned rows",
        "Total revenue",
        "Unique invoices",
        "Unique products",
        "Unique countries",
        "Unique customers",
        "T-statistic",
        "P-value",
        "Test conclusion"
    ],
    "Value": [
        541909,
        len(df),
        round(df["Revenue"].sum(), 2),
        df["InvoiceNo"].nunique(),
        df["StockCode"].nunique(),
        df["Country"].nunique(),
        df["CustomerID"].nunique(),
        round(t_stat, 4),
        round(p_value, 6),
        conclusion
    ]
})

statistics.to_csv(SUMMARY_FILE, index=False)

print("\nStatistical summary saved to:", SUMMARY_FILE)

print("\nCAPSTONE ANALYSIS COMPLETED SUCCESSFULLY.")