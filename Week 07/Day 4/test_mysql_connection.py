
import getpass
import mysql.connector

user = input("MySQL username: ")
password = getpass.getpass("MySQL password: ")

try:
    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user=user,
        password=password,
        connection_timeout=5
    )

    print("Connection successful!")

    cursor = connection.cursor()
    cursor.execute("SELECT VERSION()")
    print("MySQL version:", cursor.fetchone()[0])

    cursor.execute("SHOW DATABASES")
    print("Available databases:")
    for row in cursor.fetchall():
        print("-", row[0])

    cursor.close()
    connection.close()

except mysql.connector.Error as error:
    print("Connection failed:", error)
