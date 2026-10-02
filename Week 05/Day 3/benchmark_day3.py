import time
from pathlib import Path

import duckdb
import pandas as pd
import polars as pl


DATA_PATH = Path(__file__).parent / "data_100k.csv"
RESULT_PATH = Path(__file__).parent / "benchmark_results.txt"


def benchmark_pandas():
    start = time.perf_counter()

    df = pd.read_csv(DATA_PATH)

    results = {
        "count": len(df),
        "sum_amount": df["amount"].sum(),
        "avg_amount": df["amount"].mean(),
        "category_sales": (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        ),
        "city_sales": (
            df.groupby("city")
            .agg(
                transactions=("sale_id", "count"),
                total_sales=("amount", "sum"),
            )
            .sort_values("total_sales", ascending=False)
        ),
    }

    elapsed = time.perf_counter() - start

    return results, elapsed


def benchmark_duckdb():
    start = time.perf_counter()

    connection = duckdb.connect()

    queries = {
        "count": f"""
            SELECT COUNT(*) AS count
            FROM read_csv_auto('{DATA_PATH.as_posix()}')
        """,
        "sum_amount": f"""
            SELECT SUM(amount) AS sum_amount
            FROM read_csv_auto('{DATA_PATH.as_posix()}')
        """,
        "avg_amount": f"""
            SELECT AVG(amount) AS avg_amount
            FROM read_csv_auto('{DATA_PATH.as_posix()}')
        """,
        "category_sales": f"""
            SELECT category, SUM(amount) AS total_sales
            FROM read_csv_auto('{DATA_PATH.as_posix()}')
            GROUP BY category
            ORDER BY total_sales DESC
        """,
        "city_sales": f"""
            SELECT
                city,
                COUNT(*) AS transactions,
                SUM(amount) AS total_sales
            FROM read_csv_auto('{DATA_PATH.as_posix()}')
            GROUP BY city
            ORDER BY total_sales DESC
        """,
    }

    results = {}

    results["count"] = connection.execute(
        queries["count"]
    ).fetchone()[0]

    results["sum_amount"] = connection.execute(
        queries["sum_amount"]
    ).fetchone()[0]

    results["avg_amount"] = connection.execute(
        queries["avg_amount"]
    ).fetchone()[0]

    results["category_sales"] = connection.execute(
        queries["category_sales"]
    ).fetchdf()

    results["city_sales"] = connection.execute(
        queries["city_sales"]
    ).fetchdf()

    connection.close()

    elapsed = time.perf_counter() - start

    return results, elapsed


def benchmark_polars():
    start = time.perf_counter()

    df = pl.read_csv(DATA_PATH)

    results = {
        "count": df.height,
        "sum_amount": df["amount"].sum(),
        "avg_amount": df["amount"].mean(),
        "category_sales": (
            df.group_by("category")
            .agg(
                pl.col("amount")
                .sum()
                .alias("total_sales")
            )
            .sort("total_sales", descending=True)
        ),
        "city_sales": (
            df.group_by("city")
            .agg(
                pl.len().alias("transactions"),
                pl.col("amount")
                .sum()
                .alias("total_sales"),
            )
            .sort("total_sales", descending=True)
        ),
    }

    elapsed = time.perf_counter() - start

    return results, elapsed


def main():
    print("Running Pandas benchmark...")
    pandas_results, pandas_time = benchmark_pandas()

    print("Running DuckDB benchmark...")
    duckdb_results, duckdb_time = benchmark_duckdb()

    print("Running Polars benchmark...")
    polars_results, polars_time = benchmark_polars()

    output = []

    output.append("WEEK 5 DAY 3 - PANDAS VS DUCKDB VS POLARS")
    output.append("=" * 60)
    output.append("")
    output.append("Dataset: data_100k.csv")
    output.append("Rows: 100,000")
    output.append("Columns: 8")
    output.append("")

    output.append("BENCHMARK TIMES")
    output.append("-" * 60)
    output.append(f"Pandas :  {pandas_time:.6f} seconds")
    output.append(f"DuckDB : {duckdb_time:.6f} seconds")
    output.append(f"Polars :  {polars_time:.6f} seconds")
    output.append("")

    output.append("QUERY 1 - ROW COUNT")
    output.append("-" * 60)
    output.append(f"Pandas :  {pandas_results['count']}")
    output.append(f"DuckDB : {duckdb_results['count']}")
    output.append(f"Polars :  {polars_results['count']}")
    output.append("")

    output.append("QUERY 2 - TOTAL SALES AMOUNT")
    output.append("-" * 60)
    output.append(
        f"Pandas :  {pandas_results['sum_amount']:.2f}"
    )
    output.append(
        f"DuckDB : {duckdb_results['sum_amount']:.2f}"
    )
    output.append(
        f"Polars :  {polars_results['sum_amount']:.2f}"
    )
    output.append("")

    output.append("QUERY 3 - AVERAGE SALES AMOUNT")
    output.append("-" * 60)
    output.append(
        f"Pandas :  {pandas_results['avg_amount']:.2f}"
    )
    output.append(
        f"DuckDB : {duckdb_results['avg_amount']:.2f}"
    )
    output.append(
        f"Polars :  {polars_results['avg_amount']:.2f}"
    )
    output.append("")

    output.append("QUERY 4 - SALES BY CATEGORY")
    output.append("-" * 60)
    output.append("Pandas:")
    output.append(str(pandas_results["category_sales"]))
    output.append("")
    output.append("DuckDB:")
    output.append(str(duckdb_results["category_sales"]))
    output.append("")
    output.append("Polars:")
    output.append(str(polars_results["category_sales"]))
    output.append("")

    output.append("QUERY 5 - SALES BY CITY")
    output.append("-" * 60)
    output.append("Pandas:")
    output.append(str(pandas_results["city_sales"]))
    output.append("")
    output.append("DuckDB:")
    output.append(str(duckdb_results["city_sales"]))
    output.append("")
    output.append("Polars:")
    output.append(str(polars_results["city_sales"]))
    output.append("")

    RESULT_PATH.write_text(
        "\n".join(output),
        encoding="utf-8",
    )

    print("")
    print("Benchmark completed successfully.")
    print(f"Results saved to: {RESULT_PATH}")
    print("")
    print("Execution times:")
    print(f"Pandas :  {pandas_time:.6f} seconds")
    print(f"DuckDB : {duckdb_time:.6f} seconds")
    print(f"Polars :  {polars_time:.6f} seconds")


if __name__ == "__main__":
    main()