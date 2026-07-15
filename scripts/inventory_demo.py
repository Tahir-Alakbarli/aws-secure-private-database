"""Small EC2-to-RDS MySQL connectivity demonstration.

The password is requested securely at runtime and is never stored in this file.
This script resets only the demo table so repeated demonstrations stay predictable.
"""

from getpass import getpass

import mysql.connector
from mysql.connector import Error


SAMPLE_PURCHASES = [
    ("Wireless Mouse", 2, "Daniel"),
    ("USB-C Cable", 5, "Sarah"),
    ("Laptop Stand", 1, "Michael"),
    ("Mechanical Keyboard", 1, "Aylin"),
]


def main():
    print("Private RDS Inventory Demonstration")
    print("The password will not be displayed or saved.\n")

    host = input("RDS endpoint: ").strip()
    username = input("MySQL username [adminuser]: ").strip() or "adminuser"
    password = getpass("MySQL password: ")

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(
            host=host,
            port=3306,
            user=username,
            password=password,
            connection_timeout=10,
        )
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_db")
        cursor.execute("USE inventory_db")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS purchases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(100) NOT NULL,
                quantity INT UNSIGNED NOT NULL,
                buyer_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # This is a disposable demo table. Reset it so every run looks the same.
        cursor.execute("TRUNCATE TABLE purchases")
        cursor.executemany(
            """
            INSERT INTO purchases (product_name, quantity, buyer_name)
            VALUES (%s, %s, %s)
            """,
            SAMPLE_PURCHASES,
        )
        connection.commit()

        cursor.execute(
            """
            SELECT id, product_name, quantity, buyer_name, created_at
            FROM purchases
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

        print("\nConnection successful: EC2 reached the private RDS database.\n")
        print(f"{'ID':<4}{'Product Name':<24}{'Qty':<7}{'Buyer':<16}{'Created At'}")
        print("-" * 72)
        for item_id, product, quantity, buyer, created_at in rows:
            print(f"{item_id:<4}{product:<24}{quantity:<7}{buyer:<16}{created_at}")
        print(f"\nDisplayed {len(rows)} records from inventory_db.purchases.")

    except Error as error:
        print(f"\nDatabase connection failed: {error}")
        print("Check the RDS endpoint, password, database status, and security groups.")
        raise SystemExit(1) from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
