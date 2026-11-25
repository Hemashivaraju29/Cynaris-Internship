# Week 4 - Day 4: Hypothesis Testing

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

# Load dataset
file_path = "Checkpoint-2/data/da_sales_transactions.csv"
df = pd.read_csv(file_path)

# Create Revenue
df["Revenue"] = (
    df["Units"]
    * df["Unit_Price"]
    * (1 - df["Discount_Pct"] / 100)
)

print("=" * 60)
print("WEEK 4 - DAY 4: HYPOTHESIS TESTING")
print("=" * 60)

print(f"\nDataset loaded successfully.")
print(f"Number of transactions: {len(df)}")


# ============================================================
# TASK 1: BUSINESS HYPOTHESES
# ============================================================

print("\n" + "=" * 60)
print("TASK 1: BUSINESS HYPOTHESES")
print("=" * 60)

print("""
Scenario 1: Average transaction revenue
H0: The mean transaction revenue is equal to 8000.
H1: The mean transaction revenue is different from 8000.

Scenario 2: Website vs App revenue
H0: The mean revenue from Website transactions equals App transactions.
H1: The mean revenue from Website transactions differs from App transactions.

Scenario 3: Return rate
H0: The overall return rate is equal to 10%.
H1: The overall return rate is different from 10%.
""")


# ============================================================
# TASK 2: ONE-SAMPLE T-TEST
# ============================================================

print("=" * 60)
print("TASK 2: ONE-SAMPLE T-TEST")
print("=" * 60)

revenue = df["Revenue"].dropna()

# Test whether mean revenue differs from 8000
test_value = 8000

t_stat, p_value = stats.ttest_1samp(
    revenue,
    popmean=test_value
)

confidence_level = 0.95
confidence_interval = stats.t.interval(
    confidence_level,
    len(revenue) - 1,
    loc=revenue.mean(),
    scale=stats.sem(revenue)
)

print(f"Sample mean revenue: {revenue.mean():.2f}")
print(f"Hypothesized mean: {test_value:.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")

print(
    f"95% Confidence Interval: "
    f"({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})"
)

alpha = 0.05

if p_value < alpha:
    print("Decision: Reject H0.")
    print("Conclusion: The mean transaction revenue is significantly different from 8000.")
else:
    print("Decision: Fail to reject H0.")
    print("Conclusion: There is not enough evidence that the mean transaction revenue differs from 8000.")

# Save one-sample test result
one_sample_result = pd.DataFrame({
    "Test": ["One-sample t-test"],
    "Sample_Mean": [revenue.mean()],
    "Hypothesized_Mean": [test_value],
    "T_Statistic": [t_stat],
    "P_Value": [p_value],
    "CI_Lower": [confidence_interval[0]],
    "CI_Upper": [confidence_interval[1]]
})

one_sample_result.to_csv(
    "Week 04/Day 4/one_sample_ttest.csv",
    index=False
)

print("\nOne-sample test results saved successfully.")

# ============================================================
# TASK 3: TWO-SAMPLE T-TEST
# ============================================================

print("\n" + "=" * 60)
print("TASK 3: TWO-SAMPLE T-TEST")
print("=" * 60)

# Compare Revenue between Website and App channels
website_revenue = df.loc[
    df["Channel"] == "Website", "Revenue"
].dropna()

app_revenue = df.loc[
    df["Channel"] == "App", "Revenue"
].dropna()

print(f"Website transactions: {len(website_revenue)}")
print(f"App transactions: {len(app_revenue)}")

print(f"Website mean revenue: {website_revenue.mean():.2f}")
print(f"App mean revenue: {app_revenue.mean():.2f}")

# Welch's two-sample t-test
t_stat_two, p_value_two = stats.ttest_ind(
    website_revenue,
    app_revenue,
    equal_var=False
)

# 95% confidence interval for difference in means
mean_difference = website_revenue.mean() - app_revenue.mean()

se_difference = np.sqrt(
    (website_revenue.var(ddof=1) / len(website_revenue))
    + (app_revenue.var(ddof=1) / len(app_revenue))
)

df_welch = (
    (
        website_revenue.var(ddof=1) / len(website_revenue)
        + app_revenue.var(ddof=1) / len(app_revenue)
    ) ** 2
    /
    (
        (
            website_revenue.var(ddof=1) / len(website_revenue)
        ) ** 2 / (len(website_revenue) - 1)
        +
        (
            app_revenue.var(ddof=1) / len(app_revenue)
        ) ** 2 / (len(app_revenue) - 1)
    )
)

critical_value = stats.t.ppf(
    0.975,
    df_welch
)

ci_lower = mean_difference - critical_value * se_difference
ci_upper = mean_difference + critical_value * se_difference

print(f"\nt-statistic: {t_stat_two:.4f}")
print(f"p-value: {p_value_two:.6f}")
print(
    f"95% CI for mean difference: "
    f"({ci_lower:.2f}, {ci_upper:.2f})"
)

alpha = 0.05

if p_value_two < alpha:
    print("Decision: Reject H0.")
    print(
        "Conclusion: There is a statistically significant "
        "difference between Website and App mean revenue."
    )
else:
    print("Decision: Fail to reject H0.")
    print(
        "Conclusion: There is not enough evidence of a "
        "difference between Website and App mean revenue."
    )

# Save two-sample test result
two_sample_result = pd.DataFrame({
    "Test": ["Welch two-sample t-test"],
    "Website_Mean": [website_revenue.mean()],
    "App_Mean": [app_revenue.mean()],
    "Mean_Difference": [mean_difference],
    "T_Statistic": [t_stat_two],
    "P_Value": [p_value_two],
    "CI_Lower": [ci_lower],
    "CI_Upper": [ci_upper]
})

two_sample_result.to_csv(
    "Week 04/Day 4/two_sample_ttest.csv",
    index=False
)

print("\nTwo-sample test results saved successfully.")

# ============================================================
# TASK 4: TYPE I AND TYPE II ERRORS
# ============================================================

print("\n" + "=" * 60)
print("TASK 4: TYPE I AND TYPE II ERRORS")
print("=" * 60)

print("""
TYPE I ERROR:
A Type I error occurs when we reject a true null hypothesis.

Business consequence:
If we conclude that Website and App mean revenue are different
when they are actually not different, the business may make
unnecessary changes to its marketing or channel strategy.

TYPE II ERROR:
A Type II error occurs when we fail to reject a false null hypothesis.

Business consequence:
If a real difference between Website and App revenue exists but
we fail to detect it, the business may miss an opportunity to
improve the lower-performing channel.

Significance level (alpha): 0.05
""")

print("Hypothesis testing analysis completed successfully.")