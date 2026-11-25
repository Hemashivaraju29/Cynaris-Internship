import random
from pathlib import Path

import pandas as pd


OUTPUT_PATH = Path(__file__).parent / "data_100k.csv"

random.seed(42)

customers = [
    "Anil",
    "Ananya",
    "Rahul",
    "Priya",
    "Kiran",
    "Divya",
    "Sneha",
    "Arjun",
    "Vijay",
    "Meena",
]

products = [
    "Laptop",
    "Mobile",
    "Tablet",
    "Headphones",
    "Keyboard",
    "Monitor",
]

categories = [
    "Electronics",
    "Accessories",
    "Computers",
]

cities = [
    "Bengaluru",
    "Mysuru",
    "Hubballi",
    "Mangaluru",
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Chennai",
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash",
]

rows = []

for sale_id in range(1, 100001):
    rows.append(
        {
            "sale_id": sale_id,
            "customer_name": random.choice(customers),
            "product": random.choice(products),
            "category": random.choice(categories),
            "quantity": random.randint(1, 10),
            "amount": round(random.uniform(500, 100000), 2),
            "city": random.choice(cities),
            "payment_method": random.choice(payment_methods),
        }
    )

df = pd.DataFrame(rows)

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset created successfully: {OUTPUT_PATH}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(df.head())