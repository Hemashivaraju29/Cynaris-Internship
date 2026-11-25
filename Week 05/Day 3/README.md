# Week 5 Day 3 - Pandas vs DuckDB vs Polars

## Objective

Compare Pandas, DuckDB, and Polars by performing the same analytical operations on a 100,000-row sales dataset.

## Dataset

- File: `data_100k.csv`
- Rows: 100,000
- Columns: 8
- Size: approximately 5.97 MB

### Columns

- `sale_id`
- `customer_name`
- `product`
- `category`
- `quantity`
- `amount`
- `city`
- `payment_method`

## Analytical Operations

The following five operations were performed using all three tools:

1. Count total records.
2. Calculate total sales amount.
3. Calculate average sales amount.
4. Calculate total sales by category.
5. Calculate transaction count and total sales by city.

## Tools Used

### Pandas

Python-based DataFrame library commonly used for data cleaning, transformation, and analysis.

### DuckDB

An analytical SQL database engine used to execute SQL queries directly on data files such as CSV.

### Polars

A fast DataFrame library designed for efficient data processing and transformations.

## Benchmark Results

| Tool   |   Execution Time |
| ------ | ---------------: |
| Pandas | 0.171271 seconds |
| DuckDB | 0.539863 seconds |
| Polars | 0.029665 seconds |

The benchmark was performed locally using the same 100,000-row CSV dataset and the same five analytical operations.

## Files

| File                    | Description                                |
| ----------------------- | ------------------------------------------ |
| `generate_dataset.py`   | Generates the 100,000-row sales dataset    |
| `data_100k.csv`         | 100,000-row dataset used for analysis      |
| `benchmark_day3.py`     | Runs Pandas, DuckDB, and Polars benchmarks |
| `benchmark_results.txt` | Benchmark execution evidence               |
| `comparison.md`         | Pandas vs DuckDB vs Polars comparison      |

## Learning Outcome

This task provided practical experience in using SQL with DuckDB, DataFrame operations with Pandas and Polars, and benchmarking different data-processing approaches on the same dataset.

## Evidence

The benchmark execution output is stored in `benchmark_results.txt`. It contains the execution times and results for all five analytical operations performed with Pandas, DuckDB, and Polars.
