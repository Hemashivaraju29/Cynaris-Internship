import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from pathlib import Path

# W5D5: AI-Powered EDA on Indian Business Dataset
# Exploratory Data Analysis of selected NIFTY 500 companies.

DATA_DIR = Path(__file__).parent
COMBINED_FILE = DATA_DIR / "nifty500_combined_eda.csv"


def load_data():
    """Load the combined NIFTY 500 dataset."""
    df = pd.read_csv(COMBINED_FILE)

    # Convert Date column to datetime.
    df["Date"] = pd.to_datetime(df["Date"])

    return df


def basic_eda(df):
    """Display basic dataset information."""
    print("\n=== BASIC DATASET INFORMATION ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\n=== DATA TYPES ===")
    print(df.dtypes)

    print("\n=== MISSING VALUES ===")
    print(df.isnull().sum())

    print("\n=== DUPLICATE ROWS ===")
    print(df.duplicated().sum())


def descriptive_statistics(df):
    """Display descriptive statistics for numerical columns."""
    print("\n=== DESCRIPTIVE STATISTICS ===")
    print(df.describe())


def company_summary(df):
    """Compare companies using average closing price and volume."""
    summary = (
        df.groupby("Company")
        .agg(
            Average_Close=("Close", "mean"),
            Maximum_Close=("Close", "max"),
            Minimum_Close=("Close", "min"),
            Average_Volume=("Volume", "mean"),
        )
        .round(2)
        .sort_values("Average_Close", ascending=False)
    )

    print("\n=== COMPANY-WISE SUMMARY ===")
    print(summary)

    summary.to_csv(DATA_DIR / "company_summary.csv")

    return summary


def correlation_analysis(df):
    """Calculate correlations between numerical market variables."""
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
    ]

    correlation = df[numeric_columns].corr().round(3)

    print("\n=== CORRELATION MATRIX ===")
    print(correlation)

    correlation.to_csv(DATA_DIR / "correlation_matrix.csv")

    return correlation


def hypothesis_testing(df):
    """
    Compare the daily returns of TCS and Reliance
    using an independent two-sample t-test.
    """

    # Calculate daily percentage return separately for each company.
    df = df.sort_values(["Company", "Date"]).copy()

    df["Daily_Return"] = (
        df.groupby("Company")["Close"].pct_change() * 100
    )

    # Remove the first row of each company because it has no previous-day value.
    tcs_returns = df.loc[
        df["Company"] == "TCS", "Daily_Return"
    ].dropna()

    reliance_returns = df.loc[
        df["Company"] == "Reliance", "Daily_Return"
    ].dropna()

    # Independent two-sample t-test.
    t_statistic, p_value = ttest_ind(
        tcs_returns,
        reliance_returns,
        equal_var=False
    )

    print("\n=== HYPOTHESIS TESTING ===")
    print("Test: Independent two-sample t-test")
    print("Comparison: TCS vs Reliance daily returns")
    print("H0: Mean daily returns of TCS and Reliance are equal.")
    print("H1: Mean daily returns of TCS and Reliance are different.")
    print(f"TCS mean daily return: {tcs_returns.mean():.4f}%")
    print(f"Reliance mean daily return: {reliance_returns.mean():.4f}%")
    print(f"T-statistic: {t_statistic:.4f}")
    print(f"P-value: {p_value:.6f}")

    alpha = 0.05

    if p_value < alpha:
        conclusion = (
            "Reject H0: There is a statistically significant "
            "difference between the mean daily returns."
        )
    else:
        conclusion = (
            "Fail to reject H0: There is not enough evidence "
            "of a statistically significant difference."
        )

    print(f"Conclusion: {conclusion}")

    # Save results for the project evidence.
    results = [
        "HYPOTHESIS TESTING RESULTS",
        "==========================",
        "Test: Independent two-sample t-test",
        "Comparison: TCS vs Reliance daily returns",
        "",
        "H0: Mean daily returns of TCS and Reliance are equal.",
        "H1: Mean daily returns of TCS and Reliance are different.",
        "",
        f"TCS mean daily return: {tcs_returns.mean():.4f}%",
        f"Reliance mean daily return: {reliance_returns.mean():.4f}%",
        f"T-statistic: {t_statistic:.4f}",
        f"P-value: {p_value:.6f}",
        f"Significance level: {alpha}",
        "",
        f"Conclusion: {conclusion}",
    ]

    with open(
        DATA_DIR / "hypothesis_test_results.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("\n".join(results))


def create_visualizations(df):
    """Create basic EDA visualizations."""

    # Average closing price by company
    avg_close = df.groupby("Company")["Close"].mean()

    plt.figure(figsize=(8, 5))
    avg_close.plot(kind="bar")
    plt.title("Average Closing Price by Company")
    plt.xlabel("Company")
    plt.ylabel("Average Closing Price")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(
        DATA_DIR / "average_closing_price.png",
        dpi=150
    )
    plt.close()

    # Average trading volume by company
    avg_volume = df.groupby("Company")["Volume"].mean()

    plt.figure(figsize=(8, 5))
    avg_volume.plot(kind="bar")
    plt.title("Average Trading Volume by Company")
    plt.xlabel("Company")
    plt.ylabel("Average Volume")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(
        DATA_DIR / "average_trading_volume.png",
        dpi=150
    )
    plt.close()

    print("\n=== VISUALIZATIONS CREATED ===")
    print("average_closing_price.png")
    print("average_trading_volume.png")


def main():
    df = load_data()

    basic_eda(df)
    descriptive_statistics(df)
    company_summary(df)
    correlation_analysis(df)
    hypothesis_testing(df)
    create_visualizations(df)


if __name__ == "__main__":
    main()