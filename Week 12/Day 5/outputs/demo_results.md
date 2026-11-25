# W12D5 – AI Data Analyst Platform Demo Results

## 1. Environment Verification

| Component            | Verified Result   |
| -------------------- | ----------------- |
| Python               | 3.11.9            |
| Vanna                | 2.0.2             |
| Ollama Python Client | 0.6.3             |
| FastAPI              | 0.142.2           |
| Uvicorn              | 0.54.0            |
| MySQL Server         | 8.0.46            |
| LLM Model            | llama3.2:3b       |
| Ollama Port          | 11434 – Reachable |
| MySQL Port           | 3307 – Reachable  |

## 2. Application Verification

| Test                      | Result     |
| ------------------------- | ---------- |
| Python syntax compilation | Successful |
| FastAPI startup           | Successful |
| Home endpoint             | HTTP 200   |
| Health endpoint           | HTTP 200   |
| Database configuration    | Verified   |
| Training examples         | 5          |

## 3. Natural-Language Query Results

### Query 1: Total Sales Records

Question: How many records are there in the sales table?

Generated SQL:

```sql
SELECT COUNT(*) FROM sales;
```

Result: 10 records.

Status: Successful.

### Query 2: Sales by Payment Method

Question: Show the total number of sales records grouped by payment method.

Generated SQL:

```sql
SELECT payment_method, COUNT(*)
FROM sales
GROUP BY payment_method;
```

| Payment Method | Record Count |
| -------------- | -----------: |
| UPI            |            4 |
| Credit Card    |            2 |
| Cash           |            3 |
| NULL           |            1 |
| Total          |           10 |

Status: Successful.

### Query 3: Missing Payment Method

Question: How many sales records have a missing or NULL payment_method?

Generated SQL:

```sql
SELECT COUNT(*)
FROM sales
WHERE payment_method IS NULL;
```

Result: 1 record.

Status: Successful.

## 4. Consolidated Results

| Metric                         | Result |
| ------------------------------ | -----: |
| Total demo questions           |      3 |
| Successful SQL executions      |      3 |
| Failed SQL executions          |      0 |
| Sales records examined         |     10 |
| Missing payment-method records |      1 |

## 5. Observations

- Natural-language questions were converted into SQL queries.
- SQL queries executed successfully against MySQL.
- Query results were returned through the Vanna AI workflow.
- One missing payment-method value was identified.
- The results demonstrate basic AI-assisted business analysis and data-quality investigation.

## 6. Known Limitations

- The application currently returns serialized Vanna component representations in its API response.
- The API uses a fixed local request context.
- The demonstration database contains only 10 sales records.
- Production authentication and authorization are not implemented.

## 7. Conclusion

The AI Data Analyst Platform successfully demonstrated natural-language-to-SQL analysis using Vanna AI, Ollama, FastAPI and MySQL.

All three demonstration questions executed successfully and returned the expected results.

These results establish a working local capstone demonstration.
