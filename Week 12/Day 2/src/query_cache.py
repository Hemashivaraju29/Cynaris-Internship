
"""Simple in-memory SQL query-result cache for DuckDB."""

import hashlib

import pandas as pd


class QueryCache:
    """Cache DuckDB query results using SQL and data version."""

    def __init__(self):
        self._cache = {}

    def _make_key(self, sql: str, data_version: str) -> str:
        raw_key = f"{data_version}:{sql.strip()}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def execute(
        self,
        sql: str,
        connection,
        data_version: str = "v1",
    ) -> pd.DataFrame:
        """Return a cached DataFrame or execute and cache the query."""

        if not isinstance(sql, str) or not sql.strip():
            raise ValueError("SQL query must be a non-empty string.")

        key = self._make_key(sql, data_version)

        if key in self._cache:
            print("Cache HIT: Returning stored query result.")
            return self._cache[key].copy()

        print("Cache MISS: Executing query in DuckDB.")

        result = connection.execute(sql).fetchdf()
        self._cache[key] = result.copy()

        return result

    def clear(self):
        """Remove all cached query results."""
        self._cache.clear()

    def cache_size(self) -> int:
        """Return number of cached queries."""
        return len(self._cache)
