
import json
import urllib.error
import urllib.request

API_URL = "http://127.0.0.1:8000/cia/sql-analyst"

QUESTIONS = [
    "How many sales records are there?",
    "What is the total sales amount by city?",
    "What are the top five products by total sales amount?",
    "What is the average sale amount by category?",
    "How many sales records are there for each payment method?",
    "Which five cities have the most sales records?",
    "What is the total quantity sold for each product?",
    "What is the highest sale amount?",
    "How many sales records are there for each region?",
    "Show the ten most recent sales with their date, product, and amount.",
]


def main():
    passed = 0

    for index, question in enumerate(QUESTIONS, start=1):
        print(f"\n[{index}/10] {question}")

        payload = json.dumps({"question": question}).encode("utf-8")
        request = urllib.request.Request(
            API_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))

            sql = result.get("sql", "")
            rows = result.get("results", [])

            print("Generated SQL:", sql)
            print("Returned rows:", result.get("row_count", len(rows)))
            print("Sample results:", rows[:2])
            print("HTTP test: PASS")
            passed += 1

        except urllib.error.HTTPError as exc:
            print("HTTP test: FAIL", exc.code)
            print(exc.read().decode("utf-8", errors="replace"))

        except Exception as exc:
            print("Test failed:", type(exc).__name__, str(exc))

    print(f"\nSuccessful API calls: {passed}/10")
    print("Manually verify the generated SQL and results.")


if __name__ == "__main__":
    main()
