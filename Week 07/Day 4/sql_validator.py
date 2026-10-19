
import re

ALLOWED_TABLES = {"sales", "customers", "orders"}
MAX_LIMIT = 500


class SQLValidationError(ValueError):
    """Raised when a generated SQL query is unsafe."""


def validate_sql(sql: str) -> str:
    """Allow a single read-only SELECT against approved sales_db tables."""
    if not isinstance(sql, str) or not sql.strip():
        raise SQLValidationError("SQL query is empty.")

    query = sql.strip()

    # Reject multiple statements, comments, and suspicious constructs.
    if ";" in query.rstrip(";"):
        raise SQLValidationError("Multiple SQL statements are not allowed.")

    if re.search(r"--|/\*|\*/|#", query):
        raise SQLValidationError("SQL comments are not allowed.")

    if not re.match(r"(?is)^SELECT\b", query):
        raise SQLValidationError("Only SELECT queries are allowed.")

    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|"
        r"REPLACE|GRANT|REVOKE|CALL|EXECUTE|INTO|OUTFILE|"
        r"DUMPFILE|LOAD_FILE|SLEEP|BENCHMARK|FOR\s+UPDATE|"
        r"LOCK\s+IN\s+SHARE\s+MODE)\b",
        re.IGNORECASE,
    )
    if forbidden.search(query):
        raise SQLValidationError("Query contains a forbidden SQL operation.")

    # Restrict table references to the tables in sales_db.
    if re.search(r"\b(?:information_schema|mysql|performance_schema|sys)\s*\.",
                 query, re.IGNORECASE):
        raise SQLValidationError("System databases are not permitted.")

    if re.search(r"\b(?:FROM|JOIN)\s+[a-zA-Z0-9_]+\s*\.", query,
                 re.IGNORECASE):
        raise SQLValidationError("Qualified table names are not permitted.")

    referenced_tables = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)",
        query,
        re.IGNORECASE,
    )
    if not referenced_tables:
        raise SQLValidationError("Query must reference an approved table.")

    for table in referenced_tables:
        if table.lower() not in ALLOWED_TABLES:
            raise SQLValidationError(f"Table '{table}' is not permitted.")

    query = query.rstrip().rstrip(";").strip()

    # Apply a maximum result count if the query has no LIMIT.
    if not re.search(r"\bLIMIT\s+\d+\b", query, re.IGNORECASE):
        query += f" LIMIT {MAX_LIMIT}"
    else:
        match = re.search(r"\bLIMIT\s+(\d+)\b", query, re.IGNORECASE)
        if match and int(match.group(1)) > MAX_LIMIT:
            query = query[:match.start()] + f"LIMIT {MAX_LIMIT}"

    return query
