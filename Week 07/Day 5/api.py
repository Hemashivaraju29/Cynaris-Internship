
import io
import uuid
import json
from typing import Any

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


app = FastAPI(
    title="CIA Data Analyst Mode",
    description="Upload a CSV and analyze it with validated Pandas operations.",
    version="1.0.0",
)

# Allow the local frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_ROWS = 100_000
MAX_COLUMNS = 100

# Temporary in-memory storage. Sessions clear when the server restarts.
SESSIONS: dict[str, pd.DataFrame] = {}


class QueryRequest(BaseModel):
    session_id: str
    question: str = Field(min_length=1, max_length=1000)


@app.get("/")
def root():
    return {
        "message": "CIA Data Analyst Mode API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/cia/upload")
async def upload_csv(file: UploadFile = File(...)) -> dict[str, Any]:
    """Validate a CSV and store it in temporary session memory."""

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a file with a .csv extension.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)
    await file.close()

    if not content:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 10 MB.",
        )

    try:
        dataframe = pd.read_csv(io.BytesIO(content))
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail="Could not parse this file as a valid CSV.",
        ) from exc

    if dataframe.empty:
        raise HTTPException(
            status_code=400,
            detail="The CSV must contain at least one data row.",
        )

    if len(dataframe) > MAX_ROWS or len(dataframe.columns) > MAX_COLUMNS:
        raise HTTPException(
            status_code=400,
            detail="CSV exceeds the row or column limit.",
        )

    dataframe.columns = [str(column).strip() for column in dataframe.columns]

    if dataframe.columns.duplicated().any():
        raise HTTPException(
            status_code=400,
            detail="CSV column names must be unique.",
        )

    if any(not column for column in dataframe.columns):
        raise HTTPException(
            status_code=400,
            detail="CSV column names cannot be blank.",
        )

    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = dataframe

    preview_df = dataframe.head(5).astype(object).where(
        pd.notna(dataframe.head(5)), None
    )

    return {
        "session_id": session_id,
        "filename": file.filename,
        "rows": int(len(dataframe)),
        "columns": list(dataframe.columns),
        "preview": preview_df.to_dict(orient="records"),
        "message": "CSV uploaded and parsed successfully.",
    }


def find_column(dataframe: pd.DataFrame, keywords: list[str]) -> str | None:
    """Find a column by matching its name against known keywords."""

    for column in dataframe.columns:
        name = str(column).strip().lower()
        if any(keyword in name for keyword in keywords):
            return column

    return None


def numeric_column(dataframe: pd.DataFrame) -> str | None:
    """Prefer a sales/revenue column, otherwise find a numeric column."""

    preferred = find_column(
        dataframe,
        ["sales", "revenue", "amount", "total", "profit"],
    )

    if preferred is not None and pd.api.types.is_numeric_dtype(dataframe[preferred]):
        return preferred

    numeric = dataframe.select_dtypes(include="number").columns.tolist()
    return numeric[0] if numeric else None


def safe_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    """Convert a DataFrame to JSON-safe records."""

    cleaned = dataframe.astype(object).where(pd.notna(dataframe), None)
    return json.loads(cleaned.to_json(orient="records", date_format="iso"))


def make_chart(
    grouped: pd.DataFrame,
    label_column: str,
    value_column: str,
) -> dict[str, Any]:
    """Build Chart.js data and Plotly-compatible JSON."""

    labels = grouped[label_column].astype(str).tolist()
    values = [float(value) for value in grouped[value_column].tolist()]

    chartjs = {
        "type": "bar",
        "labels": labels,
        "datasets": [
            {
                "label": str(value_column),
                "data": values,
            }
        ],
    }

    plotly_json = {
        "data": [
            {
                "type": "bar",
                "x": labels,
                "y": values,
                "name": str(value_column),
            }
        ],
        "layout": {
            "title": f"{value_column} by {label_column}",
            "xaxis": {"title": str(label_column)},
            "yaxis": {"title": str(value_column)},
        },
    }

    return {
        "chartjs": chartjs,
        "plotly_json": plotly_json,
    }


@app.post("/cia/query")
def query_csv(request: QueryRequest) -> dict[str, Any]:
    """Answer supported questions using validated Pandas operations."""

    dataframe = SESSIONS.get(request.session_id)

    if dataframe is None:
        raise HTTPException(
            status_code=404,
            detail="Session not found. Please upload the CSV again.",
        )

    question = request.question.strip()
    q = question.lower()

    if not q:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Total or average of a numeric column.
    value_column = numeric_column(dataframe)

    asks_average = any(word in q for word in ["average", "mean", "avg"])
    asks_total = any(
        word in q
        for word in ["total", "sum", "overall", "how much", "sales amount"]
    )

    if value_column and (asks_average or asks_total):
        series = pd.to_numeric(dataframe[value_column], errors="coerce").dropna()

        if series.empty:
            raise HTTPException(
                status_code=400,
                detail=f"Column '{value_column}' contains no usable numbers.",
            )

        if asks_average:
            answer = round(float(series.mean()), 2)
            operation = "mean"
        else:
            answer = round(float(series.sum()), 2)
            operation = "sum"

        return {
            "answer": answer,
            "question": question,
            "method": "validated_pandas_aggregation",
            "operation": operation,
            "column": str(value_column),
            "chart": None,
        }

    # Group by a categorical column and sum a numeric column.
    group_column = find_column(
        dataframe,
        ["category", "region", "product", "company", "department", "city"],
    )

    asks_chart = any(
        word in q for word in ["chart", "plot", "graph", "visual", "show"]
    )
    asks_grouping = any(
        word in q for word in ["by category", "by region", "by product", "by company",
                               "by department", "by city", "group"]
    )

    if value_column and group_column and (asks_chart or asks_grouping):
        working = dataframe[[group_column, value_column]].copy()
        working[value_column] = pd.to_numeric(
            working[value_column], errors="coerce"
        )
        working = working.dropna(subset=[group_column, value_column])

        grouped = (
            working.groupby(group_column, as_index=False)[value_column]
            .sum()
            .sort_values(value_column, ascending=False)
        )

        return {
            "answer": (
                f"{value_column} grouped by {group_column}. "
                f"Found {len(grouped)} groups."
            ),
            "question": question,
            "method": "validated_pandas_groupby",
            "table": safe_records(grouped),
            "chart": make_chart(grouped, group_column, value_column),
        }

    # Basic row count query.
    if any(term in q for term in ["how many rows", "row count", "number of rows",
                                   "count records", "how many records"]):
        return {
            "answer": int(len(dataframe)),
            "question": question,
            "method": "validated_pandas_count",
            "chart": None,
        }

    # Explain which columns are available instead of guessing.
    return {
        "answer": (
            "I could not match this question to a supported operation. "
            "Try asking for total sales, average sales, number of rows, "
            "or a chart of sales by category or region."
        ),
        "question": question,
        "method": "help_fallback",
        "available_columns": list(dataframe.columns),
        "chart": None,
    }
