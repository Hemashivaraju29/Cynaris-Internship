# W6D2 Test Evidence

## API Health Test

Endpoint:
GET /health

Result:
healthy

## CIA SQL Analyst Test

Endpoint:
POST /cia/sql-analyst

Test query:
Show the total sales amount by city

Result:
Request successfully processed by the Vanna SQL analyst service.

## Natural Language Query Testing

10 natural-language SQL analyst queries were tested successfully through the CIA endpoint.

Test categories included:

1. Total sales by city
2. Total sales by region
3. Highest-selling product
4. Average sale amount by category
5. Sales by payment method
6. Sales transaction count
7. Highest-sales city
8. Total quantity by category
9. Overall sales amount
10. Top-selling products

## Verification

The generated SQL was manually checked against the sales table schema and database results.

## Status

W6D2 endpoint and query testing completed successfully.
