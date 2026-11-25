
import os
import re
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from vanna import Agent, ToolRegistry, ToolContext
from vanna.core.user import User, UserResolver, RequestContext
from vanna.core.system_prompt.default import DefaultSystemPromptBuilder
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.mysql import MySQLRunner
from vanna.integrations.ollama import OllamaLlmService
from vanna.tools import RunSqlTool


# ============================================================
# 1. CONFIGURATION
# ============================================================

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3307"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "sales_db")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

if not MYSQL_PASSWORD:
    raise RuntimeError(
        "MYSQL_PASSWORD is not set. Set it in PowerShell before starting the API."
    )


# ============================================================
# 2. DATABASE SCHEMA
# ============================================================

SCHEMA_CONTEXT = """
Database: sales_db
SQL dialect: MySQL

Use only the following tables and columns.

Table: sales
Columns:
sale_id, customer_name, product, category, quantity,
amount, city, payment_method, region, sale_date

Table: customers
Columns:
customer_id, customer_name, city

Table: orders
Columns:
order_id, customer_id, product, amount

Rules:
- Use sales.amount for sales revenue.
- Use the sales table for sales-analysis questions.
- The sales table already contains city and region.
- Do not join customers merely to obtain city.
- Join customers and orders using customer_id when needed.
- Never invent tables or columns.
- Only read data; never modify database objects or records.

Example:
SELECT city, SUM(amount) AS total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC;
"""


# ============================================================
# 3. FIVE TRAINING EXAMPLES
# ============================================================

TRAINING_EXAMPLES = [
    {
        "question": "What is the total sales amount by city?",
        "sql": """
SELECT city, SUM(amount) AS total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC
""",
    },
    {
        "question": "Show total sales by region.",
        "sql": """
SELECT region, SUM(amount) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC
""",
    },
    {
        "question": "Which products have the highest total sales?",
        "sql": """
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC
""",
    },
    {
        "question": "What is the average sale amount for each category?",
        "sql": """
SELECT category, AVG(amount) AS average_sale_amount
FROM sales
GROUP BY category
ORDER BY average_sale_amount DESC
""",
    },
    {
        "question": "Show total sales by payment method.",
        "sql": """
SELECT payment_method, SUM(amount) AS total_sales
FROM sales
GROUP BY payment_method
ORDER BY total_sales DESC
""",
    },
]


# ============================================================
# 4. READ-ONLY SQL VALIDATION
# ============================================================

def validate_read_only_sql(sql: str) -> None:
    """Reject empty, multiple, or obviously unsafe SQL statements."""

    statement = sql.strip()

    if not statement:
        raise ValueError("SQL query cannot be empty.")

    # Allow one optional trailing semicolon.
    statement = statement.rstrip(";").strip()

    # Reject multiple statements.
    if ";" in statement:
        raise ValueError("Only one SQL statement is allowed.")

    # Accept only SELECT or WITH at the beginning.
    if not re.match(r"^(SELECT|WITH)\b", statement, re.IGNORECASE):
        raise ValueError("Only SELECT or WITH queries are allowed.")

    # Block common data-changing or administrative keywords.
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|"
        r"REPLACE|GRANT|REVOKE|CALL|EXECUTE|LOAD|OUTFILE|DUMPFILE)\b",
        re.IGNORECASE,
    )

    if forbidden.search(statement):
        raise ValueError("The SQL contains a forbidden operation.")


class SafeSqlRunner:
    """Validate a query before passing it to MySQLRunner."""

    def __init__(self, runner: MySQLRunner):
        self.runner = runner

    async def run_sql(self, args: Any, context: Any):
        validate_read_only_sql(args.sql)
        return await self.runner.run_sql(args, context)


# ============================================================
# 5. DATABASE RUNNER
# ============================================================

sql_runner = MySQLRunner(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
)

safe_sql_runner = SafeSqlRunner(sql_runner)


# ============================================================
# 6. OLLAMA LANGUAGE MODEL
# ============================================================

