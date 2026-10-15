-- Advanced SQL - Week 1 Day 4

USE sales_db;


-- 1. Non-correlated subquery
-- Find sales above the average sale amount

SELECT
    sale_id,
    customer_name,
    amount
FROM sales
WHERE amount > (
    SELECT AVG(amount)
    FROM sales
)
ORDER BY amount DESC;


-- 2. Correlated subquery
-- Find the top performer (highest sale) in each region

SELECT
    s.sale_id,
    s.customer_name,
    s.region,
    s.amount
FROM sales AS s
WHERE s.amount = (
    SELECT MAX(s2.amount)
    FROM sales AS s2
    WHERE s2.region = s.region
)
ORDER BY s.region;


-- 3. CTE using WITH clause
-- Find categories whose total sales are greater than 100000

WITH category_sales AS (
    SELECT
        category,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY category
)
SELECT
    category,
    total_sales
FROM category_sales
WHERE total_sales > 100000
ORDER BY total_sales DESC;


-- 4. Chain two CTEs
-- Find regions whose total sales are above the average regional sales

WITH regional_sales AS (
    SELECT
        region,
        SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
),
regional_average AS (
    SELECT
        AVG(total_sales) AS average_sales
    FROM regional_sales
)
SELECT
    region,
    total_sales
FROM regional_sales
WHERE total_sales > (
    SELECT average_sales
    FROM regional_average
)
ORDER BY total_sales DESC;