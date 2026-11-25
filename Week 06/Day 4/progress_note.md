# Week 6 Day 4 — Progress Note

## Objective

Build and test a natural-language SQL analyst using Vanna, MySQL, and Ollama, exposed through a FastAPI endpoint.

## Work Completed

- Configured the Vanna agent to work with the `sales_db` MySQL database.
- Added database schema context for the `sales`, `customers`, and `orders` tables.
- Registered five example question-and-SQL pairs in agent memory.
- Added the `POST /cia/sql-analyst` endpoint.
- Added a `/health` endpoint to check API availability.
- Added validation to restrict generated SQL to read-only `SELECT` or `WITH` statements.
- Tested the API using natural-language questions.

## Testing

- Tested 10 natural-language SQL questions.
- Verified the generated SQL for sales totals, product totals, category averages, payment methods, record count, and quantity sold.
- Manually checked the Bengaluru and Delhi city filter in MySQL Workbench.
- Investigated a missing payment-method value in the source data.

## Issues Identified

- The model initially generated a city query without the requested city filter.
- One sales record has a missing or blank payment method.
- Generated SQL and query results must be checked rather than relying only on the API status.

## Status

The API is running and responding to requests. Most tested queries produced appropriate SQL. The city-filter issue and missing payment-method value are documented for follow-up.

## Next Steps

- Improve the prompt or training examples for filtered queries.
- Review the missing payment-method record.
- Commit the W6D4 implementation and test documentation.
- Push the feature branch and update the pull request.
