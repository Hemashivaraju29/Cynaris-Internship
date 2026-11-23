# W12D5 – AI Data Analyst Platform: Full Demo Script

## 1. Introduction

Good morning everyone.

Today, I am demonstrating my 3M internship capstone project: AI Data Analyst Platform.

The project allows users to ask business questions in natural language and retrieve results from a MySQL sales database using an AI-powered SQL analysis workflow.

The platform integrates Vanna AI, Ollama, Llama 3.2, FastAPI and MySQL.

## 2. Technology Overview

- Python 3.11 – Application development.
- Vanna AI – Natural-language-to-SQL workflow.
- Ollama – Local language model service.
- Llama 3.2:3b – AI model.
- FastAPI – REST API framework.
- Uvicorn – Application server.
- MySQL 8.0.46 – Database.
- python-dotenv – Environment configuration.

## 3. Application Startup

Start the application:

```powershell
python "Week 06\Day 1\vanna_sql_analyst.py"
```

Expected local URL:

http://127.0.0.1:8000

Keep the server running during the demonstration.

## 4. Demonstrate the API Endpoints

### Home endpoint

```powershell
Invoke-RestMethod http://127.0.0.1:8000/
```

Explain the project name, database and available endpoint.

### Health endpoint

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Expected status: healthy.

## 5. Demonstrate Natural-Language SQL Analysis

Use a second PowerShell terminal.

### Demo 1: Count sales records

Question: How many records are there in the sales table?

```powershell
$body = @{
    question = "How many records are there in the sales table?"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/cia/sql-analyst" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json -Depth 10
```

Generated SQL:

```sql
SELECT COUNT(*) FROM sales;
```

Verified result: 10 records.

### Demo 2: Group sales by payment method

Question: Show the total number of sales records grouped by payment method.

```powershell
$body = @{
    question = "Show the total number of sales records grouped by payment method."
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/cia/sql-analyst" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json -Depth 10
```

Verified results:

| Payment Method | Count |
| -------------- | ----: |
| UPI            |     4 |
| Credit Card    |     2 |
| Cash           |     3 |
| NULL           |     1 |

### Demo 3: Identify missing payment methods

Question: How many sales records have a missing or NULL payment_method?

```powershell
$body = @{
    question = "How many sales records have a missing or NULL payment_method?"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/cia/sql-analyst" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response | ConvertTo-Json -Depth 10
```

Generated SQL:

```sql
SELECT COUNT(*)
FROM sales
WHERE payment_method IS NULL;
```

Verified result: 1 record.

## 6. Explain the Application Workflow

1. The user submits a natural-language question.
2. FastAPI receives the request.
3. Vanna processes the question with schema context.
4. Ollama provides local language-model inference.
5. The agent generates a SQL query.
6. The SQL execution tool runs the query against MySQL.
7. The application returns query results and an AI-generated explanation.

## 7. Demonstrate Database Security

Explain the security improvements:

- Application credentials are stored in the local .env file.
- The .env file is excluded from Git.
- The application uses the dedicated vanna_analyst database account.
- The account has SELECT-only permission on sales_db.
- The application runs locally on 127.0.0.1.

Never display passwords or API keys.

## 8. Demonstration Results

| Test                           | Result               |
| ------------------------------ | -------------------- |
| Home endpoint                  | Successful           |
| Health endpoint                | HTTP 200             |
| Sales record count             | 10                   |
| Payment-method grouping        | 4 result groups      |
| Missing payment-method count   | 1                    |
| Natural-language SQL execution | 3 successful queries |

## 9. Known Limitations

- The current demonstration database contains 10 sales records.
- API responses contain serialized Vanna component representations rather than a clean structured JSON format.
- The API uses a fixed local request context and does not provide full user authentication.
- The application is intended for local demonstration, not public production deployment.

## 10. Conclusion

The capstone successfully demonstrated an AI-powered SQL analysis workflow that converts natural-language questions into executable SQL queries and returns results from a MySQL database.

The project combines AI integration, Python API development, local model execution, relational database connectivity and secure credential management.

Thank you.
