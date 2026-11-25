import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "outputs" / "pristyn_healthcare.db"

with sqlite3.connect(DB_PATH) as connection:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    tables = cursor.fetchall()

    print("DATABASE TABLES")

    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        print(f"{table_name}: {count} records")