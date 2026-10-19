
import getpass
import mysql.connector

username = input("MySQL username: ")
password = getpass.getpass("MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user=username,
        password=password,
        database="sales_db",
        connection_timeout=5
    )

    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")

    tables = [row[0] for row in cursor.fetchall()]

    print("\nTables in sales_db:")
    for table in tables:
        print(f"\nTable: {table}")
        cursor.execute(f"DESCRIBE `{table}`")
        for column in cursor.fetchall():
            print(f"  {column[0]} - {column[1]}")

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Database inspection failed:", error)
