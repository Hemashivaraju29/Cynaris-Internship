
import os
from pathlib import Path

import pymysql
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

required = [
    "CIA_DB_HOST",
    "CIA_DB_PORT",
    "CIA_DB_NAME",
    "CIA_DB_USER",
    "CIA_DB_PASSWORD",
]

missing = [name for name in required if not os.getenv(name)]
if missing:
    raise RuntimeError(
        "Missing environment variables: " + ", ".join(missing)
    )

connection = pymysql.connect(
    host=os.environ["CIA_DB_HOST"],
    port=int(os.environ["CIA_DB_PORT"]),
    database=os.environ["CIA_DB_NAME"],
    user=os.environ["CIA_DB_USER"],
    password=os.environ["CIA_DB_PASSWORD"],
    connect_timeout=5,
    read_timeout=10,
    write_timeout=10,
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS database_name")
        print("Database connection: successful")
        print("Connected database:", cursor.fetchone()["database_name"])

        cursor.execute("SHOW GRANTS")
        print("Permission check:")
        for row in cursor.fetchall():
            print(*row.values())
finally:
    connection.close()
