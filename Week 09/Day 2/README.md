# W9D2: MLflow Model Registry

## Objective
Train a Linear Regression model, track its metrics with MLflow, and register the model.

## Dataset
Source: Week 07/Day 3/Sales_Data.csv
Feature: Units Sold
Target: Sales

## Implementation
- Trained a Linear Regression model using scikit-learn.
- Logged parameters and evaluation metrics using MLflow.
- Registered W9D2-Sales-Prediction-Model, Version 1.
- Saved evaluation metrics to output/evaluation_metrics.csv.
- Used a separate SQLite database for W9D2.

## Evaluation Metrics
- MAE: approximately 4753.09
- MSE: approximately 48024010
- RMSE: approximately 6929.94
- R2 Score: approximately 0.0172

The low R2 score indicates that Units Sold alone is not sufficient to predict sales accurately.

## How to Run
python "Week 09\Day 2\model_registry.py"

## Tools Used
Python, Pandas, scikit-learn, MLflow, SQLite, Git, GitHub, VS Code, PowerShell.
