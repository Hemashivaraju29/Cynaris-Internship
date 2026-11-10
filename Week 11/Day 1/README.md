# Week 11 - Day 1: Data Storytelling

## Project Overview
This project applies data storytelling principles to retail sales data. It uses Python, Pandas and Plotly to convert raw data into meaningful business insights.

## Objective
- Analyze overall sales performance.
- Compare regional and category-wise sales.
- Identify monthly sales trends.
- Present findings through interactive charts.
- Recommend business improvements.

## Dataset
Source: Week 07/Day 3/Sales_Data.csv

- Records: 24
- Period: January to September 2026
- Total sales: INR 308,400
- Total units sold: 1,079
- Average transaction value: INR 12,850

## Key Findings
- South recorded the highest regional sales: INR 89,200.
- East recorded the lowest regional sales: INR 59,800.
- Electronics generated the highest category revenue: INR 133,000.
- Grocery recorded the highest quantity sold: 542 units.
- June recorded the highest monthly sales: INR 43,000.
- January recorded the lowest monthly sales: INR 23,500.

## Business Recommendations
1. Study the successful sales strategies in the South region.
2. Investigate the lower sales performance in the East region.
3. Maintain product availability for Electronics.
4. Review Grocery pricing and product mix.
5. Investigate the sales decline after June.

## Visualizations
Four interactive Plotly charts are generated:
- Regional sales performance
- Category-wise sales performance
- Monthly sales trend
- Units sold by category

Charts and the JSON report are saved in the outputs folder.

## How to Run
Install dependencies:
pip install -r "Week 11/Day 1/requirements.txt"

Run analysis:
python "Week 11/Day 1/analysis.py"

Run tests:
python -m pytest "Week 11/Day 1/tests/test_analysis.py" -v

## Testing
Six automated tests cover data loading, validation, sales analysis, chart generation and JSON report generation.

Latest result: 6 passed.

## Limitations
- The dataset contains only 24 transactions.
- Customer-level, cost, discount and marketing data are unavailable.
- The findings show observed patterns and do not establish cause and effect.

## Conclusion
Data storytelling helps transform sales data into understandable insights and supports informed business decisions.
