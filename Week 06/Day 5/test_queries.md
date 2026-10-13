# W6D5 — Natural Language SQL Dashboard Test Report

**Project:** NL SQL Dashboard on CRM Data  
**Database:** `sales_db`  
**API endpoint:** `POST /cia/sql-analyst`  
**Test date:** 13 October 2026

## Test Summary

| No. | Natural-language question | Outcome |
|---:|---|---|
| 1 | How many customers are in the database? | PASS |
| 2 | Show each customer with their orders. | PASS |
| 3 | What is the total order value for each customer? | PARTIAL |
| 4 | What is the total value of all orders combined? | PASS |
| 5 | Which products have the highest total sales? | PARTIAL |
| 6 | Show every product and its total sales amount, ordered from highest to lowest. | PASS |
| 7 | Which city has the most customers? | PARTIAL |
| 8 | Which customer has the most orders? Show the customer name and number of orders. | PASS after prompt refinement |
| 9 | Show the top 3 products by total order value, from highest to lowest. | PASS |
| 10 | List all customers who have never placed an order. | PASS |

**Summary:** 7 passed, 3 partial, 0 final failures. One query required prompt refinement before returning the expected result.

## Detailed Test Results

### 1. Count customers

**Question:** How many customers are in the database?

```sql
SELECT COUNT(*) FROM customers;
```

**Observed result:** 5 customers.

**Outcome:** PASS — returned the expected customer count.

### 2. List customers and their orders

**Question:** Show each customer with their orders.

```sql
SELECT customers.customer_name, orders.order_id, orders.amount
FROM customers
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id;
```

**Observed result:** 6 rows. Anil had orders 103 and 101; Priya had order 102; Rahul had order 104. Sneha and Kiran had NULL order fields.

**Outcome:** PASS — retained customers without orders.

### 3. Total order value per customer

**Question:** What is the total order value for each customer?

**Generated SQL:**
```sql
SELECT SUM(o.amount) AS total_order_value
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id;
```

**Observed result:** Four totals: 85000, 40000, 12000, and 25000. Customer names were missing, and customers without orders were omitted.

**Outcome:** PARTIAL — the generated query did not fully satisfy the question.

**Suggested correction:**
```sql
SELECT
    c.customer_name,
    COALESCE(SUM(o.amount), 0) AS total_order_value
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name;
```

### 4. Total value of all orders

**Question:** What is the total value of all orders combined?

```sql
SELECT SUM(amount) FROM orders;
```

**Observed result:** 162000.00.

**Outcome:** PASS — returned the combined order value.

### 5. Product with the highest total sales

**Question:** Which products have the highest total sales?

```sql
SELECT product
FROM sales
GROUP BY product
ORDER BY SUM(amount) DESC
LIMIT 1;
```

**Observed result:** Laptop.

**Outcome:** PARTIAL — returned only one product despite the plural wording of the question.

### 6. Total sales amount by product

**Question:** Show every product and its total sales amount, ordered from highest to lowest.

```sql
SELECT product, SUM(amount) AS total_sales
FROM sales
GROUP BY product
ORDER BY total_sales DESC;
```

**Observed result:**

| Product | Total sales |
|---|---:|
| Laptop | 195000 |
| Phone | 85000 |
| Monitor | 30000 |
| Chair | 27000 |
| Table | 25000 |
| Desk | 18000 |

**Outcome:** PASS — returned products in descending sales order.

### 7. City with the most customers

**Question:** Which city has the most customers?

```sql
SELECT city
FROM customers
GROUP BY city
ORDER BY COUNT(*) DESC
LIMIT 1;
```

**Observed result:** Bengaluru.

**Outcome:** PARTIAL — returned the city, but did not include its customer count or show whether there was a tie.

### 8. Customer with the most orders

**Question:** Which customer has the most orders? Show the customer name and number of orders.

**Initial attempt:** Failed because the generated query referenced `customer_name` without joining the `customers` table. A retry returned a customer ID instead of the requested name.

**Final refined question:** Find the customer with the most orders by joining customers and orders. Return the customer name and order count.

```sql
SELECT c.customer_name, COUNT(o.order_id) AS num_orders
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_name
ORDER BY num_orders DESC
LIMIT 1;
```

**Observed result:** Anil — 2 orders.

**Outcome:** PASS after prompt refinement.

### 9. Top 3 products by order value

**Question:** Show the top 3 products by total order value, from highest to lowest.

```sql
SELECT product, SUM(amount)
FROM orders
GROUP BY product
ORDER BY SUM(amount) DESC
LIMIT 3;
```

**Observed result:**

| Product | Total order value |
|---|---:|
| Laptop | 55000 |
| Phone | 40000 |
| Monitor | 30000 |

**Outcome:** PASS — returned the top three products in descending order.

**Note:** An unnecessary follow-up suggestion about combining `sales` and `orders` was generated after the results.

### 10. Customers who have never placed an order

**Question:** List all customers who have never placed an order.

```sql
SELECT c.customer_id, c.customer_name, c.city
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id
HAVING COUNT(o.order_id) = 0;
```

**Observed result:**

| Customer | City |
|---|---|
| Sneha | Chennai |
| Kiran | Bengaluru |

**Outcome:** PASS — returned the two customers without orders.

## Conclusion

The endpoint successfully handled most tested natural-language questions. The tests also identified limitations involving incomplete aggregations, plural wording, missing counts, and join selection. These findings should be considered when evaluating the dashboard's reliability.
