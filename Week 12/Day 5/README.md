# Week 12 Day 5 – 3M Capstone: AI Data Analyst Platform

## 1. Project Overview

This capstone demonstrates an AI-powered Data Analyst Platform that allows users to ask business questions in natural language and retrieve analytical results from a MySQL database.

The application integrates Vanna AI, Ollama, FastAPI and MySQL to generate and execute SQL queries.

## 2. Technology Stack

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python 3.11   | Application development            |
| Vanna 2.0.2   | AI-powered SQL analysis            |
| Ollama 0.6.3  | Local language model integration   |
| Llama 3.2:3b  | Natural-language processing        |
| FastAPI       | REST API development               |
| Uvicorn       | Application server                 |
| MySQL 8.0.46  | Relational database                |
| python-dotenv | Environment-variable configuration |

## 3. Application Architecture

```text
User Question
     |
     v
FastAPI Application
     |
     v
Vanna AI Agent
     |
     v
Ollama – Llama 3.2:3b
     |
     v
SQL Generation and Execution
     |
     v
MySQL – sales_db
     |
     v
Query Results and AI Explanation
```

## 4. API Endpoints

| Method | Endpoint           | Purpose                       |
| ------ | ------------------ | ----------------------------- |
| GET    | `/`                | Application information       |
| GET    | `/health`          | Health verification           |
| POST   | `/cia/sql-analyst` | Natural-language SQL analysis |

## 5. Demonstration Results

Three natural-language questions were successfully tested.

### Demo 1: Total sales records

Question: How many records are there in the sales table?

Generated SQL:

```sql
SELECT COUNT(*) FROM sales;
```

Result: 10 records.

### Demo 2: Sales grouped by payment method

Question: Show the total number of sales records grouped by payment method.

Results:

| Payment Method | Records |
| -------------- | ------: |
| UPI            |       4 |
| Credit Card    |       2 |
| Cash           |       3 |
| NULL           |       1 |
| Total          |      10 |

### Demo 3: Missing payment method

Question: How many sales records have a missing or NULL payment_method?

Generated SQL:

```sql
SELECT COUNT(*)
FROM sales
WHERE payment_method IS NULL;
```

Result: 1 record.

## 6. Security Configuration

- Database credentials are loaded from the local `.env` file.
- The `.env` file is excluded from Git.
- The application uses a dedicated MySQL account named `vanna_analyst`.
- The account has SELECT-only access to `sales_db`.
- The application runs locally on `127.0.0.1:8000`.
- No database write operations are required for the demonstration.

The application currently uses a fixed local request context. It is not an authenticated multi-user production service.

## 7. Verified Components

- Ollama model availability verified.
- MySQL port connectivity verified.
- FastAPI application startup successful.
- Home endpoint returned HTTP 200.
- Health endpoint returned HTTP 200.
- Three AI-generated SQL queries executed successfully.

## 8. Known Limitations

- API responses currently contain serialized Vanna component representations rather than clean structured SQL and result fields.
- The API request context is fixed for local demonstration.
- The current demonstration database contains only 10 sales records.
- The application is intended for local demonstration, not public production deployment.
- Authentication, authorization and production monitoring require further implementation.

## 9. Project Structure

```text
Week 12/
└── Day 5/
    ├── README.md
    ├── docs/
    │   └── capstone_report.md
    ├── demo/
    │   └── full_demo_script.md
    └── outputs/
        └── demo_results.md
```

## 10. Conclusion

The capstone successfully demonstrated a natural-language interface for querying sales data using Vanna AI, Ollama, FastAPI and MySQL.

Three analytical questions were executed successfully, including a data-quality query identifying one missing payment-method value.

The demonstration brings together AI-assisted SQL analysis, database connectivity, environment-based credential management and analytical reporting.
