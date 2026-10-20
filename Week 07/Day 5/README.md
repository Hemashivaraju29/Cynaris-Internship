# Week 7 Day 5 — CIA Data Analyst Mode

## Overview

A web-based data analysis application that allows users to upload CSV files, ask questions about their data, and view charts.

## Technologies Used

- Python 3.11
- FastAPI
- Pandas
- HTML, CSS, JavaScript
- Chart.js
- Plotly-compatible chart JSON
- Uvicorn

## Features

- CSV upload and validation
- Temporary session-based dataset storage
- Data analysis through validated Pandas operations
- Total and average calculations
- Grouped sales analysis by category and region
- Chart.js visualization data
- API documentation through Swagger UI

## How to Run

Activate the virtual environment and run:

```powershell
uvicorn "Week 07.Day 5.api:app" --reload
```

Open the API documentation at http://127.0.0.1:8000/docs.

Open `index.html` with VS Code Live Server to use the frontend.

## Test Questions

1. What is the total sales?
2. What is the average sales?
3. Show a chart of sales by category.
4. Show a chart of sales by region.
5. How many rows are in the dataset?

## Notes

Uploaded datasets are stored in temporary memory and are cleared when the API restarts. The current API uses validated Pandas operations for supported queries.
