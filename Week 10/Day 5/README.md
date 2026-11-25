# W10D5 – Sales Forecasting Dashboard

## 1. Project Overview

This project develops an interactive Sales Forecasting Dashboard using Python, Streamlit, and Plotly. It analyses historical sales data and predicts sales for the next three months using a moving-average forecasting method.

## 2. Objectives

- Analyse historical sales performance.
- Forecast future monthly sales.
- Compare sales across different regions.
- Analyse sales by product category.
- Evaluate forecasting performance using error metrics.
- Present business insights through an interactive dashboard.

## 3. Dataset Information

**Dataset:** `Sales_Data.csv`

**Source:** Week 07, Day 3

| Column     | Description          |
| ---------- | -------------------- |
| Date       | Transaction date     |
| Region     | Sales region         |
| Category   | Product category     |
| Sales      | Sales revenue        |
| Units Sold | Number of units sold |

Dataset contains 24 records covering January to September 2026.

## 4. Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit
- Pytest

## 5. Forecasting Methodology

A three-month moving-average forecasting method is used.

The process includes:

1. Load and validate the sales dataset.
2. Clean date and numerical columns.
3. Filter records by region and category.
4. Aggregate sales into monthly totals.
5. Calculate the average of the previous three months.
6. Forecast sales for October, November, and December 2026.
7. Evaluate model performance using MAE and RMSE.

## 6. Forecast Results

| Month         | Forecast Sales |
| ------------- | -------------: |
| October 2026  |     ₹30,100.00 |
| November 2026 |     ₹30,133.33 |
| December 2026 |     ₹28,377.78 |

## 7. Model Evaluation

The model was evaluated using the last three months as a historical test period.

| Metric |     Result |
| ------ | ---------: |
| MAE    | ₹10,203.70 |
| RMSE   | ₹11,087.62 |

Lower MAE and RMSE values indicate smaller forecasting errors.

## 8. Dashboard Features

- Total sales and average monthly sales.
- Total units sold.
- Next-month sales forecast.
- Interactive monthly sales trend chart.
- Historical sales versus forecast chart.
- Region and category filters.
- Sales analysis by region.
- Sales analysis by category.
- Forecast details table.
- Download forecast results as CSV.
- Model evaluation metrics.

## 9. Project Structure

```text
Week 10/
└── Day 5/
    ├── app.py
    ├── forecasting_utils.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── tests/
        ├── conftest.py
        └── test_forecasting.py
```

## 10. Installation and Execution

Install the required libraries:

```bash
pip install -r "Week 10/Day 5/requirements.txt"
```

Run the dashboard from the repository root:

```bash
python -m streamlit run "Week 10/Day 5/app.py"
```

Run automated tests:

```bash
python -m pytest "Week 10/Day 5/tests/test_forecasting.py" -v
```

## 11. Testing Results

Eight automated tests were executed successfully.

**Result: 8 passed.**

Tests cover data loading, region filtering, category filtering, monthly aggregation, forecasting, invalid forecast windows, model evaluation, and invalid file handling.

## 12. Limitations

- The dataset contains only 24 records.
- The forecasting model uses a simple moving average.
- The dataset covers only nine months.
- Seasonal patterns and long-term trends are not modelled.
- Forecast values are estimates and should not be treated as guaranteed future sales.

## 13. Conclusion

The project successfully demonstrates how historical sales data can be analysed and future sales can be estimated using Python. The Streamlit and Plotly dashboard presents business performance and forecasting results in an interactive and understandable format.
