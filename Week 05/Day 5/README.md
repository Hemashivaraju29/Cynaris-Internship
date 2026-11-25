# Week 5 Day 5 — AI-Powered EDA on Indian Business Dataset

## Project Overview

This project performs exploratory data analysis (EDA) on selected NIFTY 500 company stock datasets.

The analysis focuses on:

- Data quality checks
- Descriptive statistics
- Company-wise comparison
- Correlation analysis
- Data visualization
- Statistical hypothesis testing

## Dataset

The stock datasets contain daily market information for selected NIFTY 500 companies.

Companies analyzed:

- Reliance
- TCS
- HDFC Bank

The combined dataset contains:

- 7,395 rows
- 8 columns
- Data period: 2012–2021

### Columns

| Column    | Description            |
| --------- | ---------------------- |
| Date      | Trading date           |
| Open      | Opening price          |
| High      | Highest price          |
| Low       | Lowest price           |
| Close     | Closing price          |
| Adj Close | Adjusted closing price |
| Volume    | Trading volume         |
| Company   | Company name           |

## Data Quality Checks

The following checks were performed:

- Missing value detection
- Duplicate row detection
- Data type verification
- Date conversion to datetime

Results:

- Missing values: 0
- Duplicate rows: 0

## Descriptive Analysis

Descriptive statistics were generated for the numerical market variables.

Company-wise average closing prices:

| Company   | Average Close |
| --------- | ------------: |
| TCS       |       1589.00 |
| Reliance  |        926.73 |
| HDFC Bank |        774.37 |

Company-wise average trading volume:

| Company   | Average Volume |
| --------- | -------------: |
| Reliance  |   8,665,124.78 |
| HDFC Bank |   5,930,289.92 |
| TCS       |   2,781,300.78 |

## Correlation Analysis

A correlation matrix was calculated for:

- Open
- High
- Low
- Close
- Adj Close
- Volume

The price variables show very strong positive correlations with each other.

For example:

- Open vs Close: 1.000
- High vs Close: 1.000
- Low vs Close: 1.000
- Close vs Adj Close: 0.998

Trading volume has a much weaker relationship with the price variables.

## Statistical Hypothesis Testing

An independent two-sample t-test was performed on the daily returns of TCS and Reliance.

### Hypotheses

**Null hypothesis (H0):**

The mean daily returns of TCS and Reliance are equal.

**Alternative hypothesis (H1):**

The mean daily returns of TCS and Reliance are different.

### Results

- TCS mean daily return: 0.0873%
- Reliance mean daily return: 0.0937%
- T-statistic: -0.1321
- P-value: 0.894918
- Significance level: 0.05

Since the p-value is greater than 0.05, the null hypothesis is not rejected.

### Conclusion

There is not enough statistical evidence to conclude that the mean daily returns of TCS and Reliance are significantly different in this dataset.

## Visualizations

The following visualizations were generated:

1. `average_closing_price.png`
2. `average_trading_volume.png`

These charts provide a visual comparison of the selected companies.

## Project Files

```text
Week 05/Day 5/
├── 000_RELIANCE.csv
├── 001_TCS.csv
├── 003_HDFCBANK.csv
├── average_closing_price.png
├── average_trading_volume.png
├── company_summary.csv
├── correlation_matrix.csv
├── eda_analysis.py
├── hypothesis_test_results.txt
├── nifty500_combined_eda.csv
└── README.md
```
