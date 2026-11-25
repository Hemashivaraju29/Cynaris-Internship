import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()



def calculate_insights(df):
    """Calculate five meaningful insights from a sales dataset."""
    if df.empty:
        raise ValueError("The dataset is empty.")

    insights = []

    # Insight 1: Dataset overview
    insights.append(
        f"The dataset contains {len(df)} rows and {len(df.columns)} columns."
    )

    # Insight 2–4: Sales statistics
    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if "Sales" in df.columns and pd.api.types.is_numeric_dtype(df["Sales"]):
        sales_column = "Sales"
    elif numeric_columns:
        sales_column = numeric_columns[0]
    else:
        raise ValueError("The dataset must contain a numeric column.")

    sales = df[sales_column].dropna()

    if sales.empty:
        raise ValueError(f"The column '{sales_column}' has no numeric values.")

    insights.append(
        f"Average {sales_column} is {sales.mean():,.2f}."
    )
    insights.append(
        f"Highest {sales_column} is {sales.max():,.2f}."
    )
    insights.append(
        f"Lowest {sales_column} is {sales.min():,.2f}."
    )

    # Insight 5: Region with the highest total sales
    if (
        "Region" in df.columns
        and "Sales" in df.columns
        and pd.api.types.is_numeric_dtype(df["Sales"])
    ):
        region_sales = df.dropna(subset=["Region", "Sales"]).groupby(
            "Region"
        )["Sales"].sum()

        if not region_sales.empty:
            top_region = region_sales.idxmax()
            insights.append(
                f"The {top_region} region has the highest total sales "
                f"at {region_sales.max():,.2f}."
            )
        else:
            insights.append("Regional sales data is unavailable.")
    else:
        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if categorical_columns:
            category = categorical_columns[0]
            insights.append(
                f"The dataset contains {df[category].nunique()} unique "
                f"values in the {category} column."
            )
        else:
            insights.append("No categorical data is available for further analysis.")

    return insights



def generate_summary(insights: list[str]) -> str:
    """Generate a business-focused executive summary using Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to the project .env file."
        )

    client = Groq(api_key=api_key)
    prompt = "\n".join(
        f"{i + 1}. {item}" for i, item in enumerate(insights)
    )

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior data analyst. Write an executive "
                    "summary of approximately 200 words for business leaders. "
                    "Explain the main findings, business impact, limitations, "
                    "and practical next steps. Use only the supplied facts. "
                    "Do not invent figures or claim unsupported causation."
                ),
            },
            {
                "role": "user",
                "content": "Summarize these five data insights:\n" + prompt,
            },
        ],
        temperature=0.3,
        max_tokens=350,
    )

    summary = response.choices[0].message.content
    if not summary:
        raise RuntimeError("Groq returned an empty summary.")
    return summary.strip()
