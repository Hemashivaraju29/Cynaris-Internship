# Exploratory Data Analysis - Week 2 Day 3

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned sales dataset
df = pd.read_csv("Week 01/Day 5/sales_cleaned.csv")

print("========== DATASET ==========")
print(df)

# --------------------------------------------------
# 1. DATA PROFILING
# --------------------------------------------------

print("\n========== DATASET SHAPE ==========")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== NULL VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATE ROWS ==========")
print("Number of duplicate rows:", df.duplicated().sum())

# --------------------------------------------------
# 2. NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = df.select_dtypes(include="number").columns

print("\n========== NUMERIC COLUMNS ==========")
print(list(numeric_columns))

# --------------------------------------------------
# 3. SUMMARY STATISTICS
# --------------------------------------------------

summary_statistics = df[numeric_columns].describe()

print("\n========== SUMMARY STATISTICS ==========")
print(summary_statistics)

# Save summary statistics
summary_statistics.to_csv("summary_statistics.csv")

print("\nSummary statistics saved to summary_statistics.csv")

# --------------------------------------------------
# 4. DISTRIBUTIONS FOR NUMERIC COLUMNS
# --------------------------------------------------

for column in numeric_columns:
    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=column,
        bins=5,
        kde=True
    )

    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    filename = f"{column}_distribution.png"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()

# --------------------------------------------------
# 5. CORRELATION HEATMAP
# --------------------------------------------------

correlation_matrix = df[numeric_columns].corr()

print("\n========== CORRELATION MATRIX ==========")
print(correlation_matrix)

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    "correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# --------------------------------------------------
# 6. BUSINESS INSIGHTS
# --------------------------------------------------

print("\n========== BUSINESS INSIGHTS ==========")

# Insight 1 - Average sales value
average_sales = df["amount"].mean()

print(
    f"1. The average sales amount is ₹{average_sales:,.2f}, "
    "indicating a relatively high average transaction value."
)

# Insight 2 - Sales range
min_sales = df["amount"].min()
max_sales = df["amount"].max()

print(
    f"2. Sales amounts range from ₹{min_sales:,.2f} to "
    f"₹{max_sales:,.2f}, showing a ₹{max_sales - min_sales:,.2f} "
    "difference between the lowest and highest transaction."
)

# Insight 3 - Product category concentration
category_counts = df["category"].value_counts()

print(
    f"3. {category_counts.index[0]} represents "
    f"{category_counts.iloc[0]} out of {len(df)} sales records, "
    "showing that the current dataset is concentrated in one category."
)

# Insight 4 - Payment method
payment_counts = df["payment_method"].value_counts()

print(
    f"4. {payment_counts.index[0]} was used for "
    f"{payment_counts.iloc[0]} out of {len(df)} transactions, "
    "indicating complete dependence on this payment method in the sample."
)

# Insight 5 - Quantity
quantity_unique = df["quantity"].nunique()

print(
    f"5. The quantity column contains only {quantity_unique} unique value, "
    "so every recorded transaction has the same quantity."
)

# --------------------------------------------------
# 7. SUPPORTING BUSINESS CHARTS
# --------------------------------------------------

# Chart 1 - Sales amount by city
city_sales = df.groupby("city", as_index=False)["amount"].sum()

plt.figure(figsize=(8, 5))

ax = sns.barplot(
    data=city_sales,
    x="city",
    y="amount"
)

plt.title("Total Sales by City")
plt.xlabel("City")
plt.ylabel("Total Sales")

for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"₹{value:,.0f}" for value in container.datavalues]
    )

plt.tight_layout()

plt.savefig(
    "sales_by_city.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Chart 2 - Sales by Payment Method
payment_sales = df.groupby(
    "payment_method",
    as_index=False
)["amount"].sum()

plt.figure(figsize=(8, 5))

ax = sns.barplot(
    data=payment_sales,
    x="payment_method",
    y="amount"
)

plt.title("Total Sales by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Sales")

for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"₹{value:,.0f}" for value in container.datavalues]
    )

plt.tight_layout()

plt.savefig(
    "sales_by_payment_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n========== EDA COMPLETED ==========")