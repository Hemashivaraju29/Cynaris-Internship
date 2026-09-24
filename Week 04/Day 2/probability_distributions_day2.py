import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ============================================================
# WEEK 4 - DAY 2: PROBABILITY & DISTRIBUTIONS
# ============================================================

# Load dataset
file_path = "Checkpoint-2/data/da_sales_transactions.csv"
df = pd.read_csv(file_path)

# ============================================================
# TASK 1: BASIC PROBABILITIES USING CONTINGENCY TABLE
# ============================================================

# Event A: Transaction was returned
# Event B: Transaction was made through Website

total_transactions = len(df)

returns = df["Return_Flag"] == 1
website = df["Channel"] == "Website"

# Basic probabilities
p_A = returns.mean()
p_B = website.mean()

# Joint probability P(A and B)
p_A_and_B = (returns & website).mean()

# Conditional probability P(A | B)
p_A_given_B = (returns & website).sum() / website.sum()

# Create contingency table
contingency_table = pd.crosstab(
    df["Channel"],
    df["Return_Flag"]
)

print("=" * 60)
print("TASK 1: BASIC PROBABILITIES")
print("=" * 60)

print("\nContingency Table:")
print(contingency_table)

print(f"\nTotal Transactions: {total_transactions}")
print(f"P(A) - Probability of Return: {p_A:.4f}")
print(f"P(B) - Probability of Website Channel: {p_B:.4f}")
print(f"P(A ∩ B) - Return AND Website: {p_A_and_B:.4f}")
print(f"P(A | B) - Return given Website: {p_A_given_B:.4f}")

# Save probability results
probability_summary = pd.DataFrame({
    "Measure": [
        "Total Transactions",
        "P(A) - Return",
        "P(B) - Website",
        "P(A and B) - Return and Website",
        "P(A given B) - Return given Website"
    ],
    "Value": [
        total_transactions,
        p_A,
        p_B,
        p_A_and_B,
        p_A_given_B
    ]
})

probability_summary.to_csv(
    "Week 04/Day 2/probability_summary.csv",
    index=False
)

print("\nProbability summary saved successfully.")

# ============================================================
# TASK 2: NORMAL DISTRIBUTION - 68-95-99.7 RULE
# ============================================================

# Standard normal distribution
x = np.linspace(-4, 4, 1000)
y = norm.pdf(x, 0, 1)

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)

# Shade areas for the 68-95-99.7 rule
plt.fill_between(
    x, y,
    where=(x >= -1) & (x <= 1),
    alpha=0.4,
    label="68.27% within ±1 SD"
)

plt.fill_between(
    x, y,
    where=(x >= -2) & (x <= 2),
    alpha=0.2,
    label="95.45% within ±2 SD"
)

plt.fill_between(
    x, y,
    where=(x >= -3) & (x <= 3),
    alpha=0.1,
    label="99.73% within ±3 SD"
)

# Mark standard deviations
for value in [-3, -2, -1, 0, 1, 2, 3]:
    plt.axvline(value, linestyle="--", linewidth=0.8)

plt.title("Standard Normal Distribution - 68-95-99.7 Rule")
plt.xlabel("Standard Deviations from Mean")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    "Week 04/Day 2/normal_distribution.png",
    dpi=300
)

plt.show()

print("\nNormal distribution plot saved successfully.")
print("68-95-99.7 Rule:")
print("Approximately 68.27% of values lie within ±1 standard deviation.")
print("Approximately 95.45% of values lie within ±2 standard deviations.")
print("Approximately 99.73% of values lie within ±3 standard deviations.")

# ============================================================
# TASK 3: BINOMIAL DISTRIBUTION USING NUMPY
# ============================================================

# Parameters
n = 10          # Number of trials
p = 0.5         # Probability of success
simulations = 10000

# Simulate binomial distribution
binomial_results = np.random.binomial(
    n=n,
    p=p,
    size=simulations
)

# Plot distribution
plt.figure(figsize=(10, 6))

values, counts = np.unique(
    binomial_results,
    return_counts=True
)

probabilities = counts / simulations

plt.bar(
    values,
    probabilities,
    alpha=0.7
)

plt.title("Binomial Distribution Simulation")
plt.xlabel("Number of Successes")
plt.ylabel("Probability")
plt.xticks(range(n + 1))
plt.grid(axis="y", alpha=0.2)

plt.tight_layout()

plt.savefig(
    "Week 04/Day 2/binomial_distribution.png",
    dpi=300
)

plt.show()

print("\nBinomial distribution plot saved successfully.")
print(f"Number of trials (n): {n}")
print(f"Probability of success (p): {p}")
print(f"Number of simulations: {simulations}")
print(f"Mean of simulated results: {binomial_results.mean():.4f}")
print(f"Standard deviation of simulated results: {binomial_results.std():.4f}")

# ============================================================
# TASK 4: CENTRAL LIMIT THEOREM (CLT)
# ============================================================

# Create revenue column
df["Revenue"] = (
    df["Units"]
    * df["Unit_Price"]
    * (1 - df["Discount_Pct"] / 100)
)

# Population
population = df["Revenue"].dropna()

# Sampling parameters
sample_size = 30
number_of_samples = 1000

# Generate sample means
sample_means = []

for _ in range(number_of_samples):
    sample = np.random.choice(
        population,
        size=sample_size,
        replace=True
    )
    sample_means.append(sample.mean())

sample_means = np.array(sample_means)

# Plot sampling distribution
plt.figure(figsize=(10, 6))

plt.hist(
    sample_means,
    bins=30,
    density=True,
    alpha=0.7
)

plt.axvline(
    sample_means.mean(),
    linestyle="--",
    linewidth=2,
    label=f"Mean = {sample_means.mean():.2f}"
)

plt.title("Central Limit Theorem - Sampling Distribution of Mean Revenue")
plt.xlabel("Sample Mean Revenue")
plt.ylabel("Density")
plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()

plt.savefig(
    "Week 04/Day 2/central_limit_theorem.png",
    dpi=300
)

plt.show()

print("\nCentral Limit Theorem plot saved successfully.")
print(f"Population size: {len(population)}")
print(f"Sample size: {sample_size}")
print(f"Number of samples: {number_of_samples}")
print(f"Mean of sample means: {sample_means.mean():.2f}")
print(f"Standard deviation of sample means: {sample_means.std():.2f}")

print("\nCLT Explanation:")
print(
    "When many random samples are taken from a population, "
    "the distribution of their sample means becomes approximately normal."
)