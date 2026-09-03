-- SQL JOINs - Week 1 Day 2

-- Select database
USE sales_db;

-- Create Customers table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    city VARCHAR(50)
);

-- Create Orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product VARCHAR(50),
    amount DECIMAL(10,2)
);

-- Insert sample customers
INSERT INTO customers (customer_id, customer_name, city)
VALUES
(1, 'Anil', 'Bengaluru'),
(2, 'Priya', 'Mumbai'),
(3, 'Rahul', 'Delhi'),
(4, 'Sneha', 'Chennai'),
(5, 'Kiran', 'Bengaluru');

-- Insert sample orders
INSERT INTO orders (order_id, customer_id, product, amount)
VALUES
(101, 1, 'Laptop', 55000),
(102, 2, 'Phone', 40000),
(103, 1, 'Monitor', 30000),
(104, 3, 'Chair', 12000),
(105, 6, 'Table', 25000);


-- 1. INNER JOIN
-- Shows only matching customers and orders
SELECT c.customer_name, o.product, o.amount
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 2. LEFT JOIN
-- Shows all customers, including customers without orders
SELECT c.customer_name, o.product, o.amount
FROM customers AS c
LEFT JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 3. RIGHT JOIN
-- Shows all orders, including orders without a matching customer
SELECT c.customer_name, o.product, o.amount
FROM customers AS c
RIGHT JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 4. FULL OUTER JOIN
-- MySQL does not directly support FULL OUTER JOIN.
-- UNION combines LEFT JOIN and RIGHT JOIN.
SELECT c.customer_name, o.product, o.amount
FROM customers AS c
LEFT JOIN orders AS o
ON c.customer_id = o.customer_id

UNION

SELECT c.customer_name, o.product, o.amount
FROM customers AS c
RIGHT JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 5. Demonstrate duplicate rows caused by JOIN
-- Anil has two orders, so he appears twice.
SELECT c.customer_id,
       c.customer_name,
       o.order_id,
       o.product
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 6. Fix duplicate-looking customer rows
-- GROUP BY returns one row per customer.
SELECT c.customer_id,
       c.customer_name,
       COUNT(o.order_id) AS total_orders
FROM customers AS c
LEFT JOIN orders AS o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;


-- 7. SELF JOIN
-- Find customers who live in the same city.
SELECT
    c1.customer_name AS customer1,
    c2.customer_name AS customer2,
    c1.city
FROM customers AS c1
INNER JOIN customers AS c2
ON c1.city = c2.city
AND c1.customer_id < c2.customer_id;


-- 8. Table aliases
-- Aliases make JOIN queries shorter and easier to read.
SELECT
    c.customer_name AS customer,
    o.product,
    o.amount
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id;