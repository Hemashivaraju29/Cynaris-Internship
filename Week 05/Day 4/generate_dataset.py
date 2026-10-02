import pandas as pd
import numpy as np

np.random.seed(42)

rows = 100_000

df = pd.DataFrame({
    "sale_id": np.arange(1, rows + 1),
    "customer_id": np.random.randint(1, 10_001, rows),
    "product": np.random.choice(
        ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse"],
        rows
    ),
    "category": np.random.choice(
        ["Electronics", "Accessories", "Computers"],
        rows
    ),
    "quantity": np.random.randint(1, 10, rows),
    "amount": np.round(np.random.uniform(500, 100000, rows), 2),
    "city": np.random.choice(
        ["Bengaluru", "Delhi", "Mumbai", "Chennai", "Hyderabad"],
        rows
    ),
    "payment_method": np.random.choice(
        ["UPI", "Card", "Cash", "Net Banking"],
        rows
    )
})

output = r"Week 05\Day 4\data_100k.csv"
df.to_csv(output, index=False)

print("Dataset created successfully")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("Saved to:", output)
