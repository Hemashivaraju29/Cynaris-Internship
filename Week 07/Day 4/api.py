
import os
import re
from decimal import Decimal
from pathlib import Path
from datetime import date, datetime
from typing import Any

import mysql.connector
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

# Load environment files without displaying their contents.
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parents[1] / ".env")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

DB_CONFIG = {
    "host": os.getenv("CIA_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("CIA_DB_PORT", "3307")),
    "database": os.getenv("CIA_DB_NAME", "sales_db"),
    "user": os.getenv("CIA_DB_USER", "cia_reader"),
    "password": os.getenv("CIA_DB_PASSWORD", ""),
    "connection_timeout": 10,
}

ALLOWED_TABLES = {"sales", "customers", "orders"}
MAX_ROWS = 500

app = FastAPI(
    title="CIA SQL Analyst API",
    description="Generate and execute read-only SQL using a local Ollama model.",
    version="1.0.0",
)


# --------------------------------------------------
# Example question-and-SQL pairs
# --------------------------------------------------

EXAMPLES = [
    {
        "question": "How many sales records are there?",
        "sql": "SELECT COUNT(*) AS total_sales FROM sales",
    },
    {
        "question": "What are the total sales by city?",
        "sql": (
            "SELECT city, SUM(amount) AS total_amount "
            "FROM sales GROUP BY city ORDER BY total_amount DESC"
        ),
    },
    {
        "question": "Show the top 5 products by sales amount.",
        "sql": (
            "SELECT product, SUM(amount) AS total_amount "
            "FROM sales GROUP BY product "
            "ORDER BY total_amount DESC LIMIT 5"
        ),
    },
    {
        "question": "What is the average sale amount by category?",
        "sql": (
            "SELECT category, AVG(amount) AS average_amount "
            "FROM sales GROUP BY category"
        ),
    },
    {
        "question": "How many sales transactions are there per payment method?",
        "sql": (
            "SELECT payment_method, COUNT(*) AS transaction_count "
            "FROM sales GROUP BY payment_method"
        ),
    },
    {
        "question": "What is the highest sale amount?",
        "sql": (
            "SELECT MAX(amount) AS highest_sale_amount FROM sales"
        ),
    },
]


# --------------------------------------------------
# Request model
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="A natural-language question about the sales database.",
    )


# --------------------------------------------------
# SQL generation using local Ollama
# --------------------------------------------------

def generate_sql(question: str, correction: str | None = None) -> str:
    """Generate one SQL query using the local Ollama model."""

    examples_text = "\n".join(
        f"Question: {example['question']}\nSQL: {example['sql']}"
        for example in EXAMPLES
    )

    correction_text = ""
    if correction:
        correction_text = (
            "\nYour previous SQL was rejected for this reason: "
            f"{correction}\nGenerate a corrected query that follows every rule."
        )

    prompt = f"""
You are a careful MySQL SQL analyst.

Available tables and columns:

sales:
sale_id, customer_name, product, category, quantity, amount,
city, payment_method, region, sale_date

customers:
customer_id, customer_name, city

orders:
order_id, customer_id, product, amount

Examples:
{examples_text}

Rules:
1. Return exactly one MySQL SELECT query and nothing else.
2. Every query MUST contain FROM and reference at least one approved table.
3. For a highest sale amount question, use:
   SELECT MAX(amount) AS highest_sale_amount FROM sales
4. For a lowest sale amount question, use:
   SELECT MIN(amount) AS lowest_sale_amount FROM sales
5. Use only the tables and columns listed above.
6. Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE,
   REPLACE, GRANT, REVOKE, or any other data-changing statement.
7. Do not use multiple statements, SQL comments, or system tables.
8. Add a LIMIT for queries returning multiple rows.
9. Do not invent columns or tables.
10. Aggregate questions must use the appropriate COUNT, SUM, AVG, MAX,
    or MIN function.
11. Do not wrap the SQL in Markdown code fences.
12. Return only the SQL query.

Question: {question}
{correction_text}
""".strip()

    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0},
            },
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()
        sql = data.get("message", {}).get("content", "").strip()

    except requests.RequestException as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Could not contact Ollama. Ensure Ollama is running "
                "and the configured model is available."
            ),
        ) from exc

    # Remove Markdown fences if the model adds them.
    sql = re.sub(r"^\s*```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```\s*$", "", sql)
    sql = sql.strip()

    if not sql:
        raise HTTPException(
            status_code=502,
            detail="The AI model did not generate a SQL query.",
        )

    return sql


# --------------------------------------------------
# SQL validation
# --------------------------------------------------

