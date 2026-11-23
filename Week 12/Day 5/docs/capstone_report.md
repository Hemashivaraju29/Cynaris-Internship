# W12D5 – 3M Capstone: AI Data Analyst Platform

## 1. Introduction

The objective of this capstone is to demonstrate an AI-powered Data Analyst Platform that allows users to interact with a relational database using natural-language questions.

The application integrates Vanna AI, Ollama, FastAPI and MySQL to interpret business questions, generate SQL queries, execute them against the sales database and return understandable results.

## 2. Project Objectives

- Develop a natural-language interface for database analysis.
- Integrate a local language model using Ollama.
- Use Vanna AI for natural-language-to-SQL workflows.
- Develop REST API endpoints using FastAPI.
- Execute analytical queries against MySQL.
- Apply environment-variable-based credential management.
- Use a restricted MySQL application account.
- Demonstrate real business questions and data-quality analysis.

## 3. Technology Stack

| Technology           | Version / Purpose   |
| -------------------- | ------------------- |
| Python               | 3.11                |
| Vanna                | 2.0.2               |
| Ollama Python Client | 0.6.3               |
| Llama 3.2            | 3B parameter model  |
| FastAPI              | 0.142.2             |
| Uvicorn              | 0.54.0              |
| MySQL                | 8.0.46              |
| MySQL Connector      | 26.7.0              |
| python-dotenv        | 1.2.3               |
| PowerShell           | Application testing |

## 4. System Architecture

The capstone follows a request-and-response architecture.

### 4.1 User Interface Layer

The user submits business questions in natural language.

Examples:

- How many records are there in the sales table?
- Show the number of sales records grouped by payment method.
- How many sales records have a missing payment method?

### 4.2 API Layer – FastAPI

FastAPI exposes three endpoints:

| HTTP Method | Endpoint           | Purpose                            |
| ----------- | ------------------ | ---------------------------------- |
| GET         | `/`                | Returns application information    |
| GET         | `/health`          | Checks application health          |
| POST        | `/cia/sql-analyst` | Accepts natural-language questions |

The application runs locally at:

`http://127.0.0.1:8000`

### 4.3 AI Layer – Vanna and Ollama

Vanna coordinates the AI SQL analysis workflow.

Ollama provides the locally hosted Llama 3.2:3b language model.

The AI agent receives the schema context and user question, generates SQL and invokes the SQL execution tool.

### 4.4 Database Layer – MySQL

The application connects to:

- Database: `sales_db`
- Host: `localhost`
- Port: `3307`
- Application user: `vanna_analyst`

The application account has SELECT-only permission on the database.

## 5. Application Implementation

The main implementation is maintained in:

`Week 06/Day 1/vanna_sql_analyst.py`

The application includes:

- FastAPI application initialization.
- Request validation using Pydantic.
- Vanna AI agent configuration.
- Ollama language-model integration.
- MySQL query execution.
- Training examples.
- Application startup handling.
- Health-check endpoint.
- Natural-language SQL endpoint.

### 5.1 Application Startup

The application is started using:

```powershell
python "Week 06\Day 1\vanna_sql_analyst.py"
```

The local server runs on:

`http://127.0.0.1:8000`

### 5.2 Health Check

Request:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Observed response:

```text
status  : healthy
service : vanna-sql-analyst
```

The home endpoint also returned application information, including the database name and five training examples.

## 6. Full AI Data Analyst Demonstration

Three natural-language queries were tested successfully against the sales database.

### 6.1 Demo 1 – Total Sales Records

User question:

"How many records are there in the sales table?"

Generated SQL:

```sql
SELECT COUNT(*) FROM sales;
```

Observed result:

| Metric              | Value |
| ------------------- | ----: |
| Total sales records |    10 |

The application executed the query successfully and returned an AI-generated explanation.

### 6.2 Demo 2 – Sales by Payment Method

User question:

"Show the total number of sales records grouped by payment method."

Generated SQL:

```sql
SELECT payment_method, COUNT(*)
FROM sales
GROUP BY payment_method;
```

Observed results:

| Payment Method | Records |
| -------------- | ------: |
| UPI            |       4 |
| Credit Card    |       2 |
| Cash           |       3 |
| NULL           |       1 |
| Total          |      10 |

The results show that one sales record does not have a payment-method value.

### 6.3 Demo 3 – Missing Payment Method Detection

User question:

"How many sales records have a missing or NULL payment_method?"

Generated SQL:

```sql
SELECT COUNT(*)
FROM sales
WHERE payment_method IS NULL;
```

Observed result:

| Data Quality Metric            | Count |
| ------------------------------ | ----: |
| Missing payment method records |     1 |

This demonstrates how natural-language questions can be used for basic data-quality investigation.

## 7. Security Implementation

Security improvements completed in the existing application include:

1. Removed hardcoded MySQL credentials from the current Python application file.
2. Stored database credentials in the local `.env` file.
3. Excluded `.env` from Git.
4. Created a dedicated MySQL application user named `vanna_analyst`.
5. Granted SELECT-only permission on `sales_db`.
6. Verified the authenticated account as `vanna_analyst@localhost`.
7. Successfully executed read-only queries against the sales table.

The application is intended for local demonstration. Its fixed request context is not a substitute for real user authentication or authorization.

Historical Git credential cleanup remains a separate security follow-up.

## 8. Capstone Demonstration Results

| Verification              | Result     |
| ------------------------- | ---------- |
| Ollama service            | Available  |
| Llama 3.2:3b model        | Available  |
| MySQL service             | Reachable  |
| Python syntax compilation | Successful |
| FastAPI startup           | Successful |
| Home endpoint             | HTTP 200   |
| Health endpoint           | HTTP 200   |
| Natural-language query 1  | Successful |
| Natural-language query 2  | Successful |
| Natural-language query 3  | Successful |

All three demonstrated analytical SQL queries executed successfully.

## 9. Limitations and Future Improvements

### Current Limitations

- The API currently returns serialized Vanna component representations rather than a clean structured JSON response.
- The application uses a fixed local request context.
- The sales database used in the demonstration contains 10 records.
- Authentication and authorization for multiple users have not been implemented.
- The application is not configured for public production deployment.

### Future Improvements

- Implement proper user authentication and role-based access.
- Return structured JSON fields containing generated SQL, query results and explanations.
- Add comprehensive API tests.
- Improve error handling and request validation.
- Add monitoring and audit logging.
- Evaluate performance using larger datasets.
- Introduce production-grade deployment and security controls.

## 10. Conclusion

The W12D5 capstone successfully demonstrated an AI-powered Data Analyst Platform integrating Vanna AI, Ollama, FastAPI and MySQL.

The platform accepted natural-language questions, generated SQL statements, executed analytical queries and returned understandable responses.

Three demonstration queries were successfully executed, covering record counting, payment-method analysis and missing-value detection.

The capstone brings together AI-assisted SQL analysis, Python API development, database integration and secure credential configuration, demonstrating practical data analytics and application development skills.
