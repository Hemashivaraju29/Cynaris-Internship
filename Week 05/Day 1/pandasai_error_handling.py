import logging
import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

# --------------------------------------------------
# Error logging configuration
# --------------------------------------------------

log_file = "Week 05/Day 1/pandasai_errors.log"

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

csv_path = "Week 05/Day 1/india_districts_census_2011.csv"

df = pai.read_csv(csv_path)

columns = [
    "District name",
    "State Name",
    "Population"
]

df = pai.DataFrame(df[columns])

# --------------------------------------------------
# Configure Ollama
# --------------------------------------------------

llm = LiteLLM(
    model="ollama_chat/llama3.2:3b",
    api_base="http://localhost:11434"
)

pai.config.set({
    "llm": llm
})

print("PandasAI error-handling test")
print("Dataset rows:", len(df))

# --------------------------------------------------
# Test queries
# --------------------------------------------------

questions = [
    "What is the average population?",
    "Which 10 districts have the highest population?",
    "What is the total population?"
]

for question in questions:

    print("\nQuestion:", question)

    try:
        result = df.chat(question)

        print("Result:")
        print(result)

    except KeyboardInterrupt:
        print("Query interrupted by user.")
        logging.exception("PandasAI query interrupted: %s", question)

    except Exception as e:
        print("Query failed:", type(e).__name__)
        print(e)

        logging.exception(
            "PandasAI query failed: %s",
            question
        )

print("\nError-handling test completed.")
print("Error log:", log_file)