def validate_sql(sql: str) -> str:
    """
    Validate SQL before execution.

    Only a single SELECT statement using approved tables is accepted.
    """

    if not sql or not sql.strip():
        raise ValueError("The SQL query is empty.")

    query = sql.strip()

    # Do not allow comments.
    if "--" in query or "/*" in query or "*/" in query or "#" in query:
        raise ValueError("SQL comments are not allowed.")

    # Remove one optional trailing semicolon, then reject internal semicolons.
    query = query.rstrip()
    if query.endswith(";"):
        query = query[:-1].rstrip()

    if ";" in query:
        raise ValueError("Only one SQL statement is allowed.")

    # Require a SELECT statement.
    if not re.match(r"^SELECT\b", query, flags=re.IGNORECASE):
        raise ValueError("Only SELECT queries are allowed.")

    # Block dangerous statements and operations.
    forbidden_pattern = (
        r"\b(?:INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE|"
        r"GRANT|REVOKE|EXEC|EXECUTE|CALL|LOAD_FILE|INTO|OUTFILE|DUMPFILE|"
        r"SET|USE|HANDLER|LOCK|UNLOCK)\b"
    )

    if re.search(forbidden_pattern, query, flags=re.IGNORECASE):
        raise ValueError("The query contains a prohibited SQL operation.")

    # Block access to system schemas.
    if re.search(
        r"\b(?:information_schema|performance_schema|mysql|sys)\s*\.",
        query,
        flags=re.IGNORECASE,
    ):
        raise ValueError("System database access is not allowed.")

    # Require FROM and at least one approved table.
    from_join_tables = re.findall(
        r"\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b",
        query,
        flags=re.IGNORECASE,
    )

    if not from_join_tables:
        raise ValueError(
            "The query must include FROM and read from an approved table."
        )

    # Reject references to tables that are not approved.
    invalid_tables = {
        table.lower()
        for table in from_join_tables
        if table.lower() not in ALLOWED_TABLES
    }

    if invalid_tables:
        raise ValueError(
            "The query references unapproved table(s): "
            + ", ".join(sorted(invalid_tables))
        )

    # Limit the size of result sets.
    if not re.search(r"\bLIMIT\s+\d+\b", query, flags=re.IGNORECASE):
        query = f"{query} LIMIT {MAX_ROWS}"

    limit_match = re.search(
        r"\bLIMIT\s+(\d+)\b", query, flags=re.IGNORECASE
    )
    if limit_match and int(limit_match.group(1)) > MAX_ROWS:
        query = re.sub(
            r"\bLIMIT\s+\d+\b",
            f"LIMIT {MAX_ROWS}",
            query,
            count=1,
            flags=re.IGNORECASE,
        )

    return query


# --------------------------------------------------
# Database execution
# --------------------------------------------------

def make_json_safe(value: Any) -> Any:
    """Convert MySQL result values to JSON-compatible values."""

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    return value


def execute_sql(sql: str) -> list[dict[str, Any]]:
    """Execute a validated query and return rows as dictionaries."""

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql)

        rows = cursor.fetchall()

        return [
            {key: make_json_safe(value) for key, value in row.items()}
            for row in rows
        ]

    except mysql.connector.Error as exc:
        raise HTTPException(
            status_code=500,
            detail="The database could not execute the generated query.",
        ) from exc

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


# --------------------------------------------------
# API endpoints
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "CIA SQL Analyst API is running.",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    """Check API, Ollama, and database availability."""

    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        response.raise_for_status()
        ollama_status = "connected"
    except requests.RequestException:
        ollama_status = "unavailable"

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        connection.close()
        database_status = "connected"
    except mysql.connector.Error:
        database_status = "unavailable"

    return {
        "api": "running",
        "ollama": ollama_status,
        "database": database_status,
        "model": OLLAMA_MODEL,
    }


@app.get("/examples")
def get_examples():
    """Return example natural-language questions."""

    return {"examples": EXAMPLES}


@app.post("/cia/sql-analyst")
def sql_analyst(request: QuestionRequest):
    """Generate, validate, and execute a read-only SQL query."""

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Please provide a non-empty question.",
        )

    # Retry once if the model generates invalid SQL.
    last_error = None

    for attempt in range(2):
        generated_sql = generate_sql(
            question,
            correction=str(last_error) if last_error else None,
        )

        try:
            validated_sql = validate_sql(generated_sql)
            results = execute_sql(validated_sql)

            return {
                "question": question,
                "sql": validated_sql,
                "row_count": len(results),
                "results": results,
            }

        except ValueError as exc:
            last_error = exc

            if attempt == 1:
                raise HTTPException(
                    status_code=400,
                    detail=f"Generated SQL was rejected: {exc}",
                ) from exc

    raise HTTPException(
        status_code=400,
        detail="Unable to generate a valid SQL query.",
    )
