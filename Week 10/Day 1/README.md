# Week 10 - Day 1: Time Series Analysis

## Objective

Analyze historical sales data to understand trends, check stationarity, and forecast future sales using the ARIMA model.

## Dataset

- **Source:** `Week 07/Day 3/Sales_Data.csv`
- **Records:** 24
- **Columns:** Date, Region, Category, Sales, Units Sold
- **Time period:** January 2026 to September 2026

## Tasks Performed

1. Loaded and cleaned the sales dataset.
2. Converted transaction dates into monthly sales data.
3. Aggregated sales values month by month.
4. Analyzed the monthly sales trend using a line chart.
5. Performed the Augmented Dickey-Fuller (ADF) test to check stationarity.
6. Applied an ARIMA(1,1,1) model.
7. Forecast sales for the next three months.
8. Saved the results as CSV files and charts.

## Key Results

- Highest monthly sales: June 2026 (43,000).
- The ADF test returned a p-value of approximately 0.0248.
- At the 5% significance level, the monthly series was classified as stationary.
- Forecasts were generated for October, November, and December 2026.

## Forecast Results

| Month         | Forecast Sales |
| ------------- | -------------: |
| October 2026  |      20,453.68 |
| November 2026 |      23,311.50 |
| December 2026 |      21,474.67 |

Day 1/
|-- time_series_analysis.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- tests/
| |-- test_time_series.py
|-- output/
|-- monthly_sales.csv
|-- sales_forecast.csv
|-- stationarity_test.csv
|-- sales_trend.png
|-- arima_forecast.png

## Tools and Libraries

- Python
- Pandas
- Matplotlib
- Statsmodels
- ARIMA
- Augmented Dickey-Fuller Test
- Pytest
- Git and GitHub

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
python time_series_analysis.py
```

Run the tests:

```bash
python -m pytest tests/test_time_series.py -v
```

## Testing

All 5 test cases passed successfully.

## Limitations

The dataset contains only nine monthly observations. Therefore, it is too small to reliably identify yearly seasonality or establish a strong long-term forecasting pattern. The ARIMA forecasts should be treated as illustrative estimates, not guaranteed future sales values.
