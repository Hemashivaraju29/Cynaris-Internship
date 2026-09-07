# Checkpoint 2 – Data Pipeline + Baseline Metrics

## Objective
Build a repeatable Python data pipeline, calculate baseline metrics, and keep the analysis version-controlled.

## Data sources
- `data/da_sales_transactions.csv`
- `data/da_customer_data.csv`
- `data/da_product_catalogue.csv`

## Pipeline
`src/pipeline.py`:
1. Reads the three CSV files.
2. Standardizes dates and numeric fields.
3. Joins sales to customer and product reference data.
4. Calculates gross sales, discount amount, net sales, and realized sales.
5. Runs basic data-quality checks.
6. Writes baseline metrics and supporting outputs to `outputs/`.

## Run
```bash
python src/pipeline.py
```

## Outputs
- `outputs/baseline_metrics.csv`
- `outputs/data_quality_report.csv`
- `outputs/channel_baseline.csv`

## Baseline definitions
- Gross Sales = Units × Unit Price
- Discount Amount = Gross Sales × Discount %
- Net Sales Before Returns = Gross Sales − Discount Amount
- Realized Sales = Net Sales Before Returns × (1 − Return Flag)
- Transaction Return Rate = Returned transactions / total transactions

## Important project limitation
The supplied files are sales/customer/product datasets and do not contain the seven healthcare funnel stages (ad click, enquiry, consultation, diagnostics, booking, surgery, follow-up). Therefore, true patient-funnel conversion/drop-off and funnel-based revenue-lift metrics cannot yet be calculated from these files. This should be resolved with the stakeholder before the final funnel analysis.

## Version control
Recommended Git workflow:
```bash
git add .
git commit -m "Checkpoint 2: data pipeline and baseline metrics"
git push
```
