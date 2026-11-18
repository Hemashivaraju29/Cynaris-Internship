
"""DuckDB analytics for the 100K-row sales dataset."""

from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_PATH = (
    PROJECT_ROOT
    / "Week 05"
    / "Day 4"
    / "data_100k.csv"
)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"


def create_connection():
    """Create an in-memory DuckDB connection."""
    return duckdb.connect(database=":memory:")


def load_csv(connection, csv_path=DATA_PATH):
    """Load a CSV file directly into a DuckDB table."""
    csv_path = Path(csv_path)

    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    connection.execute(
        """
        CREATE OR REPLACE TABLE sales AS
        SELECT * FROM read_csv_auto(?)
        """,
        [str(csv_path)],
    )

    return connection.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]


def query_to_dataframe(sql: str, connection) -> pd.DataFrame:
    """Execute SQL and return the result as a Pandas DataFrame."""
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL query must be a non-empty string.")

    return connection.execute(sql).fetchdf()


ANALYTICAL_QUERIES = {
    "total_sales": """
        SELECT
            COUNT(*) AS total_transactions,
            SUM(quantity) AS total_quantity,
            ROUND(SUM(amount), 2) AS total_revenue,
            ROUND(AVG(amount), 2) AS average_transaction_value
        FROM sales
    """,

    "category_performance": """
        SELECT
            category,
            SUM(quantity) AS units_sold,
            ROUND(SUM(amount), 2) AS total_revenue
        FROM sales
        GROUP BY category
        ORDER BY total_revenue DESC
    """,

    "city_performance": """
        SELECT
            city,
            COUNT(*) AS transactions,
            ROUND(SUM(amount), 2) AS total_revenue
        FROM sales
        GROUP BY city
        ORDER BY total_revenue DESC
    """,

    "top_products": """
        SELECT
            product,
            SUM(quantity) AS units_sold,
            ROUND(SUM(amount), 2) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
        LIMIT 10
    """,

    "payment_analysis": """
        SELECT
            payment_method,
            COUNT(*) AS transaction_count,
            ROUND(SUM(amount), 2) AS total_revenue
        FROM sales
        GROUP BY payment_method
        ORDER BY total_revenue DESC
    """,
}


def run_analytical_queries(connection):
    """Execute five analytical SQL queries and save their results."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = {}

    for query_name, sql in ANALYTICAL_QUERIES.items():
        dataframe = query_to_dataframe(sql, connection)
        results[query_name] = dataframe

        output_path = OUTPUT_DIR / f"{query_name}.csv"
        dataframe.to_csv(output_path, index=False)

        print(f"\n{query_name.replace('_', ' ').title()}")
        print(dataframe.to_string(index=False))
        print(f"Saved: {output_path}")

    return results


def main():
    connection = create_connection()

    try:
        row_count = load_csv(connection)

        print(f"Dataset loaded successfully: {row_count:,} rows")
        print("Database: DuckDB in-memory")

        results = run_analytical_queries(connection)

        print(f"\nCompleted {len(results)} analytical SQL queries.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
