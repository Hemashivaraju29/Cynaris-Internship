# Week 09 Day 5 – Tracked Data Analytics Experiment Pipeline

## Objective

Build a reproducible data analytics pipeline using MLflow to track experiments, parameters, metrics, datasets, and output artifacts.

## Dataset

- File: `Week 07/Day 3/Sales_Data.csv`
- Rows: 24
- Columns: 5
- Fields: Date, Region, Category, Sales, Units Sold

## Experiments

1. Original Dataset – analyzes the original sales data.
2. After Duplicate Removal – removes duplicate rows and analyzes the cleaned data.
3. Pipeline Comparison – records the comparison report as an MLflow artifact.

## Metrics Tracked

- Number of rows and columns
- Missing cells
- Duplicate rows
- Total, average, maximum, and minimum sales
- Total units sold

## MLflow Tracking

Experiment name: `W9D5-Tracked-DA-Pipeline`

Tracking database: `output/mlflow.db`

Each experiment records parameters, metrics, dataset artifacts, descriptive statistics, and JSON metrics.

## Results

| Metric         | Original | Cleaned |
| -------------- | -------: | ------: |
| Rows           |       24 |      24 |
| Missing Cells  |        0 |       0 |
| Duplicate Rows |        0 |       0 |
| Total Sales    |   308400 |  308400 |
| Average Sales  |    12850 |   12850 |
| Maximum Sales  |    28700 |   28700 |
| Minimum Sales  |     4200 |    4200 |
| Units Sold     |     1079 |    1079 |

Both experiments produced identical results because the original dataset contained no duplicate rows.

## Testing

Run from the Day 5 directory:

`python -m pytest tests/test_experiment_pipeline.py -v`

Result: 4 tests passed.

## Tools Used

Python, Pandas, MLflow, SQLite, Pytest, Git, GitHub, VS Code, PowerShell.

## Conclusion

Successfully implemented a tracked data analytics experiment pipeline. MLflow records experiment parameters, metrics, datasets, and artifacts, making the workflow reproducible and easier to compare.

## How to Run the Pipeline

1. Activate the project virtual environment.
2. Install dependencies using:

   `pip install -r requirements.txt`

3. Run the pipeline:

   `python experiment_pipeline.py`

4. View the generated comparison report in the output folder.

## Reproducibility

- The pipeline uses a separate SQLite tracking database.
- Each experiment receives a unique MLflow Run ID.
- Dataset versions, parameters, metrics, and reports are logged as artifacts.
- The comparison report helps evaluate the original and cleaned datasets.

## Project Structure

- `experiment_pipeline.py` – Main experiment pipeline.
- `tests/` – Automated test cases.
- `output/` – Generated reports and MLflow database.
- `requirements.txt` – Required Python packages.
- `README.md` – Project documentation.
