# Week 7 Day 4 — Natural-Language SQL Analyst API

## Objective

Build an API that converts natural-language questions into SQL queries and returns results from a MySQL sales database.

## Tools Used

- Python
- FastAPI
- Uvicorn
- Ollama with llama3.2:3b
- MySQL 8
- mysql-connector-python
- python-dotenv

## Features

- `GET /health` checks whether the API is running.
- `GET /examples` displays five example question-and-SQL pairs.
- `POST /cia/sql-analyst` generates SQL, validates it, executes it, and returns results.
- Five example SQL questions are included.
- Ten API test questions are provided in `test_api.py`.
- The database uses a read-only account.

## Setup

1. Start Ollama and confirm the llama3.2:3b model is installed.
2. Configure database credentials in the local environment or `.env` file.
3. Install dependencies:

   `python -m pip install -r "Week 07\Day 4\requirements.txt"`

4. Start the API from the repository root:

   `uvicorn api:app --app-dir "Week 07\Day 4" --reload`

5. Open `http://127.0.0.1:8000/docs` to test the endpoints.
6. Run the test script in another terminal:

   `python "Week 07\Day 4\test_api.py"`

## Example Request

Endpoint: `POST /cia/sql-analyst`

```json
{
  "question": "How many sales records are there?"
}
```

The API returns the generated SQL, row count, and query results.

## Security

This project is intended for local development. It uses a read-only database account and a basic SQL validator. The validator is not a complete security solution. Proper authentication and stronger query controls are required before public deployment.

## Testing

Run all ten API tests. Manually inspect each generated SQL query and compare important results with direct MySQL queries. Record the actual test results before submission.
