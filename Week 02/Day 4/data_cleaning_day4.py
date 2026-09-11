# Data Cleaning & Quality - Week 2 Day 4

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("Week 01/Day 5/sales_cleaned.csv")

print("========== ORIGINAL DATA ==========")
print(df)

# --------------------------------------------------
# 1. IDENTIFY MISSING VALUES
# --------------------------------------------------

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# --------------------------------------------------
# 2. IMPUTATION STRATEGIES
# --------------------------------------------------

# Mean imputation for numeric column
df["amount"] = df["amount"].fillna(df["amount"].mean())

# Median imputation for numeric column
df["quantity"] = df["quantity"].fillna(df["quantity"].median())

# Mode imputation for categorical column
df["category"] = df["category"].fillna(df["category"].mode()[0])

# Forward-fill for payment method
df["payment_method"] = df["payment_method"].ffill()

print("\n========== AFTER IMPUTATION ==========")
print(df.isnull().sum())

# --------------------------------------------------
# 3. OUTLIER DETECTION USING IQR
# --------------------------------------------------

Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

print("\n========== IQR OUTLIER DETECTION ==========")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)

outliers = df[
    (df["amount"] < lower_limit) |
    (df["amount"] > upper_limit)
]

print("\nOutliers detected:")
print(outliers)

# Cap outliers instead of removing them
df["amount"] = df["amount"].clip(
    lower=lower_limit,
    upper=upper_limit
)

print("\nOutliers capped successfully.")

# --------------------------------------------------
# 4. STANDARDISE STRING VALUES
# --------------------------------------------------

# Remove extra spaces and standardise casing
df["customer_name"] = df["customer_name"].str.strip().str.title()
df["product"] = df["product"].str.strip().str.title()
df["category"] = df["category"].str.strip().str.title()
df["city"] = df["city"].str.strip().str.title()
df["payment_method"] = df["payment_method"].str.strip().str.title()

# Standardise common payment-method variations
df["payment_method"] = df["payment_method"].replace({
    "Creditcard": "Credit Card",
    "Credit Card ": "Credit Card",
    "Upi": "UPI"
})

print("\n========== STANDARDISED STRING VALUES ==========")
print(df)

# --------------------------------------------------
# 5. DATA QUALITY LOG
# --------------------------------------------------

quality_log = pd.DataFrame({
    "issue": [
        "Missing values",
        "Amount missing values",
        "Quantity missing values",
        "Category missing values",
        "Payment method missing values",
        "Outliers in amount",
        "Inconsistent string values"
    ],
    "cleaning_action": [
        "Checked using isnull().sum()",
        "Imputed using mean",
        "Imputed using median",
        "Imputed using mode",
        "Applied forward-fill",
        "Detected using IQR and capped",
        "Removed whitespace and standardised casing/known variations"
    ],
    "reason": [
        "To quantify data completeness",
        "Mean preserves the overall average for numeric data",
        "Median is less affected by extreme values",
        "Mode is suitable for categorical data",
        "Forward-fill uses the previous available value",
        "Capping reduces the influence of extreme values",
        "Creates consistent categorical values for analysis"
    ]
})

quality_log.to_csv(
    "Week 02/Day 4/data_quality_log.csv",
    index=False
)

# --------------------------------------------------
# 6. EXPORT CLEANED DATA
# --------------------------------------------------

df.to_csv(
    "Week 02/Day 4/sales_cleaned_day4.csv",
    index=False
)

print("\n========== FINAL DATA ==========")
print(df)

print("\nCleaned dataset saved successfully.")
print("Data quality log saved successfully.")

print("\n========== DATA CLEANING COMPLETED ==========")