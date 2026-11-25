\# W9D4 – MLflow Dashboard: Compare Model Versions



\## Objective

To compare different registered machine learning model versions using MLflow Tracking and Model Registry.



\## Tools Used

\- Python

\- Pandas

\- Scikit-learn

\- MLflow

\- SQLite

\- Pytest



\## Project Files

\- `compare\_model\_versions.py` – Trains a Linear Regression model, registers a new version, and compares registered versions.

\- `tests/test\_compare\_model\_versions.py` – Contains automated tests.

\- `output/model\_version\_comparison.csv` – Stores the model comparison results.



\## Dataset

The project uses `Sales\_Data.csv` from Week 07 Day 3.



\- Feature: Units Sold

\- Target: Sales

\- Algorithm: Linear Regression

\- Train-test split: 75:25

\- Random state: 42



\## Model Comparison



The script compares registered model versions using:

\- MAE (Mean Absolute Error)

\- RMSE (Root Mean Squared Error)

\- R² (R-squared)



| Version | MAE | RMSE | R² | Status |

|---|---:|---:|---:|---|

| 1 | 4753.09 | 6929.94 | Not available | READY |

| 2 | 4753.09 | 6929.94 | 0.0172 | READY |

| 3 | 4753.09 | 6929.94 | 0.0172 | READY |



All three versions have the same MAE and RMSE. Therefore, no measurable improvement in prediction accuracy was observed.



Version 1's R² value was not retrieved in the comparison output because its metric was stored using a different naming convention. The comparison script supports both uppercase and lowercase metric names.



\## MLflow Dashboard



The MLflow UI was started using:



```powershell

python -m mlflow ui --backend-store-uri "sqlite:///Week 09/Day 2/output/mlflow.db" --host 127.0.0.1 --port 5002 --workers 1

```



Dashboard URL: `http://127.0.0.1:5002`



The dashboard was used to inspect experiment runs and registered model versions. Versions 1, 2, and 3 were verified in the Model Registry with READY status.



\## Run the Project



```powershell

python "Week 09\\Day 4\\compare\_model\_versions.py"

```



\## Run Tests



```powershell

python -m pytest "Week 09\\Day 4\\tests\\test\_compare\_model\_versions.py" -v

```



\## Test Results



All 3 automated tests passed successfully.



