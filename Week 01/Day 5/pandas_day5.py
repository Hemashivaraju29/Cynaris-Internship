# Pandas Data Analysis - Week 1 Day 5

import pandas as pd


# 1. Load CSV into a Pandas DataFrame

df = pd.read_csv("Week 01/Day 1/sales_filtered.csv")

print("Sales Data:")
print(df)


# 2. Inspect the DataFrame

print("\nFirst 5 rows:")
print(df.head())

print("\nDataFrame Information:")
df.info()

print("\nStatistical Summary:")
print(df.describe())

print("\nPayment Method Counts:")
print(df["payment_method"].value_counts(dropna=False))


# 3. Filter rows and select columns

print("\nSales above 50000:")
high_sales = df[df["amount"] > 50000]
print(high_sales)

print("\nSelected Columns:")
selected_columns = df[["customer_name", "product", "amount"]]
print(selected_columns)


# 4. Handle missing values

print("\nMissing Values Before Cleaning:")
print(df.isnull().sum())

df["payment_method"] = df["payment_method"].fillna("Unknown")

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())


# 5. Group by a column and aggregate

print("\nSales by Category:")
category_sales = df.groupby("category")["amount"].sum()
print(category_sales)


# 6. Export cleaned data to CSV

df.to_csv("sales_cleaned.csv", index=False)

print("\nCleaned data exported successfully to sales_cleaned.csv")