
import sys
from pathlib import Path

import pandas as pd
import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from duckdb_analytics import (
    create_connection,
    load_csv,
    query_to_dataframe,
)

from query_cache import QueryCache


@pytest.fixture
def connection():
    con = create_connection()

    con.execute("""
        CREATE TABLE sales (
            sale_id INTEGER,
            customer_id INTEGER,
            product VARCHAR,
            category VARCHAR,
            quantity INTEGER,
            amount DOUBLE,
            city VARCHAR,
            payment_method VARCHAR
        )
    """)

    con.execute("""
        INSERT INTO sales VALUES
        (1, 101, 'Laptop', 'Computers', 2, 50000, 'Bengaluru', 'UPI'),
        (2, 102, 'Mouse', 'Accessories', 3, 1500, 'Mumbai', 'Card'),
        (3, 103, 'Phone', 'Electronics', 1, 30000, 'Delhi', 'Cash')
    """)

    yield con
    con.close()


def test_load_csv():
    con = create_connection()
    try:
        row_count = load_csv(
            con,
            Path(__file__).resolve().parents[3]
            / "Week 05" / "Day 4" / "data_100k.csv"
        )
        assert row_count == 100000
    finally:
        con.close()


def test_query_returns_dataframe(connection):
    result = query_to_dataframe(
        "SELECT * FROM sales",
        connection
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3


def test_query_aggregation(connection):
    result = query_to_dataframe(
        "SELECT SUM(amount) AS revenue FROM sales",
        connection
    )

    assert result.iloc[0]["revenue"] == 81500


def test_empty_query_rejected(connection):
    with pytest.raises(ValueError):
        query_to_dataframe("", connection)


def test_cache_hit_returns_same_result(connection):
    cache = QueryCache()
    sql = "SELECT city, SUM(amount) AS revenue FROM sales GROUP BY city"

    first = cache.execute(sql, connection)
    second = cache.execute(sql, connection)

    pd.testing.assert_frame_equal(first, second)
    assert cache.cache_size() == 1


def test_cache_version_creates_separate_entry(connection):
    cache = QueryCache()
    sql = "SELECT COUNT(*) AS total FROM sales"

    cache.execute(sql, connection, data_version="v1")
    cache.execute(sql, connection, data_version="v2")

    assert cache.cache_size() == 2
