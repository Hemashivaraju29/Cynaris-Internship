-- SQL Fundamentals - Week 1 Day 1

-- Query 1: Display all sales records
SELECT *
FROM sales;

-- Query 2: Display selected columns
SELECT customer_name, product, amount
FROM sales;

-- Query 3: Sales above 50000
SELECT *
FROM sales
WHERE amount > 50000;

-- Query 4: Bengaluru sales above 20000
SELECT *
FROM sales
WHERE city = 'Bengaluru'
AND amount > 20000;

-- Query 5: Sales from Bengaluru or Mumbai
SELECT *
FROM sales
WHERE city = 'Bengaluru'
OR city = 'Mumbai';

-- Query 6: Sales not paid by Cash
SELECT *
FROM sales
WHERE NOT payment_method = 'Cash';

-- Query 7: Customers whose name starts with A
SELECT *
FROM sales
WHERE customer_name LIKE 'A%';

-- Query 8: Sales paid using UPI or Credit Card
SELECT *
FROM sales
WHERE payment_method IN ('UPI', 'Credit Card');

-- Query 9: Sales between 20000 and 50000
SELECT *
FROM sales
WHERE amount BETWEEN 20000 AND 50000;

-- Query 10: Sales with missing payment method
SELECT *
FROM sales
WHERE payment_method IS NULL;