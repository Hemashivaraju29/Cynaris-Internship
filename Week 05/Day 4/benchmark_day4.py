import time
import pandas as pd
import duckdb
import polars as pl

CSV_PATH = r"Week 05\Day 4\data_100k.csv"


def run_pandas():
    start = time.perf_counter()

    df = pd.read_csv(CSV_PATH)

    results = {}

    results["count"] = len(df)
    results["sum_amount"] = df["amount"].sum()
    results["avg_amount"] = df["amount"].mean()

    results["category_sales"] = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    results["city_sales"] = (
        df.groupby("city")
        .agg(
            transactions=("sale_id", "count"),
            total_sales=("amount", "sum")
        )
        .sort_values("total_sales", ascending=False)
    )

    elapsed = time.perf_counter() - start
    return elapsed, results


def run_duckdb():
    start = time.perf_counter()

    con = duckdb.connect()

    results = {}

    results["count"] = con.execute(
        f"SELECT COUNT(*) FROM '{CSV_PATH}'"
    ).fetchone()[0]

    results["sum_amount"] = con.execute(
        f"SELECT SUM(amount) FROM '{CSV_PATH}'"
    ).fetchone()[0]

    results["avg_amount"] = con.execute(
        f"SELECT AVG(amount) FROM '{CSV_PATH}'"
    ).fetchone()[0]

    results["category_sales"] = con.execute(
        f"""
        SELECT category, SUM(amount) AS total_sales
        FROM '{CSV_PATH}'
        GROUP BY category
        ORDER BY total_sales DESC
        """
    ).fetchall()

    results["city_sales"] = con.execute(
        f"""
        SELECT city,
               COUNT(*) AS transactions,
               SUM(amount) AS total_sales
        FROM '{CSV_PATH}'
        GROUP BY city
        ORDER BY total_sales DESC
        """
    ).fetchall()

    con.close()

    elapsed = time.perf_counter() - start
    return elapsed, results


def run_polars():
    start = time.perf_counter()

    df = pl.read_csv(CSV_PATH)

    results = {}

    results["count"] = df.height
    results["sum_amount"] = df["amount"].sum()
    results["avg_amount"] = df["amount"].mean()

    results["category_sales"] = (
        df.group_by("category")
        .agg(pl.col("amount").sum().alias("total_sales"))
        .sort("total_sales", descending=True)
    )

    results["city_sales"] = (
        df.group_by("city")
        .agg(
            pl.len().alias("transactions"),
            pl.col("amount").sum().alias("total_sales")
        )
        .sort("total_sales", descending=True)
    )

    elapsed = time.perf_counter() - start
    return elapsed, results


print("=" * 60)
print("WEEK 5 DAY 4 - PANDAS vs DUCKDB vs POLARS")
print("=" * 60)

pandas_time, pandas_results = run_pandas()
duckdb_time, duckdb_results = run_duckdb()
polars_time, polars_results = run_polars()

print("\nPANDAS")
print("-" * 40)
print(f"Time: {pandas_time:.6f} seconds")
print(f"Record count: {pandas_results['count']}")
print(f"Total amount: {pandas_results['sum_amount']:.2f}")
print(f"Average amount: {pandas_results['avg_amount']:.2f}")
print("Category sales:")
print(pandas_results["category_sales"])
print("City sales:")
print(pandas_results["city_sales"])

print("\nDUCKDB")
print("-" * 40)
print(f"Time: {duckdb_time:.6f} seconds")
print(f"Record count: {duckdb_results['count']}")
print(f"Total amount: {duckdb_results['sum_amount']:.2f}")
print(f"Average amount: {duckdb_results['avg_amount']:.2f}")
print("Category sales:")
print(duckdb_results["category_sales"])
print("City sales:")
print(duckdb_results["city_sales"])

print("\nPOLARS")
print("-" * 40)
print(f"Time: {polars_time:.6f} seconds")
print(f"Record count: {polars_results['count']}")
print(f"Total amount: {polars_results['sum_amount']:.2f}")
print(f"Average amount: {polars_results['avg_amount']:.2f}")
print("Category sales:")
print(polars_results["category_sales"])
print("City sales:")
print(polars_results["city_sales"])

print("\n" + "=" * 60)
print("BENCHMARK SUMMARY")
print("=" * 60)
print(f"Pandas : {pandas_time:.6f} seconds")
print(f"DuckDB : {duckdb_time:.6f} seconds")
print(f"Polars : {polars_time:.6f} seconds")