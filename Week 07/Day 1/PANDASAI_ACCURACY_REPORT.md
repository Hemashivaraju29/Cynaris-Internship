# PandasAI vs Manual Pandas - Accuracy Report

## Dataset
- Dataset: Nifty 500 combined EDA CSV
- Rows: 7,395
- Columns: 8
- Unique companies: 3
- Missing values: None in the inspected columns

## Observed Results
1. Row count: Manual Pandas returned 7,395; PandasAI returned 1.
2. Unique companies: Both returned 3.
3. Average closing price: Manual Pandas returned 1,096.7013; PandasAI returned approximately 1,097.2978, which corresponds to the average Open value rather than Close.
4. Highest closing price: PandasAI generated the correct numeric value but failed to return a usable final response.
5. Lowest closing price: The numeric value matched, but PandasAI output validation failed.
6. Total trading volume: The numeric value matched, but PandasAI output validation failed.
7. Company with most records: All three companies tie at 2,465 records; PandasAI generated conflicting rankings.
8. Average closing price by company: Manual Pandas results verified; PandasAI result not verified.
9. Date with highest total daily volume: Manual Pandas result verified as 2017-02-17, with total volume 210,705,356; PandasAI result not verified.
10. Missing values: Manual Pandas found zero missing values in every column; PandasAI result not verified.

## Conclusion
Manual Pandas provided a reliable baseline for validating the generated answers.
PandasAI demonstrated that it can answer some natural-language questions, but the local model sometimes generated incorrect calculations, inconsistent answers, or outputs that failed validation.

A completed query is not necessarily a correct query. Answers should be checked against deterministic Pandas calculations.

## Error Handling
The Python script catches query exceptions, logs errors, and continues to the next question. Failed outputs are recorded in query_results.txt, and error details are recorded in pandasai_errors.log.

