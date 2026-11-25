# Checkpoint 2 – Data Pipeline + Baseline Metrics

## Objective
Build a repeatable Python data pipeline, calculate baseline metrics, and maintain the analysis under version control as part of the Pristyn Care Health Analytics project.

## Data Sources
The pipeline uses the following datasets:

- `Pristyn-Care-Health/data/da_sales_transactions.csv`
- `Pristyn-Care-Health/data/da_customer_data.csv`
- `Pristyn-Care-Health/data/da_product_catalogue.csv`

## Pipeline
Main script: `Pristyn-Care-Health/src/pipeline.py`

The pipeline:
1. Reads the three CSV datasets.
2. Standardizes dates and numeric fields.
3. Joins sales data with customer and product reference data.
4. Calculates gross sales, discounts, net sales, and realized sales.
5. Performs basic data-quality checks.
6. Generates baseline metrics and supporting reports.

## How to Run

Run the following command from the repository root:

```bash
python "Pristyn-Care-Health/src/pipeline.py"
```

## Generated Outputs

The pipeline generates:

- `Pristyn-Care-Health/outputs/baseline_metrics.csv`
- `Pristyn-Care-Health/outputs/data_quality_report.csv`
- `Pristyn-Care-Health/outputs/channel_baseline.csv`

## Baseline Metric Definitions

- Gross Sales = Units × Unit Price
- Discount Amount = Gross Sales × Discount Percentage
- Net Sales Before Returns = Gross Sales − Discount Amount
- Realized Sales = Net Sales Before Returns × (1 − Return Flag)
- Transaction Return Rate = Returned Transactions / Total Transactions × 100

## Project Limitation

The available sales, customer, and product datasets do not contain the seven healthcare funnel stages: ad click, enquiry, consultation, diagnostics, booking, surgery, and follow-up.

Therefore, actual patient-funnel conversion rates, drop-offs, and funnel-based revenue impact cannot be calculated from the available data. Verified healthcare journey and financial data are required for these metrics.

## Project Structure

This checkpoint is maintained within the main `Pristyn-Care-Health` project:

- `data/` – Input datasets
- `src/` – Python pipeline
- `sql/` – SQL queries
- `outputs/` – Generated reports
- `docs/checkpoint-2/` – Checkpoint documentation

## Version Control

All project files are maintained in the main Cynaris Internship Git repository. Changes should be staged selectively, reviewed, committed, and pushed to the project branch.