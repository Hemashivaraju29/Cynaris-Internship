
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

Table: customers
Columns: customer_id, customer_name, city

Table: orders
Columns: order_id, customer_id, product, amount

Table: sales
Columns: sale_id, customer_name, product, category, quantity,
amount, city, payment_method, region, sale_date

Rules:
- Use customers and orders for customer-order questions.
- Join customers and orders using customer_id.
- Use sales for sales-analysis questions.
- Use sales.amount for sales revenue and orders.amount for order value.
- Do not invent tables or columns.
- Use only read-only SELECT queries.
"""


# ============================================================
# 3. FIVE TRAINING EXAMPLES
# ============================================================

TRAINING_EXAMPLES = [
    {
        "question": "How many customers are in the database?",
        "sql": """
SELECT COUNT(*) AS customer_count
FROM customers
""",
    },
    {
        "question": "Show all customers and their cities.",
        "sql": """
SELECT customer_id, customer_name, city
FROM customers
ORDER BY customer_id
""",
    },
    {
        "question": "Show each customer with their orders.",
        "sql": """
SELECT c.customer_id, c.customer_name,
       o.order_id, o.product, o.amount
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_id
""",
    },
    {
        "question": "What is the total order value for each customer?",
        "sql": """
SELECT c.customer_id, c.customer_name,
       COALESCE(SUM(o.amount), 0) AS total_order_value
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_order_value DESC
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
]


# ============================================================
# 4. READ-ONLY SQL VALIDATION
# ============================================================

def validate_read_only_sql(sql: str) -> None:
    statement = sql.strip()

    if not statement:
        raise ValueError("SQL query cannot be empty.")

    statement = statement.rstrip(";").strip()

    if ";" in statement:
        raise ValueError("Only one SQL statement is allowed.")

    if not re.match(r"^(SELECT|WITH)\b", statement, re.IGNORECASE):
        raise ValueError("Only SELECT or WITH queries are allowed.")

    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|"
        r"REPLACE|GRANT|REVOKE|CALL|EXECUTE|LOAD|OUTFILE|DUMPFILE)\b",
        re.IGNORECASE,
    )

    if forbidden.search(statement):
        raise ValueError("The SQL contains a forbidden operation.")


class SafeSqlRunner:
    def __init__(self, runner: MySQLRunner):
        self.runner = runner

    async def run_sql(self, args: Any, context: Any):
        validate_read_only_sql(args.sql)
        return await self.runner.run_sql(args, context)


# ============================================================
# 5. DATABASE RUNNER AND LANGUAGE MODEL
# ============================================================

sql_runner = MySQLRunner(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
)

safe_sql_runner = SafeSqlRunner(sql_runner)

llm = OllamaLlmService(
    model=OLLAMA_MODEL,
    host=OLLAMA_HOST,
)


# ============================================================
# 6. VANNA MEMORY AND USER RESOLVER
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
# 7. REGISTER SQL TOOL
# ============================================================

tool_registry = ToolRegistry()

tool_registry.register_local_tool(
    RunSqlTool(
        sql_runner=safe_sql_runner,
        custom_tool_description=(
            "Execute one read-only SELECT or WITH query against sales_db. "
            "Use the documented customers, orders, and sales schema only."
        ),
    ),
    access_groups=["admin", "user"],
)


# ============================================================
# 8. CREATE VANNA AGENT
# ============================================================

agent = Agent(
    llm_service=llm,
    tool_registry=tool_registry,
    user_resolver=SimpleUserResolver(),
    agent_memory=agent_memory,
    system_prompt_builder=DefaultSystemPromptBuilder(
        base_prompt=f"""
You are a careful MySQL CRM and sales data analyst.

DATABASE SCHEMA:
{SCHEMA_CONTEXT}

Rules:
1. Use only the listed tables and columns.
2. Join customers and orders using customer_id.
3. Use LEFT JOIN when customers without orders must be included.
4. Use sales for sales-analysis questions.
5. Do not invent data or schema.
6. Only generate read-only SQL.
7. If the question cannot be answered from this schema, explain why.
"""
    ),
)


# ============================================================
# 9. TRAIN THE AGENT ON FIVE QUESTION-SQL PAIRS
# ============================================================

async def train_vanna() -> None:
    context = ToolContext(
        user=User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        ),
        conversation_id="w6d5-training",
        request_id="w6d5-training-request",
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
        f"W6D5 training completed: "
        f"{len(TRAINING_EXAMPLES)} examples registered."
    )


# ============================================================
# 10. FASTAPI APPLICATION
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    await train_vanna()
    yield


app = FastAPI(
    title="W6D5 NL SQL CRM Dashboard",
    description="Natural-language SQL analyst for CRM and sales data.",
    version="1.0.0",
    lifespan=lifespan,
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@app.get("/")
async def root():
    return {
        "service": "W6D5 NL SQL CRM Dashboard",
        "endpoint": "POST /cia/sql-analyst",
        "training_examples": len(TRAINING_EXAMPLES),
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "w6d5-nl-sql-crm-dashboard",
    }


# ============================================================
# 11. REQUIRED CIA ENDPOINT
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
        conversation_id="w6d5-api",
        request_id="w6d5-api-request",
    )

    components = []

    try:
        async for component in agent.send_message(
            request_context=request_context,
            message=f"{SCHEMA_CONTEXT}\n\nUser question: {question}",
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
        raise HTTPException(
            status_code=500,
            detail=f"SQL analyst request failed: {type(exc).__name__}",
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
