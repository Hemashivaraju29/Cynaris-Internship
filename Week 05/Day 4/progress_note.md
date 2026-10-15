\# Week 5 Day 4 Progress Note



\## Topic



DuckDB and Polars Analytics



\## Work Completed



\- Created a 100,000-row sales CSV dataset with 8 columns.

\- Loaded and analyzed the dataset using Pandas.

\- Used DuckDB to run SQL queries directly on the CSV file.

\- Loaded the same dataset using Polars.

\- Performed the same five analytical operations with all three tools:

&#x20; 1. Record count

&#x20; 2. Total sales amount

&#x20; 3. Average sales amount

&#x20; 4. Sales grouped by category

&#x20; 5. Transactions and sales grouped by city

\- Benchmarked the execution time of Pandas, DuckDB, and Polars.

\- Documented syntax, processing approach, performance, and suitable use cases.



\## Benchmark Results



| Tool | Execution Time |

|---|---:|

| Pandas | 0.105989 seconds |

| DuckDB | 0.538168 seconds |

| Polars | 0.113329 seconds |



All three tools produced matching analytical results for the tested operations.



\## Deliverables



\- `generate\_dataset.py`

\- `data\_100k.csv`

\- `benchmark\_day4.py`

\- `benchmark\_results.txt`

\- `comparison.md`

\- `README.md`



\## Learning Outcome



I learned how Pandas, DuckDB, and Polars can be used for analytical processing of CSV data. I also learned how SQL-based analysis with DuckDB differs from DataFrame-based analysis with Pandas and Polars, and how to perform a basic local performance benchmark.