llm = OllamaLlmService(
    model=OLLAMA_MODEL,
    host=OLLAMA_HOST,
)


# ============================================================
# 7. VANNA MEMORY AND USER RESOLVER
# ============================================================

agent_memory = DemoAgentMemory(max_items=1000)


class SimpleUserResolver(UserResolver):
    async def resolve_user(
        self,
        request_context: RequestContext,
    ) -> User:
        return User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        )


# ============================================================
# 8. REGISTER SQL TOOL
# ============================================================

tool_registry = ToolRegistry()

tool_registry.register_local_tool(
    RunSqlTool(
        sql_runner=safe_sql_runner,
        custom_tool_description=(
            "Execute one read-only SELECT or WITH query against the "
            "sales_db MySQL database. Use only the documented schema. "
            "Never modify tables or records."
        ),
    ),
    access_groups=["admin", "user"],
)


# ============================================================
# 9. CREATE VANNA AGENT
# ============================================================

agent = Agent(
    llm_service=llm,
    tool_registry=tool_registry,
    user_resolver=SimpleUserResolver(),
    agent_memory=agent_memory,
    system_prompt_builder=DefaultSystemPromptBuilder(
        base_prompt=f"""
You are a careful MySQL data analyst.

DATABASE SCHEMA:
{SCHEMA_CONTEXT}

STRICT RULES:
1. Use only tables and columns in the schema.
2. Use the sales table for sales-analysis questions.
3. For total sales by city, generate:
   SELECT city, SUM(amount) AS total_sales
   FROM sales
   GROUP BY city
   ORDER BY total_sales DESC
4. The sales table already has city. Do not join customers
   to obtain city for this query.
5. Use sales.amount for revenue.
6. Never invent tables or columns.
7. Generate read-only SELECT queries only.
8. Never create, alter, insert, update, or delete data.
9. If a question cannot be answered from the schema,
   explain the limitation instead of inventing SQL.
"""
    ),
)


# ============================================================
# 10. TRAIN THE AGENT
# ============================================================

async def train_vanna() -> None:
    context = ToolContext(
        user=User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        ),
        conversation_id="w6d4-training",
        request_id="w6d4-training-request",
        agent_memory=agent_memory,
    )

    for example in TRAINING_EXAMPLES:
        await agent.agent_memory.save_tool_usage(
            question=example["question"],
            tool_name="run_sql",
            args={"sql": example["sql"].strip()},
            context=context,
            success=True,
        )

    print(
        f"Vanna training completed: "
        f"{len(TRAINING_EXAMPLES)} examples registered."
    )


# ============================================================
# 11. FASTAPI APPLICATION
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    await train_vanna()
    yield


app = FastAPI(
    title="W6D4 Vanna SQL Analyst",
    description="Natural-language SQL analyst for sales_db.",
    version="1.0.0",
    lifespan=lifespan,
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


# ============================================================
# 12. HEALTH ENDPOINT
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "w6d4-vanna-sql-analyst",
    }


# ============================================================
# 13. CIA SQL ANALYST ENDPOINT
# ============================================================

@app.post("/cia/sql-analyst")
async def sql_analyst(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    request_context = RequestContext(
        user=User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        ),
        conversation_id="w6d4-api",
        request_id="w6d4-api-request",
    )

    components = []

    try:
        async for component in agent.send_message(
            request_context=request_context,
            message=(
                f"{SCHEMA_CONTEXT}\n\n"
                f"User question: {question}"
            ),
        ):
            components.append(str(component))

        response_text = "\n".join(components)

        failed = (
            "Tool failed:" in response_text
            or "Error executing query:" in response_text
            or "status='error'" in response_text
        )

        return {
            "question": question,
            "status": "error" if failed else "completed",
            "results": components,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        # Do not return credentials or detailed connection settings.
        raise HTTPException(
            status_code=500,
            detail=f"SQL analyst request failed: {type(exc).__name__}",
        ) from exc


# ============================================================
# 14. RUN SERVER
# ============================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
