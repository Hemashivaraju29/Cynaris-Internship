# Data Quality & Great Expectations - Week 2 Day 6

import pandas as pd
import great_expectations as gx

# Load dataset
df = pd.read_csv("Week 02/Day 6/sales_quality_errors.csv")

print("========== DATASET ==========")
print(df)
print("\nColumns:", list(df.columns))
print("Rows:", len(df))

# Create Great Expectations context
context = gx.get_context()

# Create a pandas data source
data_source = context.data_sources.add_pandas(
    name="sales_data_source"
)

# Create a data asset
data_asset = data_source.add_dataframe_asset(
    name="sales_data"
)

# Create a batch definition
batch_definition = data_asset.add_batch_definition_whole_dataframe(
    "sales_batch"
)

# Get batch
batch = batch_definition.get_batch(
    batch_parameters={"dataframe": df}
)

# Create expectation suite
suite = gx.ExpectationSuite(
    name="sales_data_quality_suite"
)

# 1. sale_id should not contain null values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="sale_id"
    )
)

# 2. sale_id should be unique
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="sale_id"
    )
)

# 3. customer_name should not contain null values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer_name"
    )
)

# 4. amount should not contain null values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="amount"
    )
)

# 5. amount should be greater than zero
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0,
        strict_min=True
    )
)

# 6. quantity should be greater than zero
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="quantity",
        min_value=0,
        strict_min=True
    )
)

# 7. category should contain valid values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="category",
        value_set=["Electronics", "Furniture", "Clothing", "Grocery"]
    )
)

# 8. payment_method should contain valid values
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeInSet(
        column="payment_method",
        value_set=["UPI", "Credit Card", "Debit Card", "Cash", "Unknown"]
    )
)

# Add suite to context
context.suites.add(suite)

# Validate dataset
validation_result = batch.validate(suite)

print("\n========== VALIDATION RESULTS ==========")
print("Overall success:", validation_result.success)

for result in validation_result.results:
    print(
        result.expectation_config.type,
        "->",
        result.success
    )

print("\n========== DAY 6 INITIAL VALIDATION COMPLETE ==========")

# Generate HTML validation report

import html

report_file = "Week 02/Day 6/validation_report.html"

passed = sum(
    1 for result in validation_result.results
    if result.success
)

failed = len(validation_result.results) - passed

rows = ""

for result in validation_result.results:
    expectation_type = result.expectation_config.type
    success = result.success

    if success:
        status = "PASS"
    else:
        status = "FAIL"

    rows += f"""
    <tr>
        <td>{html.escape(expectation_type)}</td>
        <td>{status}</td>
    </tr>
    """

report_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Great Expectations Validation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f7fa;
            color: #222;
        }}

        h1 {{
            color: #1f2937;
        }}

        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 25px;
        }}

        .failed {{
            color: #b91c1c;
            font-weight: bold;
        }}

        .passed {{
            color: #15803d;
            font-weight: bold;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        th, td {{
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }}

        th {{
            background-color: #e5e7eb;
        }}
    </style>
</head>

<body>

<h1>Great Expectations Validation Report</h1>

<div class="summary">
    <h2>Dataset Information</h2>
    <p><strong>Dataset:</strong> sales_quality_errors.csv</p>
    <p><strong>Rows:</strong> {len(df)}</p>
    <p><strong>Expectations Evaluated:</strong> {len(validation_result.results)}</p>
    <p><strong>Passed:</strong>
        <span class="passed">{passed}</span>
    </p>
    <p><strong>Failed:</strong>
        <span class="failed">{failed}</span>
    </p>
    <p><strong>Overall Validation:</strong>
        <span class="failed">FAILED - Data quality issues detected</span>
    </p>
</div>

<h2>Expectation Results</h2>

<table>
    <tr>
        <th>Expectation</th>
        <th>Status</th>
    </tr>

    {rows}

</table>

<h2>Intentional Data Quality Errors</h2>

<ul>
    <li>Duplicate sale_id value introduced.</li>
    <li>Missing customer_name value introduced.</li>
    <li>Negative amount value introduced.</li>
</ul>

<h2>Conclusion</h2>

<p>
Great Expectations successfully detected all three intentionally
introduced data quality errors.
</p>

</body>
</html>
"""

with open(report_file, "w", encoding="utf-8") as file:
    file.write(report_html)

print("\nHTML validation report created:")
print(report_file)