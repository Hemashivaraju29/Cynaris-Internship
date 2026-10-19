
"""
Cynaris Internship - Week 7 Day 4
Read-only SQL Analyst using Vanna and local Ollama.
"""

import json
import os
import uuid
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from vanna.core import Agent, AgentConfig, ToolRegistry
from vanna.core.tool import Tool, ToolContext, ToolResult
from vanna.core.user import User, RequestContext
from vanna.core.system_prompt import DefaultSystemPromptBuilder
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.integrations.mysql import MySQLRunner
from vanna.integrations.mysql.sql_runner import RunSqlToolArgs
from vanna.integrations.ollama import OllamaLlmService


# ---------------------------------------------------------
# Paths and environment
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parents[1]

load_dotenv(ROOT_DIR / ".env")

EXAMPLES_PATH = BASE_DIR / "training_examples.json"


def require_env(name: str) -> str:
    """Read a required environment variable without displaying its value."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing environment variable: {name}. "
            "Check your project's .env configuration."
        )
    return value


def load_examples() -> list[dict[str, Any]]:
    """Load the example question and SQL pairs."""
    if not EXAMPLES_PATH.exists():
        raise FileNotFoundError(
            f"Training examples file not found: {EXAMPLES_PATH}"
        )

    with EXAMPLES_PATH.open("r", encoding="utf-8") as file:
        examples = json.load(file)

    if not isinstance(examples, list):
        raise ValueError(
            "training_examples.json must contain a JSON list."
        )

    return examples


EXAMPLES = load_examples()


# ---------------------------------------------------------
# Database schema and prompt
# ---------------------------------------------------------

SCHEMA_DESCRIPTION = """
Database: sales_db

Approved tables and columns:

sales:
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

customers:
- customer_id
- customer_name
- city

orders:
- order_id
- customer_id
- product
- amount

Use only these tables and columns.
Generate MySQL-compatible SQL.
"""

EXAMPLE_TEXT = "\n\n".join(
    f"Question: {item.get('question', '')}\n"
    f"SQL: {item.get('sql', '')}"
    for item in EXAMPLES
)

SYSTEM_INSTRUCTIONS = f"""
You are a data analyst working with the sales_db database.

Answer questions using the available database when appropriate.
Use MySQL syntax and only the approved tables and columns.

DATABASE SCHEMA:
{SCHEMA_DESCRIPTION}

EXAMPLES:
{EXAMPLE_TEXT}

SAFETY RULES:
- Execute only read-only SELECT queries.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE,
  TRUNCATE, GRANT, REVOKE, or administrative statements.
- Never access unapproved tables or system schemas.
- Never invent table or column names.
- Do not claim a query succeeded unless its results are available.
- If a question cannot be answered from this schema, explain why.
"""


# ---------------------------------------------------------
# Read-only SQL tool
# ---------------------------------------------------------

class SQLQueryArgs(BaseModel):
    sql: str = Field(
        ...,
        description="One read-only SQL SELECT statement.",
    )


class ReadOnlySQLTool(Tool[SQLQueryArgs]):
    """Execute SQL only after it passes the project validator."""

    def __init__(self, runner: MySQLRunner):
        self.runner = runner

    @property
    def name(self) -> str:
        return "run_readonly_sales_sql"

    @property
    def description(self) -> str:
        return (
            "Execute one validated, read-only SQL query against "
            "the approved sales_db tables."
        )

    @property
    def parameters(self) -> type[SQLQueryArgs]:
        return SQLQueryArgs

    @property
    def access_groups(self) -> list[str]:
        return ["user", "admin"]

    async def execute(
        self,
        params: SQLQueryArgs,
        context: ToolContext,
    ) -> ToolResult:
        # Import from the current project directory.
        from sql_validator import validate_sql

        safe_sql = validate_sql(params.sql)

        # MySQLRunner is asynchronous in the installed Vanna version.
        result = await self.runner.run_sql(
            RunSqlToolArgs(sql=safe_sql),
            context,
        )

        return result


# ---------------------------------------------------------
# Local user resolver
# ---------------------------------------------------------

class LocalUserResolver:
    async def resolve_user(
        self,
        request_context: RequestContext,
    ) -> User:
        return User(
            id="local-sql-analyst",
            group_memberships=["user"],
        )


# ---------------------------------------------------------
# Agent creation
# ---------------------------------------------------------

def build_agent() -> Agent:
    """Create a Vanna agent using Ollama, not OpenAI."""

    runner = MySQLRunner(
        host=os.getenv("CIA_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("CIA_DB_PORT", "3307")),
        database=os.getenv("CIA_DB_NAME", "sales_db"),
        user=require_env("CIA_DB_USER"),
        password=require_env("CIA_DB_PASSWORD"),
    )

    registry = ToolRegistry()
    registry.register_local_tool(ReadOnlySQLTool(runner))

    ollama_host = os.getenv(
        "CIA_OLLAMA_HOST",
        os.getenv("OLLAMA_HOST", "http://localhost:11434"),
    )

    llm = OllamaLlmService(
        model=os.getenv("CIA_OLLAMA_MODEL", "llama3.2:3b"),
        host=ollama_host,
        timeout=240.0,
        num_ctx=8192,
        temperature=0.1,
    )

    return Agent(
        llm_service=llm,
        tool_registry=registry,
        user_resolver=LocalUserResolver(),
        memory=DemoAgentMemory(max_items=1000),
        system_prompt_builder=DefaultSystemPromptBuilder(
            base_prompt=SYSTEM_INSTRUCTIONS
        ),
        config=AgentConfig(
            max_tool_iterations=5,
            stream_responses=True,
            auto_save_conversations=False,
            temperature=0.1,
        ),
    )


# ---------------------------------------------------------
# Ask the analyst
# ---------------------------------------------------------

async def ask_sql_analyst(question: str) -> dict[str, str]:
    """Ask a natural-language question and collect the agent response."""

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if len(question) > 500:
        raise ValueError(
            "Question must be 500 characters or fewer."
        )

    agent = build_agent()
    request_context = RequestContext()
    conversation_id = str(uuid.uuid4())

    answer_parts: list[str] = []

    async for event in agent.send_message(
        request_context,
        question,
        conversation_id=conversation_id,
    ):
        if isinstance(event, str):
            answer_parts.append(event)
            continue

        rich = getattr(event, "rich", None)
        if rich is not None:
            content = getattr(rich, "content", None)
            if content:
                answer_parts.append(str(content))

        simple = getattr(event, "simple", None)
        if simple is not None:
            text = getattr(simple, "text", None)
            if text:
                answer_parts.append(str(text))

    answer = "\n".join(
        part for part in answer_parts if part
    ).strip()

    if not answer:
        answer = (
            "No readable response was returned. Check that Ollama "
            "is running and inspect the application logs."
        )

    return {
        "question": question,
        "answer": answer,
        "conversation_id": conversation_id,
    }
