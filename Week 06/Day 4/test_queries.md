# Week 6 Day 4 — Vanna SQL Analyst Test Evidence

## Objective

Test the Vanna natural-language SQL analyst API and manually verify the generated SQL against the `sales_db` MySQL database.

## API Endpoint

`POST http://127.0.0.1:8000/cia/sql-analyst`

## Test Results

| Test | Natural-language query                              | Status            | Notes                                                                                                               |
| ---- | --------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1    | What is the total sales amount by city?             | PASS              | Correct grouping and sum; returned Bengaluru, Delhi, Mumbai, and Chennai totals.                                    |
| 2    | Show total sales by region.                         | PASS              | Correct grouping by region and descending sales order.                                                              |
| 3    | Which products have the highest total sales?        | PASS              | Correct grouping by product and descending sales order.                                                             |
| 4    | What is the average sale amount for each category?  | PASS              | Correct category grouping and average calculation.                                                                  |
| 5    | Show total sales by payment method.                 | PARTIAL           | SQL is correct, but one result has a blank payment-method label.                                                    |
| 6    | How many sales records are in the sales table?      | PASS              | Returned 10 records.                                                                                                |
| 7    | What is the total quantity sold by product?         | PASS              | Correct grouping by product and quantity sum.                                                                       |
| 8    | Show total sales by city for Bengaluru and Delhi.   | NEEDS IMPROVEMENT | First generated query omitted the city filter. A corrected query returned two rows when executed directly in MySQL. |
| 9    | Which category has the highest average sale amount? | PASS              | Correct descending average calculation with `LIMIT 1`.                                                              |
| 10   | Show the top three products by total sales.         | PASS              | Correct descending sales order with `LIMIT 3`; returned Laptop, Phone, and Monitor.                                 |

## Manual SQL Verification

### Bengaluru and Delhi filter

```sql
SELECT city, SUM(amount) AS total_sales
FROM sales
WHERE city IN ('Bengaluru', 'Delhi')
GROUP BY city
ORDER BY total_sales DESC;
```

Result: 2 rows returned in MySQL Workbench.

### Missing payment method check

```sql
SELECT sale_id, payment_method, amount
FROM sales
WHERE payment_method IS NULL
   OR TRIM(payment_method) = '';
```

Result: 1 row returned in MySQL Workbench. The specific row values should be recorded from the result grid.

## Known Issues

- Improve the model prompt or training so city-specific questions consistently include the requested `WHERE` filter.
- Investigate the row with a missing payment method; do not silently discard it.
- An API status of `completed` should be supplemented by checking generated SQL and returned results.

## Conclusion

The API responded to all 10 natural-language tests. Most generated SQL was appropriate. One city-filter query required correction, and one payment-method result requires data-quality review.
