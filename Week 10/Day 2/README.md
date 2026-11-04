# Week 10 - Day 2: Prophet Forecasting on Indian Market Data

## 1. Project Overview

This project uses Facebook Prophet to forecast Reliance stock closing prices using historical Indian stock market data.

The main objective is to understand time series forecasting, identify historical trends and seasonality, evaluate model performance, and predict future stock prices.

## 2. Dataset

**Dataset:** `nifty500_combined_eda.csv`

**Source:** Week 07, Day 1 project dataset.

**Selected Company:** Reliance

**Dataset Details:**

- Total records: 2,465
- Start date: 2 January 2012
- End date: 31 December 2021
- Target variable: Close price

The dataset contains historical stock market information, including Open, High, Low, Close, Adjusted Close, Volume and Company.

## 3. Technologies Used

- Python
- Pandas
- Matplotlib
- Facebook Prophet
- Scikit-learn
- Pytest
- VS Code

## 4. Project Methodology

### Step 1: Data Loading

Loaded the historical stock dataset using Pandas and selected Reliance company records.

### Step 2: Data Cleaning

- Converted Date into datetime format.
- Converted Close prices into numeric values.
- Removed missing and invalid records.
- Sorted records by date.

### Step 3: Model Development

Used Facebook Prophet to identify long-term trends and yearly seasonality in historical stock prices.

### Step 4: Model Evaluation

Split the dataset chronologically:

- 80% training data
- 20% testing data

Evaluated the model using:

- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)

### Step 5: Future Forecasting

Trained Prophet using all historical observations and generated a forecast for the next 30 business days.

### Step 6: Visualization

Generated historical stock price, forecast and trend/seasonality component charts.

## 5. Model Evaluation Results

| Metric | Result |
| ------ | -----: |
| MAE    | 319.42 |
| RMSE   | 368.27 |
| MAPE   | 15.98% |

### Interpretation

- MAE measures the average absolute difference between actual and predicted prices.
- RMSE gives more weight to larger prediction errors.
- MAPE represents the average percentage prediction error.

The model achieved a MAPE of approximately 15.98% on the held-out historical test period.

## 6. Generated Outputs

All generated files are stored in the `output/` directory.

| File                    | Description                          |
| ----------------------- | ------------------------------------ |
| evaluation_metrics.csv  | Model evaluation results             |
| future_forecast.csv     | 30-business-day forecast             |
| historical_trend.png    | Historical stock price visualization |
| prophet_forecast.png    | Future stock price forecast          |
| forecast_components.png | Trend and seasonality visualization  |

## 7. Project Structure

```text
Week 10/
└── Day 2/
    ├── tests/
    │   └── test_prophet.py
    ├── output/
    │   ├── evaluation_metrics.csv
    │   ├── future_forecast.csv
    │   ├── historical_trend.png
    │   ├── prophet_forecast.png
    │   └── forecast_components.png
    ├── .gitignore
    ├── prophet_forecasting.py
    ├── requirements.txt
    └── README.md
```

## 8. How to Run the Project

### Install dependencies

```bash
pip install -r "Week 10/Day 2/requirements.txt"
```

### Run the forecasting pipeline

```bash
python "Week 10/Day 2/prophet_forecasting.py"
```

### Run automated tests

```bash
python -m pytest "Week 10/Day 2/tests/test_prophet.py" -v
```

## 9. Testing

Automated testing was performed using Pytest.

The following four tests passed:

1. Data loading and preparation.
2. Reliance record count validation.
3. Model evaluation metrics validation.
4. Future forecast validation.

**Test Result: 4 passed.**

## 10. Limitations

- Stock prices are affected by market conditions and unexpected events.
- Prophet forecasts trends and seasonality but cannot reliably predict sudden market changes.
- The forecast uses business days and does not exclude Indian stock market holidays.
- Only Reliance stock data was selected for this analysis.
- The model results are based on historical data and do not guarantee future performance.

This project is intended for educational and analytical purposes, not as investment advice.

## 11. Conclusion

Successfully developed a time series forecasting project using Facebook Prophet on Reliance historical stock data.

The project covered data preparation, trend and seasonality analysis, model evaluation, future forecasting, visualization and automated testing.
