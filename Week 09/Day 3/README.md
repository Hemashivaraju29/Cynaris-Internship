# W9D3: A/B Test Tracking with MLflow

## Objective

Compare two groups using A/B testing and track the experiment using MLflow.

## Implementation

- Created sample control (A) and treatment (B) datasets.
- Calculated visitors, conversions, and conversion rates.
- Applied the Chi-square statistical test.
- Tracked experiment parameters and metrics using MLflow.
- Saved the comparison results as a CSV artifact.

## Results

| Metric          | Group A | Group B |
| --------------- | ------: | ------: |
| Visitors        |    1135 |    1135 |
| Conversions     |     113 |     169 |
| Conversion Rate |   9.96% |  14.89% |

- Chi-square statistic: 12.2486
- P-value: 0.0005
- Conclusion: Statistically significant difference.

Group B achieved a higher conversion rate in this sample.

## How to Run

```powershell
python "Week 09\Day 3\ab_test_tracking.py"
```

## Tools Used

Python, Pandas, SciPy, MLflow, SQLite, VS Code, PowerShell, Git, GitHub.
