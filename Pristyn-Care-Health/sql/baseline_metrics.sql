-- Checkpoint 2 baseline metrics (SQLite-style SQL)
-- Load the three CSV files into tables named:
-- sales_transactions, customer_data, product_catalogue

SELECT
    COUNT(*) AS transaction_count,
    COUNT(DISTINCT Customer_ID) AS unique_customers,
    SUM(Units) AS units_sold,
    ROUND(SUM(Units * Unit_Price), 2) AS gross_sales,
    ROUND(SUM(Units * Unit_Price * Discount_Pct / 100.0), 2) AS discount_amount,
    ROUND(SUM(Units * Unit_Price * (1 - Discount_Pct / 100.0)), 2) AS net_sales_before_returns,
    ROUND(SUM(Units * Unit_Price * (1 - Discount_Pct / 100.0) * (1 - Return_Flag)), 2) AS realized_sales_after_returns,
    ROUND(AVG(Return_Flag) * 100, 2) AS transaction_return_rate_pct
FROM sales_transactions;
