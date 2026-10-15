# Week 6 Day 1 - Vanna SQL Analyst

## Objective

Set up Vanna to convert natural language questions into SQL queries and execute them on the MySQL sales database.

## Completed Tasks

- Configured Vanna 2.0.2 with MySQL.
- Connected Vanna to the `sales_db` database.
- Configured Ollama with the `llama3.2:3b` model.
- Added 5 training examples for natural-language SQL generation.
- Tested 10 natural-language SQL queries.
- Manually verified the generated SQL and database results.
- Created a FastAPI endpoint:
  `POST /cia/sql-analyst`
- Tested the endpoint end-to-end using PowerShell.
- Verified that the generated SQL executes successfully against the real database.

## End-to-End Verification

### Test Question

Show the total sales amount by city.

### Generated SQL

```sql
SELECT city, SUM(amount)
FROM sales
GROUP BY city;
```
