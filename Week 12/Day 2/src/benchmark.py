
"""Benchmark DuckDB against Pandas on the same 100K-row dataset."""

from pathlib import Path
import time

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = PROJECT_ROOT / "Week 05" / "Day 4" / "data_100k.csv"
OUTPUT_PATH = (
    Path(__file__).resolve().parents[1]
    / "outputs"
    / "performance_benchmark.csv"
)

QUERIES = {
    "revenue_by_city": """
        SELECT city, SUM(amount) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC
    """,
    "revenue_by_category": """
        SELECT category, SUM(amount) AS revenue
        FROM sales
        GROUP BY category
        ORDER BY revenue DESC
    """,
    "payment_performance": """
        SELECT
            payment_method,
            COUNT(*) AS transactions,
            SUM(amount) AS revenue
        FROM sales
        GROUP BY payment_method
        ORDER BY revenue DESC
    """,
}


def pandas_query(df, name):
    """Run only the Pandas aggregation matching the requested SQL query."""

    if name == "revenue_by_city":
        return (
            df.groupby("city", as_index=False)["amount"]
            .sum()
            .rename(columns={"amount": "revenue"})
            .sort_values("revenue", ascending=False)
            .reset_index(drop=True)
        )

    if name == "revenue_by_category":
        return (
            df.groupby("category", as_index=False)["amount"]
            .sum()
            .rename(columns={"amount": "revenue"})
            .sort_values("revenue", ascending=False)
            .reset_index(drop=True)
        )

    if name == "payment_performance":
        return (
            df.groupby("payment_method")
            .agg(
                transactions=("sale_id", "count"),
                revenue=("amount", "sum"),
            )
            .reset_index()
            .sort_values("revenue", ascending=False)
            .reset_index(drop=True)
        )

    raise ValueError(f"Unknown benchmark query: {name}")


def benchmark(iterations=5):
    """Compare equivalent repeated query execution times."""
    df = pd.read_csv(DATA_PATH)

    connection = duckdb.connect(database=":memory:")

    try:
        connection.execute(
            "CREATE TABLE sales AS SELECT * FROM read_csv_auto(?)",
            [str(DATA_PATH)],
        )

        records = []

        for name, sql in QUERIES.items():
            # Warm up and verify that both engines return equivalent results.
            duckdb_result = connection.execute(sql).fetchdf()
            pandas_result = pandas_query(df, name)

            pd.testing.assert_frame_equal(
                duckdb_result.reset_index(drop=True),
                pandas_result.reset_index(drop=True),
                check_dtype=False,
                check_exact=False,
                rtol=1e-9,
                atol=1e-6,
            )

            duckdb_times = []
            pandas_times = []

            for _ in range(iterations):
                start = time.perf_counter()
                connection.execute(sql).fetchdf()
                duckdb_times.append(
                    (time.perf_counter() - start) * 1000
                )

                start = time.perf_counter()
                pandas_query(df, name)
                pandas_times.append(
                    (time.perf_counter() - start) * 1000
                )

            duckdb_ms = sum(duckdb_times) / iterations
            pandas_ms = sum(pandas_times) / iterations

            speedup = (
                pandas_ms / duckdb_ms
                if duckdb_ms > 0
                else None
            )

            records.append({
                "query": name,
                "duckdb_avg_ms": round(duckdb_ms, 3),
                "pandas_avg_ms": round(pandas_ms, 3),
                "speedup_ratio_pandas_over_duckdb": (
                    round(speedup, 2)
                    if speedup is not None
                    else None
                ),
                "faster_engine": (
                    "DuckDB"
                    if duckdb_ms < pandas_ms
                    else "Pandas"
                ),
            })

        results = pd.DataFrame(records)

        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(OUTPUT_PATH, index=False)

        print("\nFair Performance Benchmark Results")
        print(results.to_string(index=False))
        print(f"\nSaved benchmark results to: {OUTPUT_PATH}")

    finally:
        connection.close()


if __name__ == "__main__":
    benchmark()
