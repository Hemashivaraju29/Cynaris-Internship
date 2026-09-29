# Executive Summary — Online Retail Capstone Analysis

## Business Question

How can an online retail business identify its most valuable products, customers, and markets to improve sales performance?

## Key Findings

The Online Retail dataset contained 541,909 transactions. After removing duplicate records, cancelled invoices, invalid quantities/prices, and handling missing values, 524,878 valid transactions remained.

The cleaned data generated approximately 10.64 million in revenue across 19,960 invoices, 3,922 products, 38 countries, and 4,338 customers.

The United Kingdom generated the highest total revenue at approximately 9.00 million, making it the largest revenue-contributing market in the dataset. The highest-revenue product entries included DOTCOM POSTAGE, REGENCY CAKESTAND 3 TIER, and PAPER CRAFT, LITTLE BIRDIE.

Monthly revenue was substantially higher during 2011 than during the early months of 2010. Revenue reached approximately 465K in September 2011, one of the highest monthly values in the dataset.

A Welch two-sample t-test comparing transaction revenue between the United Kingdom and Netherlands produced p < 0.001, indicating a statistically significant difference in average transaction revenue. However, the two markets have very different transaction volumes, so statistical significance should not be interpreted alone as evidence that one market is better.

## Actionable Recommendations

### 1. Strengthen high-value customer retention

Identify and segment high-value customers using total revenue and purchase frequency. Create loyalty offers, personalised product recommendations, and targeted campaigns for these customers.

### 2. Evaluate international markets using multiple KPIs

Track total revenue, transaction volume, average transaction value, and customer count together. Markets with higher average transaction values should be investigated for opportunities to increase customer acquisition and repeat purchases.

### 3. Prioritise high-revenue products and improve merchandising

Use product-level revenue analysis to support inventory planning, promotions, and product recommendations. Postage and manual entries should be analysed separately so they do not distort the performance of actual merchandise.

## Conclusion

The analysis shows that customer value, product performance, and geographic markets provide useful signals for improving retail sales performance. The Power BI dashboard enables management to explore these findings interactively using revenue, country, and month filters.
