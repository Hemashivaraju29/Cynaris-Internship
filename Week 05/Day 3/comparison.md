# Week 5 Day 3 - Pandas vs DuckDB vs Polars

## Comparison Table

| Criteria        | Pandas                                 | DuckDB                                        | Polars                                             |
| --------------- | -------------------------------------- | --------------------------------------------- | -------------------------------------------------- |
| Syntax          | Python DataFrame API                   | SQL-based analytical queries                  | Python DataFrame API                               |
| Data Processing | In-memory DataFrame processing         | SQL engine optimized for analytical workloads | Fast DataFrame processing with an optimized engine |
| CSV Handling    | `pd.read_csv()`                        | `read_csv_auto()`                             | `pl.read_csv()`                                    |
| Performance     | 0.171271 seconds                       | 0.539863 seconds                              | 0.029665 seconds                                   |
| Suitable Use    | General data analysis and manipulation | SQL analytics and large analytical queries    | Fast data processing and transformation            |

## Benchmark Summary

The same 100,000-row CSV dataset was processed using Pandas, DuckDB, and Polars.

- Pandas execution time: **0.171271 seconds**
- DuckDB execution time: **0.539863 seconds**
- Polars execution time: **0.029665 seconds**

The benchmark times are from the local execution of the Week 5 Day 3 benchmark script. Results can vary depending on hardware, Python environment, caching, and system load.

## Analytical Operations

All three tools performed the same five operations:

1. Count the total number of records.
2. Calculate the total sales amount.
3. Calculate the average sales amount.
4. Calculate total sales grouped by category.
5. Calculate transaction count and total sales grouped by city.

## Conclusion

Pandas provides a familiar Python-based DataFrame interface and is widely useful for general data analysis. DuckDB allows analytical operations to be written directly in SQL and is useful when SQL-based analysis is preferred. Polars provides a DataFrame API with an optimized execution engine and showed the shortest execution time in this local benchmark.
