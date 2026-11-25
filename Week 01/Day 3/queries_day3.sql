-- SQL Aggregate & Window Functions - Week 1 Day 3

USE sales_db;

-- 1. COUNT - Total number of sales
SELECT COUNT(*) AS total_sales
FROM sales;

-- 2. SUM - Total sales amount
SELECT SUM(amount) AS total_sales_amount
FROM sales;

-- 3. AVG - Average sales amount
SELECT AVG(amount) AS average_sales_amount
FROM sales;

-- 4. MAX - Highest sale amount
SELECT MAX(amount) AS highest_sale
FROM sales;

-- 5. MIN - Lowest sale amount
SELECT MIN(amount) AS lowest_sale
FROM sales;

-- 6. COUNT - Number of sales by category
SELECT category, COUNT(*) AS total_sales
FROM sales
GROUP BY category;

-- 7. SUM - Total sales amount by region
SELECT region, SUM(amount) AS total_sales_amount
FROM sales
GROUP BY region;

-- 8. AVG - Average sale amount by category
SELECT category, AVG(amount) AS average_sale
FROM sales
GROUP BY category;

-- 9. Group sales by month
SELECT
    DATE_FORMAT(sale_date, '%Y-%m') AS sales_month,
    COUNT(*) AS total_sales,
    SUM(amount) AS total_amount
FROM sales
GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
ORDER BY sales_month;

-- 10. Group sales by region and category
SELECT
    region,
    category,
    COUNT(*) AS total_sales,
    SUM(amount) AS total_amount
FROM sales
GROUP BY region, category
ORDER BY region, category;

-- 11. HAVING - Filter aggregated results
SELECT
    category,
    COUNT(*) AS total_sales,
    SUM(amount) AS total_amount
FROM sales
GROUP BY category
HAVING SUM(amount) > 50000;

-- 12. Window Function - Running total
SELECT
    sale_id,
    customer_name,
    amount,
    SUM(amount) OVER (ORDER BY sale_id) AS running_total
FROM sales
ORDER BY sale_id;