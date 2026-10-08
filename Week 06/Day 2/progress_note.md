# Week 6 Day 2 - Vanna Training

## Objective
Train Vanna with custom SQL patterns for the sales domain and expose the SQL analyst through a CIA endpoint.

## Work Completed

- Configured Vanna with MySQL database sales_db.
- Connected Vanna to the MySQL database running on port 3307.
- Connected Vanna to the Ollama llama3.2:3b model.
- Added 5 custom SQL training examples.
- Added SQL patterns for:
  - Total sales by city
  - Total sales by region
  - Total sales by product
  - Average sale amount by category
  - Sales by payment method
- Created FastAPI service for the SQL analyst.
- Added POST /cia/sql-analyst endpoint.
- Added /health endpoint.
- Tested the endpoint successfully using PowerShell.
- Tested 10 natural-language SQL analyst queries.
- Verified the generated SQL queries against the sales database.

## Training Examples

1. Total sales amount by city
2. Total sales by region
3. Highest-selling products
4. Average sale amount by category
5. Sales by payment method

## API Test

Endpoint:

POST /cia/sql-analyst

Example request:

Show the total sales amount by city

Result:

The request was successfully processed by the Vanna SQL analyst service.

## Server

Local API:

http://127.0.0.1:8000

Health endpoint:

GET /health

Status:

healthy

## Technology Used

- Python
- Vanna
- FastAPI
- MySQL
- Ollama
- PowerShell

## Status

W6D2 implementation and functional testing completed.
