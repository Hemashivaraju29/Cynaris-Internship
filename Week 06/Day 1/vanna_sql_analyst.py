import asyncio
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.tool import ToolContext
from vanna.core.user import UserResolver, User, RequestContext
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.mysql import MySQLRunner
from vanna.integrations.ollama import OllamaLlmService
from vanna.tools import RunSqlTool


# ============================================================
# CONFIGURATION
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3307
MYSQL_DATABASE = "sales_db"
MYSQL_USER = "root"

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b"


# ============================================================
# DATABASE
# ============================================================

sql_runner = MySQLRunner(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password="Chinnu@29",
)


db_tool = RunSqlTool(
    sql_runner=sql_runner,
)


# ============================================================
# OLLAMA
# ============================================================

llm = OllamaLlmService(
    model=OLLAMA_MODEL,
    host=OLLAMA_HOST,
)


# ============================================================
# MEMORY
# ============================================================

agent_memory = DemoAgentMemory(
    max_items=1000
)


# ============================================================
# USER RESOLVER
# ============================================================

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


user_resolver = SimpleUserResolver()


# ============================================================
# TOOLS
# ============================================================

tools = ToolRegistry()

tools.register_local_tool(
    db_tool,
    access_groups=["admin", "user"],
)


# ============================================================
# AGENT
# ============================================================

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    agent_memory=agent_memory,
)


# ============================================================
# DATABASE SCHEMA CONTEXT
# ============================================================

SCHEMA_CONTEXT = """
You are a SQL analyst working with a MySQL database named sales_db.

Available tables:

1. sales
Columns:
- sale_id
- customer_name
- product
- category
- quantity
- amount
- city
- payment_method
- region
- sale_date

2. customers
Columns:
- customer_id
- customer_name
- city

3. orders
Columns:
- order_id
- customer_id
- product
- amount

For sales-related questions, use the sales table unless the question
clearly requires customers or orders.

Use valid MySQL SQL.

Do not invent table names or column names.

When the user asks for total sales, use SUM(amount).

When the user asks for average sale amount, use AVG(amount).

When the user asks for number of transactions, use COUNT(*).

When the user asks for total quantity, use SUM(quantity).
"""


# ============================================================
# 5 TRAINING EXAMPLES
# ============================================================

TRAINING_EXAMPLES = [

    (
        "Show the total sales amount by city",
        """
        SELECT city,
               SUM(amount) AS total_sales
        FROM sales
        GROUP BY city
        ORDER BY total_sales DESC;
        """,
    ),

    (
        "What is the total sales amount?",
        """
        SELECT SUM(amount) AS total_sales
        FROM sales;
        """,
    ),

    (
        "Show the top 5 products by total sales amount",
        """
        SELECT product,
               SUM(amount) AS total_sales
        FROM sales
        GROUP BY product
        ORDER BY total_sales DESC
        LIMIT 5;
        """,
    ),

    (
        "Show the total quantity sold for each category",
        """
        SELECT category,
               SUM(quantity) AS total_quantity_sold
        FROM sales
        GROUP BY category;
        """,
    ),

    (
        "What is the average sale amount?",
        """
        SELECT AVG(amount) AS average_sale_amount
        FROM sales;
        """,
    ),
]


# ============================================================
# SEED TRAINING DATA
# ============================================================

async def seed_training_examples() -> None:

    context = ToolContext(
    user=User(
        id="local-user",
        email="local@example.com",
        group_memberships=["admin", "user"],
    ),
    conversation_id="training-conversation",
    request_id="training-request",
    agent_memory=agent_memory,
)

    for question, sql in TRAINING_EXAMPLES:

        await agent.agent_memory.save_tool_usage(
            question=question,
            tool_name="run_sql",
            args={
                "sql": sql.strip(),
            },
            context=context,
            success=True,
        )


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="Cynaris Vanna SQL Analyst",
    version="1.0.0",
)


# ============================================================
# REQUEST MODEL
# ============================================================

class SQLAnalystRequest(BaseModel):
    question: str


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event() -> None:

    await seed_training_examples()


# ============================================================
# HOME
# ============================================================

@app.get("/")
async def home() -> dict[str, Any]:

    return {
        "project": "Cynaris Week 6 Day 1",
        "feature": "Vanna NL to SQL Analyst",
        "database": MYSQL_DATABASE,
        "training_examples": len(TRAINING_EXAMPLES),
        "endpoint": "/cia/sql-analyst",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health() -> dict[str, str]:

    return {
        "status": "healthy",
        "service": "vanna-sql-analyst",
    }


# ============================================================
# NL TO SQL ENDPOINT
# ============================================================

@app.post("/cia/sql-analyst")
async def sql_analyst(
    request: SQLAnalystRequest,
) -> dict[str, Any]:

    request_context = RequestContext(
        user=User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        )
    )

    message = f"""
{SCHEMA_CONTEXT}

User question:

{request.question}

Generate the correct SQL query and execute it against the database.

Return the SQL and the result clearly.
"""

    response_components = []

    async for component in agent.send_message(
        request_context=request_context,
        message=message,
    ):
        response_components.append(str(component))

    return {
        "question": request.question,
        "response": response_components,
    }


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )