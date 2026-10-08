import asyncio
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

from vanna import Agent, ToolRegistry, ToolContext
from vanna.core.user import User, UserResolver, RequestContext
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.mysql import MySQLRunner
from vanna.integrations.ollama import OllamaLlmService
from vanna.tools import RunSqlTool


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3307
MYSQL_DATABASE = "sales_db"
MYSQL_USER = "root"

# KEEP YOUR EXISTING MYSQL PASSWORD HERE
MYSQL_PASSWORD = "YOUR_EXISTING_MYSQL_PASSWORD"


# ============================================================
# OLLAMA CONFIGURATION
# ============================================================

OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "llama3.2:3b"


# ============================================================
# Vanna DATABASE RUNNER
# ============================================================

sql_runner = MySQLRunner(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
)


# ============================================================
# Vanna LLM
# ============================================================

llm = OllamaLlmService(
    model=OLLAMA_MODEL,
    host=OLLAMA_HOST,
)


# ============================================================
# Vanna MEMORY
# ============================================================

agent_memory = DemoAgentMemory(max_items=1000)


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


# ============================================================
# TOOL REGISTRY
# ============================================================

tool_registry = ToolRegistry()

tool_registry.register_local_tool(
    RunSqlTool(
        sql_runner=sql_runner,
    ),
    access_groups=["admin", "user"],
)


# ============================================================
# Vanna AGENT
# ============================================================

agent = Agent(
    llm_service=llm,
    tool_registry=tool_registry,
    user_resolver=SimpleUserResolver(),
    agent_memory=agent_memory,
)


# ============================================================
# DATABASE SCHEMA CONTEXT
# ============================================================

SCHEMA_CONTEXT = """
Database: sales_db

Table: sales

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


Table: customers

Columns:
- customer_id
- customer_name
- city


Table: orders

Columns:
- order_id
- customer_id
- product
- amount


Use the sales table for sales-analysis questions unless the
question specifically requires customers or orders.
"""


# ============================================================
# 5 CUSTOM TRAINING EXAMPLES
# ============================================================

TRAINING_EXAMPLES = [

    {
        "question": "What is the total sales amount by city?",

        "sql": """
SELECT city, SUM(amount) AS total_sales
FROM sales
GROUP BY city
ORDER BY total_sales DESC;
""",
    },

    {
        "question": "Show total sales by region.",

        "sql": """
SELECT region, SUM(amount) AS total_sales
FROM sales
GROUP BY region
ORDER BY total_sales DESC;
""",
    },

    {
        "question": "Which products have the highest total sales?",

        "sql": """
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;
""",
    },

    {
        "question": "What is the average sale amount for each category?",

        "sql": """
SELECT category, AVG(amount) AS average_sale_amount
FROM sales
GROUP BY category
ORDER BY average_sale_amount DESC;
""",
    },

    {
        "question": "How much sales were made using each payment method?",

        "sql": """
SELECT payment_method, SUM(amount) AS total_sales
FROM sales
GROUP BY payment_method
ORDER BY total_sales DESC;
""",
    },

]


# ============================================================
# TRAIN VANNA
# ============================================================

async def train_vanna() -> None:

    context = ToolContext(
        user=User(
            id="local-user",
            email="local@example.com",
            group_memberships=["admin", "user"],
        ),
        conversation_id="w6d2-training",
        request_id="w6d2-training-request",
        agent_memory=agent_memory,
    )

    for example in TRAINING_EXAMPLES:

        await agent.agent_memory.save_tool_usage(
            question=example["question"],
            tool_name="run_sql",
            args={
                "sql": example["sql"].strip(),
            },
            context=context,
            success=True,
        )

    print("Vanna training completed.")
    print(f"Training examples added: {len(TRAINING_EXAMPLES)}")


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="W6D2 Vanna SQL Analyst",
    description="Vanna custom SQL training for domain data",
    version="1.0.0",
)


# ============================================================
# REQUEST MODEL
# ============================================================

class SQLAnalystRequest(BaseModel):

    question: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
async def root() -> dict[str, str]:

    return {
        "service": "w6d2-vanna-sql-analyst",
        "status": "running",
    }


# ============================================================
# HEALTH ENDPOINT
# ============================================================

@app.get("/health")
async def health() -> dict[str, str]:

    return {
        "status": "healthy",
        "service": "w6d2-vanna-sql-analyst",
    }


# ============================================================
# CIA SQL ANALYST ENDPOINT
# ============================================================

@app.post("/cia/sql-analyst")
async def sql_analyst(
    request: SQLAnalystRequest,
) -> dict[str, Any]:

    question = request.question

    messages = [

        {
            "role": "system",
            "content": (
                "You are a SQL analyst working with the "
                "sales_db database. "
                "Generate correct MySQL SQL queries for "
                "the user's question. "
                "Return SQL that can be executed directly. "
                + SCHEMA_CONTEXT
            ),
        },

        {
            "role": "user",
            "content": question,
        },

    ]

    results = []

    async for component in agent.send_message(
        request_context=RequestContext(
            user=User(
                id="local-user",
                email="local@example.com",
                group_memberships=["admin", "user"],
            ),
            conversation_id="w6d2-api",
            request_id="w6d2-api-request",
        ),
        message=messages,
    ):

        results.append(str(component))

    return {
        "question": question,
        "results": results,
    }


# ============================================================
# STARTUP EVENT
# ============================================================

@app.on_event("startup")
async def startup_event() -> None:

    await train_vanna()


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "vanna_training:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )