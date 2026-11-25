\# Week 5 Day 4 - DuckDB and Polars Analytics



\## Objective



Perform analytical operations on a 100,000-row CSV dataset using Pandas, DuckDB, and Polars, then compare their syntax, processing approach, and execution time.



\## Dataset



The dataset contains 100,000 sales records with 8 columns:



\- `sale\_id`

\- `customer\_id`

\- `product`

\- `category`

\- `quantity`

\- `amount`

\- `city`

\- `payment\_method`



Dataset file: `data\_100k.csv`



\## Tasks Completed



\### 1. DuckDB Analysis



Loaded the CSV directly into DuckDB and performed five analytical operations:



1\. Count total records

2\. Calculate total sales amount

3\. Calculate average sales amount

4\. Group sales by category

5\. Group transactions and sales by city



\### 2. Polars Analysis



Loaded the same CSV using Polars and performed the same five operations.



\### 3. Pandas Benchmark



The same operations were performed using Pandas to compare execution times.



\## Benchmark Results



| Tool | Execution Time |

|---|---:|

| Pandas | 0.105989 seconds |

| DuckDB | 0.538168 seconds |

| Polars | 0.113329 seconds |



The timings are specific to this local machine, dataset, and benchmark implementation.



\## Key Results



\- Total records: 100,000

\- Total sales amount: 5,012,749,286.61

\- Average sales amount: 50,127.49

\- Highest category sales: Accessories

\- Highest city sales: Mumbai



All three tools produced matching analytical results.



\## Tool Comparison



| Criteria | Pandas | DuckDB | Polars |

|---|---|---|---|

| Syntax | Python / DataFrame | SQL | Python / DataFrame |

| Data processing | DataFrame-based | SQL-based | DataFrame-based |

| CSV analysis | DataFrame operations | Direct SQL on CSV | DataFrame operations |

| Benchmark time | 0.105989 s | 0.538168 s | 0.113329 s |

| Suitable use | General data analysis | SQL analytics on files | Fast DataFrame processing |



\## Files



\- `generate\_dataset.py` - Generates the 100,000-row dataset

\- `data\_100k.csv` - Benchmark dataset

\- `benchmark\_day4.py` - Runs Pandas, DuckDB, and Polars benchmarks

\- `benchmark\_results.txt` - Benchmark execution evidence

\- `comparison.md` - Detailed comparison of the three tools

\- `README.md` - Day 4 documentation



\## Conclusion



Pandas provided a familiar Python-based approach for general data analysis. DuckDB allowed SQL queries to be executed directly on the CSV file. Polars provided a Python DataFrame approach similar to Pandas. For this particular 100,000-row benchmark, Pandas recorded the shortest execution time, followed closely by Polars, while DuckDB took longer for the tested workflow.

