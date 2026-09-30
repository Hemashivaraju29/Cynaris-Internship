import pandasai as pai
from pandasai_litellm.litellm import LiteLLM

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

csv_path = "Week 05/Day 1/india_districts_census_2011.csv"

df = pai.read_csv(csv_path)

# Keep only the columns required for this test
columns = [
    "District name",
    "State Name",
    "Population"
]

df = pai.DataFrame(df[columns])

print("Dataset loaded successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# --------------------------------------------------
# 2. Configure Ollama through LiteLLM
# --------------------------------------------------

llm = LiteLLM(
    model="ollama_chat/llama3.2:3b",
    api_base="http://localhost:11434"
)

pai.config.set({
    "llm": llm
})

print("PandasAI + Ollama configured successfully")

# --------------------------------------------------
# 3. Natural-language query
# --------------------------------------------------

question = "How many districts are in the dataset?"

print("\nQuestion:", question)
print("\nRunning PandasAI query...")

# --------------------------------------------------
# 4. Error handling
# --------------------------------------------------

try:
    result = df.chat(question)

    print("\nRaw PandasAI result:")
    print(result)

    # Handle PandasAI structured result
    if isinstance(result, dict):
        print("\nAnswer:")
        print(result.get("value", result))
    else:
        print("\nAnswer:")
        print(result)

except KeyboardInterrupt:
    print("\nQuery stopped by user.")

except Exception as e:
    print("\nQuery failed:", type(e).__name__)
    print(e)