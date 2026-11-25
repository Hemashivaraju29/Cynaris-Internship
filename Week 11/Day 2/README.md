# W11D2: Building Executive Reports – Plotly + python-pptx

## Objective
Convert sales data analysis into an executive-ready report using Plotly charts and PowerPoint automation.

## Dataset
Source: Week 07/Day 3/Sales_Data.csv

- Transactions: 24
- Total sales: INR 308,400
- Average transaction: INR 12,850
- Units sold: 1,079

## Tools Used
- Python 3.11
- Pandas
- Plotly
- python-pptx
- Pytest
- VS Code
- Git and GitHub

## Implementation
1. Loaded and validated the sales dataset.
2. Calculated sales metrics using Pandas.
3. Analysed regional, category, and monthly performance.
4. Generated three interactive Plotly charts.
5. Created a five-slide PowerPoint report.
6. Added executive recommendations.
7. Created automated tests using Pytest.

## Key Findings
- South recorded the highest regional sales: INR 89,200.
- Electronics generated the highest category sales: INR 133,000.
- June recorded the highest monthly sales: INR 43,000.
- East recorded the lowest regional sales: INR 59,800.

## Outputs
- outputs/charts/regional_sales.html
- outputs/charts/category_sales.html
- outputs/charts/monthly_sales.html
- outputs/executive_report.pptx

## Testing
Command:
python -m pytest "Week 11\Day 2\tests" -v

Result: 5 tests passed.

## Business Recommendations
1. Study successful strategies in the South region.
2. Improve sales performance in lower-performing regions.
3. Explore growth opportunities across product categories.
4. Investigate monthly sales fluctuations.
5. Monitor revenue and units sold regularly.

## Limitations
- Dataset contains only 24 transactions.
- Analysis covers nine months.
- Customer-level, cost, discount, and marketing data are unavailable.
- Observed patterns do not establish causation.

## Conclusion
This project demonstrates how Python, Pandas, Plotly, and python-pptx can automate executive reporting and communicate business insights effectively.
