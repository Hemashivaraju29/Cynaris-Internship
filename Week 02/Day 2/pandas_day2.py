# Advanced Pandas - Week 2 Day 2

import pandas as pd

# Create customers DataFrame
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4],
    "customer_name": ["Anil", "Priya", "Rahul", "Sneha"],
    "city": ["Bengaluru", "Mumbai", "Delhi", "Chennai"]
})

# Create orders DataFrame
orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105],
    "customer_id": [1, 2, 1, 3, 5],
    "product": ["Laptop", "Phone", "Monitor", "Chair", "Table"],
    "amount": [55000, 40000, 30000, 12000, 25000]
})

print("Customers DataFrame:")
print(customers)

print("\nOrders DataFrame:")
print(orders)

# 1. INNER JOIN
inner_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="inner"
)

print("\n1. INNER JOIN:")
print(inner_join)

# 2. LEFT JOIN
left_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="left"
)

print("\n2. LEFT JOIN:")
print(left_join)

# 3. RIGHT JOIN
right_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="right"
)

print("\n3. RIGHT JOIN:")
print(right_join)

# 4. OUTER JOIN
outer_join = pd.merge(
    customers,
    orders,
    on="customer_id",
    how="outer"
)

print("\n4. OUTER JOIN:")
print(outer_join)

# 5. PIVOT TABLE - Sales by Region and Product

sales_data = pd.DataFrame({
    "region": ["South", "South", "North", "North", "West", "West"],
    "product": ["Laptop", "Phone", "Laptop", "Phone", "Laptop", "Phone"],
    "amount": [55000, 40000, 65000, 30000, 75000, 45000]
})

print("\nSales Data for Pivot Table:")
print(sales_data)

pivot_table = pd.pivot_table(
    sales_data,
    values="amount",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

print("\n5. PIVOT TABLE - Sales by Region and Product:")
print(pivot_table)

# 6. MELT - Convert Wide Data to Long Format

wide_data = pd.DataFrame({
    "region": ["North", "South", "West"],
    "Laptop": [65000, 55000, 75000],
    "Phone": [30000, 40000, 45000]
})

print("\nWide Data:")
print(wide_data)

long_data = pd.melt(
    wide_data,
    id_vars=["region"],
    var_name="product",
    value_name="sales"
)

print("\n6. MELT - Long Format:")
print(long_data)

# 7. METHOD CHAINING - Multiple Pandas Operations

result = (
    sales_data
    .query("amount > 40000")
    .groupby("region", as_index=False)["amount"]
    .sum()
    .sort_values("amount", ascending=False)
)

print("\n7. METHOD CHAINING - Sales Above 40000:")
print(result)
