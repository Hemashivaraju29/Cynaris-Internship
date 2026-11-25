
import logging
from pathlib import Path

import pandas as pd
from pandasai import SmartDataframe
from pandasai_litellm.litellm import LiteLLM

# File paths
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "nifty500_combined_eda.csv"
LOG_PATH = BASE_DIR / "pandasai_errors.log"
RESULTS_PATH = BASE_DIR / "query_results.txt"

# Configure error logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Ten natural-language questions
QUESTIONS = [
    "How many rows are in this dataset?",
    "How many unique companies are in the dataset?",
    "What is the average closing price?",
    "What is the highest closing price?",
    "What is the lowest closing price?",
    "What is the total trading volume?",
    "Which company has the most records?",
    "What is the average closing price for each company?",
    "Which date has the highest trading volume?",
    "Are there any missing values in each column?",
]


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, parse_dates=["Date"])
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns.")

    llm = LiteLLM(
        model="ollama/llama3.2:3b",
        api_base="http://localhost:11434",
    )

    analyst = SmartDataframe(
        df,
        config={
            "llm": llm,
            "save_logs": True,
            "verbose": False,
        },
    )

    successful = 0
    failed = 0

    with RESULTS_PATH.open("w", encoding="utf-8") as results:
        for number, question in enumerate(QUESTIONS, start=1):
            print(f"\nQuery {number}/10: {question}")

            try:
                answer = analyst.chat(question)
                output = str(answer)

                print("PandasAI answer:", output)
                results.write(f"Query {number}: {question}\n")
                results.write(f"PandasAI answer: {output}\n\n")
                successful += 1

            except Exception as exc:
                logging.exception("PandasAI query failed: %s", question)
                error_message = f"{type(exc).__name__}: {exc}"

                print("Query failed:", error_message)
                results.write(f"Query {number}: {question}\n")
                results.write(f"ERROR: {error_message}\n\n")
                failed += 1

    print("\n--- Summary ---")
    print(f"Successful queries: {successful}")
    print(f"Failed queries: {failed}")
    print(f"Results saved to: {RESULTS_PATH}")
    print(f"Error log: {LOG_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("Application startup failed")
        raise
