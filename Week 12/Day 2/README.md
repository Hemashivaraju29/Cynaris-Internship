# Week 12 - Day 2: Performance Optimisation with DuckDB and Query Caching

## 1. Project Objective

The objective of this task is to explore in-process SQL analytics using DuckDB, compare its query performance with Pandas, and implement a reusable SQL-to-DataFrame function and an in-memory query-result cache.

## 2. Dataset

- **Dataset:** 100K-row sales dataset
- **Source:** Reused from `Week 05/Day 4/data_100k.csv`
- **Total records:** 100,000
- **Columns:** sale_id, customer_id, product, category, quantity, amount, city, payment_method
- **Missing values:** None

The CSV is loaded directly into an in-memory DuckDB table.

## 3. Project Structure

```text
Week 12/
â””â”€â”€ Day 2/
    â”œâ”€â”€ outputs/
    â”‚   â”œâ”€â”€ total_sales.csv
    â”‚   â”œâ”€â”€ category_performance.csv
    â”‚   â”œâ”€â”€ city_performance.csv
    â”‚   â”œâ”€â”€ top_products.csv
    â”‚   â”œâ”€â”€ payment_analysis.csv
    â”‚   â””â”€â”€ performance_benchmark.csv
    â”œâ”€â”€ src/
    â”‚   â”œâ”€â”€ duckdb_analytics.py
    â”‚   â”œâ”€â”€ benchmark.py
    â”‚   â””â”€â”€ query_cache.py
    â”œâ”€â”€ tests/
    â”‚   â””â”€â”€ test_duckdb_analytics.py
    â”œâ”€â”€ requirements.txt
    â””â”€â”€ README.md
```

## 4. DuckDB Analytical Queries

Five analytical SQL queries were implemented:

1. **Total Sales:** Calculates transaction count, total quantity, revenue and average transaction value.
2. **Category Performance:** Analyses units sold and revenue by product category.
3. **City Performance:** Calculates transactions and revenue by city.
4. **Top Products:** Identifies the ten highest-revenue products.
5. **Payment Analysis:** Compares transaction count and revenue by payment method.

All five query results are exported as CSV files in the outputs directory.

## 5. DuckDB vs Pandas Performance Benchmark

Three equivalent analytical operations were benchmarked using DuckDB and Pandas:

| Query               | DuckDB Average (ms) | Pandas Average (ms) | Faster Engine |
| ------------------- | ------------------: | ------------------: | ------------- |
| Revenue by city     |               7.559 |               6.571 | Pandas        |
| Revenue by category |               7.505 |               6.635 | Pandas        |
| Payment performance |               7.760 |              10.454 | DuckDB        |

### Findings

- Pandas performed better for city and category revenue aggregation.
- DuckDB performed better for payment performance.
- DuckDB was approximately 1.35 times faster for payment performance.
- Both engines returned equivalent results.

The benchmark uses five repeated measurements and compares average query execution times. Data loading is excluded from the timings. Results are specific to the local machine and environment.

## 6. SQL-to-Pandas DataFrame Function

The `query_to_dataframe()` function accepts an SQL query string, executes it using DuckDB, and returns the result as a Pandas DataFrame.

This provides a reusable interface between SQL analytics and Python-based data analysis.

## 7. Query Caching

A simple in-memory `QueryCache` class was implemented.

Features:

- Generates a SHA-256 cache key using the SQL query and data version.
- Executes the query when the cache is empty.
- Returns stored results for repeated queries.
- Returns copies of cached DataFrames.
- Supports clearing the cache.
- Uses a data-version parameter to distinguish results from different dataset versions.

The data version must be updated whenever the underlying dataset changes to avoid reusing stale results.

## 8. Automated Testing

Pytest was used to validate the implementation.

**Test results: 6 passed**

Tests cover:

- Loading the 100K-row CSV.
- Returning query results as a Pandas DataFrame.
- Correct SQL aggregation.
- Rejecting empty SQL queries.
- Query-cache hit behaviour.
- Separate cache entries for different data versions.

## 9. Installation and Execution

Install dependencies:

```bash
pip install -r "Week 12/Day 2/requirements.txt"
```

Run DuckDB analytics:

```bash
python "Week 12/Day 2/src/duckdb_analytics.py"
```

Run the performance benchmark:

```bash
python "Week 12/Day 2/src/benchmark.py"
```

Run automated tests:

```bash
python -m pytest "Week 12/Day 2/tests" -v
```

## 10. Tools and Technologies

- Python 3.11
- DuckDB
- Pandas
- SQL
- Pytest
- Hashlib
- Time / performance_counter
- CSV
- VS Code
- PowerShell
- Git and GitHub

## 11. Conclusion

This task demonstrated how DuckDB can perform in-process SQL analytics directly on CSV data. The performance comparison showed that the fastest engine depends on the analytical operation. A reusable SQL-to-DataFrame function and a simple query-result cache were also implemented and tested successfully.


