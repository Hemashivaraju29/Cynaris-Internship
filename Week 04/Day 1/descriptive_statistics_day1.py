import pandas as pd
import matplotlib.pyplot as plt

# Load the existing Cynaris sales dataset
df = pd.read_csv("Checkpoint-2/data/da_sales_transactions.csv")

# Calculate Revenue
df["Revenue"] = (
    df["Units"]
    * df["Unit_Price"]
    * (1 - df["Discount_Pct"] / 100)
)

# Use Revenue for descriptive statistics
revenue = df["Revenue"].dropna()

# --------------------------------------------------
# 1. Mean, Median, Mode, Variance, Standard Deviation
# --------------------------------------------------

mean_value = revenue.mean()
median_value = revenue.median()
mode_value = revenue.mode().iloc[0]
variance_value = revenue.var()
std_value = revenue.std()

print("DESCRIPTIVE STATISTICS")
print("----------------------")
print(f"Mean: {mean_value:.2f}")
print(f"Median: {median_value:.2f}")
print(f"Mode: {mode_value:.2f}")
print(f"Variance: {variance_value:.2f}")
print(f"Standard Deviation: {std_value:.2f}")

# --------------------------------------------------
# 2. Percentiles and Quartiles
# --------------------------------------------------

p10 = revenue.quantile(0.10)
q1 = revenue.quantile(0.25)
q2 = revenue.quantile(0.50)
q3 = revenue.quantile(0.75)
p90 = revenue.quantile(0.90)

iqr = q3 - q1

print("\nPERCENTILES AND QUARTILES")
print("-------------------------")
print(f"10th Percentile: {p10:.2f}")
print(f"Q1 (25th Percentile): {q1:.2f}")
print(f"Q2 (Median): {q2:.2f}")
print(f"Q3 (75th Percentile): {q3:.2f}")
print(f"90th Percentile: {p90:.2f}")
print(f"IQR: {iqr:.2f}")

# --------------------------------------------------
# 3. Distribution Shape
# --------------------------------------------------

skewness = revenue.skew()

print("\nDISTRIBUTION SHAPE")
print("------------------")
print(f"Skewness: {skewness:.2f}")

if abs(skewness) < 0.5:
    shape = "Approximately symmetric"
elif skewness >= 0.5:
    shape = "Right-skewed"
else:
    shape = "Left-skewed"

print(f"Shape: {shape}")

# --------------------------------------------------
# 4. Frequency Distribution
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.hist(
    revenue,
    bins=10,
    edgecolor="black"
)

plt.title("Frequency Distribution of Revenue")
plt.xlabel("Revenue")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(
    "Week 04/Day 1/frequency_distribution.png",
    dpi=300
)

plt.show()

# --------------------------------------------------
# 5. Side-by-Side Box Plot
# --------------------------------------------------

channels = df["Channel"].dropna().unique()

boxplot_data = [
    df.loc[df["Channel"] == channel, "Revenue"].dropna()
    for channel in channels
]

plt.figure(figsize=(10, 6))

plt.boxplot(
    boxplot_data,
    tick_labels=channels
)

plt.title("Revenue Distribution by Channel")
plt.xlabel("Channel")
plt.ylabel("Revenue")
plt.tight_layout()

plt.savefig(
    "Week 04/Day 1/boxplot_by_channel.png",
    dpi=300
)

plt.show()

# --------------------------------------------------
# 6. Save Statistics Summary
# --------------------------------------------------

summary = pd.DataFrame({
    "Statistic": [
        "Mean",
        "Median",
        "Mode",
        "Variance",
        "Standard Deviation",
        "10th Percentile",
        "Q1",
        "Q2 (Median)",
        "Q3",
        "90th Percentile",
        "IQR",
        "Skewness",
        "Distribution Shape"
    ],
    "Value": [
        mean_value,
        median_value,
        mode_value,
        variance_value,
        std_value,
        p10,
        q1,
        q2,
        q3,
        p90,
        iqr,
        skewness,
        shape
    ]
})

summary.to_csv(
    "Week 04/Day 1/statistics_summary.csv",
    index=False
)

print("\nStatistics summary saved successfully.")
print("\nWeek 4 Day 1 analysis completed.")