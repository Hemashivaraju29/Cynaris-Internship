\# Pandas vs DuckDB vs Polars Comparison



\## Benchmark Dataset



\- Dataset: `data\_100k.csv`

\- Rows: 100,000

\- Columns: 8

\- Operations tested: 5 analytical operations

\- All three tools produced matching analytical results.



\## Performance Comparison



| Criteria | Pandas | DuckDB | Polars |

|---|---|---|---|

| Syntax | Python / DataFrame | SQL | Python / DataFrame |

| Data processing | DataFrame-based | SQL-based | DataFrame-based |

| CSV analysis | `read\_csv()` and DataFrame operations | Direct SQL queries on CSV | `read\_csv()` and DataFrame operations |

| Benchmark time | 0.105989 seconds | 0.538168 seconds | 0.113329 seconds |

| Suitable use | General data analysis and manipulation | SQL analytics directly on files | Fast DataFrame-based data processing |



\## Analytical Operations



The following five operations were performed using all three tools:



1\. Count total records

2\. Calculate total sales amount

3\. Calculate average sales amount

4\. Group sales by category

5\. Group transactions and sales by city



\## Benchmark Results



| Metric | Result |

|---|---:|

| Record count | 100,000 |

| Total amount | 5,012,749,286.61 |

| Average amount | 50,127.49 |



\### Category Sales



| Category | Total Sales |

|---|---:|

| Accessories | 1,673,718,088.53 |

| Computers | 1,672,342,996.39 |

| Electronics | 1,666,688,201.69 |



\### City Sales



| City | Transactions | Total Sales |

|---|---:|---:|

| Mumbai | 20,176 | 1,017,700,770.96 |

| Chennai | 20,110 | 1,011,403,070.93 |

| Hyderabad | 19,989 | 996,372,859.30 |

| Delhi | 19,939 | 994,319,172.47 |

| Bengaluru | 19,786 | 992,953,412.95 |



\## Speed Observation



For this 100,000-row CSV benchmark, Pandas completed the tested workflow in 0.105989 seconds, while Polars took 0.113329 seconds and DuckDB took 0.538168 seconds. These timings are specific to this local machine, dataset, and benchmark implementation.



\## Syntax Comparison



\### Pandas



Pandas uses Python DataFrame operations such as `groupby()`, `agg()`, and `sort\_values()`.



\### DuckDB



DuckDB uses SQL syntax and can query the CSV file directly without first loading the complete dataset into a Pandas DataFrame.



\### Polars



Polars provides a Python DataFrame API with operations such as `group\_by()`, `agg()`, and `sort()`.



\## Conclusion



Pandas provided a familiar Python-based approach for general data analysis. DuckDB allowed the same analytical tasks to be expressed directly using SQL against the CSV file. Polars provided a DataFrame-based Python approach with syntax similar to Pandas. In this particular 100,000-row benchmark, Pandas recorded the shortest execution time, followed closely by Polars, while DuckDB took longer for this specific workflow.

