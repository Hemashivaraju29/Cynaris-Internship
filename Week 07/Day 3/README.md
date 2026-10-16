# Week 7 Day 3 — Interactive Sales Dashboard

## Objective

Build an interactive sales dashboard using Python, Pandas, NumPy, Plotly, and Dash.

## Features

- Monthly Sales line chart
- Monthly Units Sold bar chart
- Category Sales Distribution pie chart
- Region filter
- Category filter
- Date-range filter
- Filtered sales data table with sorting, filtering, and pagination

## Dataset

`Sales_Data.csv` contains sample sales records with the following columns:

- Date
- Region
- Category
- Sales
- Units Sold

## Files

- `Sales_Data.csv` — sample sales dataset
- `dashboard.py` — dashboard implementation
- `README.md` — project documentation

## How to Run

Install the required libraries:

```bash
python -m pip install pandas numpy plotly dash
```

Run the dashboard from the repository root:

```bash
python "Week 07/Day 3/dashboard.py"
```

Open `http://127.0.0.1:8050/` in a browser.

## Verification

The dashboard was launched locally, and its charts and filters were tested manually.

## Note

This implementation uses Python Dash and Plotly. Integration with ECharts in the CIA frontend is not included in this version.
