# W10D4 - Forecasting Dashboard using Plotly and Streamlit

## Project Overview

This project develops an interactive stock forecasting dashboard using Streamlit and Plotly. It displays historical Reliance stock prices, future price predictions, forecasting metrics, and prediction intervals.

The dashboard uses the Prophet forecasting results generated in W10D2.

## Objectives

- Build an interactive forecasting dashboard.
- Visualize historical stock prices.
- Display future stock price predictions.
- Show forecasting performance metrics.
- Display prediction intervals.
- Allow users to explore and download forecast data.

## Dataset

- Dataset: Nifty 500 combined dataset.
- Selected company: Reliance.
- Historical period: 2012–2021.
- Records: 2,465.
- Target column: Close.

## Technologies Used

- Python
- Pandas
- Plotly
- Streamlit
- Pytest
- Prophet (forecast generated in W10D2)

## Dashboard Features

### 1. Model Performance

Displays three evaluation metrics:

- MAE: 319.42
- RMSE: 368.27
- MAPE: 15.98%

### 2. Historical Stock Prices

Displays Reliance historical closing prices using an interactive Plotly line chart with a date range slider.

### 3. Future Stock Price Forecast

Displays the next 30 business days of Prophet forecasts.

### 4. Prediction Interval

Shows lower and upper forecast bounds to represent prediction uncertainty.

### 5. Forecast Horizon Selector

Allows users to select between 5 and 30 business days.

### 6. Forecast Details

Displays forecast dates, predicted prices, lower bounds, and upper bounds.

### 7. CSV Download

Allows users to download the selected forecast data.

## Project Structure

```text
Week 10/
└── Day 4/
    ├── app.py
    ├── dashboard_utils.py
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    └── tests/
        └── test_dashboard.py
```

## Installation

Install the required dependencies:

```bash
pip install -r "Week 10/Day 4/requirements.txt"
```

## Run the Dashboard

From the repository root, execute:

```bash
python -m streamlit run "Week 10/Day 4/app.py"
```

The dashboard will open in the browser at the local Streamlit address.

## Run Tests

Execute:

```bash
python -m pytest "Week 10/Day 4/tests/test_dashboard.py" -v
```

## Testing Results

All 4 automated tests passed successfully.

The tests validate:

- Historical data loading and sorting.
- Forecast data loading and date conversion.
- Forecasting metrics loading.
- Handling of invalid forecast files.

## Conclusion

The project successfully combines Prophet forecasting results with Streamlit and Plotly to create an interactive forecasting dashboard. It helps users explore historical stock prices, understand future predictions, and evaluate model performance.

**Note:** Forecast values are estimates based on historical data and are not guaranteed future stock prices.
