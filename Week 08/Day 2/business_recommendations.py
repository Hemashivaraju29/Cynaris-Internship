import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def calculate_insights(df: pd.DataFrame) -> list[str]:
    """Calculate exactly five useful insights from a CSV dataset."""
    if df.empty:
        raise ValueError("The dataset is empty.")

    insights = [
        f"The dataset contains {len(df)} rows and {len(df.columns)} columns."
    ]

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if "Sales" in df.columns and pd.api.types.is_numeric_dtype(df["Sales"]):
        metric = "Sales"
    elif numeric_columns:
        metric = numeric_columns[0]
    else:
        raise ValueError("The dataset must contain a numeric column.")

    values = df[metric].dropna()

    if values.empty:
        raise ValueError(f"The '{metric}' column has no numeric values.")

    insights.extend([
        f"Average {metric} is {values.mean():,.2f}.",
        f"Highest {metric} is {values.max():,.2f}.",
        f"Lowest {metric} is {values.min():,.2f}.",
    ])

    if (
        "Region" in df.columns
        and "Sales" in df.columns
        and pd.api.types.is_numeric_dtype(df["Sales"])
    ):
        regional_sales = (
            df.dropna(subset=["Region", "Sales"])
            .groupby("Region")["Sales"]
            .sum()
        )

        if not regional_sales.empty:
            region = regional_sales.idxmax()
            insights.append(
                f"The {region} region has the highest total sales "
                f"at {regional_sales.max():,.2f}."
            )
        else:
            insights.append("Regional sales data is unavailable.")
    else:
        categorical = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if categorical:
            column = categorical[0]
            insights.append(
                f"The '{column}' column contains "
                f"{df[column].nunique()} unique values."
            )
        else:
            insights.append(
                "No categorical data is available for further analysis."
            )

    return insights


def generate_business_narrative(insights: list[str]) -> str:
    """Use Groq to turn five data insights into business recommendations."""
    if len(insights) != 5:
        raise ValueError("Exactly five insights are required.")

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to your project .env file."
        )

    client = Groq(api_key=api_key)
    numbered_insights = "\n".join(
        f"{index}. {insight}"
        for index, insight in enumerate(insights, start=1)
    )

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior business intelligence analyst. "
                    "Use only the supplied data insights. Do not invent "
                    "figures, facts, or unsupported causal explanations. "
                    "Write an executive summary of approximately 200 words "
                    "explaining the major findings, business implications, "
                    "limitations, and opportunities. Then add a section "
                    "titled 'Business Recommendations' containing 3 to 5 "
                    "specific, practical, prioritized actions. Explain the "
                    "reason for each action and suggest a measurable KPI "
                    "where appropriate. Clearly identify assumptions."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Analyze these five data insights and produce the "
                    "executive summary followed by actionable business "
                    "recommendations:\n" + numbered_insights
                ),
            },
        ],
        temperature=0.3,
        max_tokens=900,
    )

    narrative = response.choices[0].message.content
    if not narrative or not narrative.strip():
        raise RuntimeError("Groq returned an empty business narrative.")

    return narrative.strip()
