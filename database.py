import sqlite3

def create_database():
    # Connect to (or create) our database file
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()

    # ---- Create customers table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT,
            signup_date TEXT
        )
    """)

    # ---- Create products table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL
        )
    """)

    # ---- Create orders table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # ---- Insert sample customers ----
    customers = [
        (1, "Ravi Kumar", "Chennai", "2024-01-15"),
        (2, "Priya Sharma", "Bangalore", "2024-02-20"),
        (3, "Arjun Reddy", "Hyderabad", "2024-03-05"),
        (4, "Sneha Iyer", "Chennai", "2024-04-10"),
        (5, "Karthik Rao", "Mumbai", "2024-05-25"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?)", customers
    )

    # ---- Insert sample products ----
    products = [
        (1, "Laptop", "Electronics", 55000.0),
        (2, "Headphones", "Electronics", 2500.0),
        (3, "Office Chair", "Furniture", 8000.0),
        (4, "Desk Lamp", "Furniture", 1200.0),
        (5, "Backpack", "Accessories", 1800.0),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?)", products
    )

    # ---- Insert sample orders ----
    orders = [
        (1, 1, 1, 1, "2024-06-01"),
        (2, 2, 2, 2, "2024-06-03"),
        (3, 1, 3, 1, "2024-06-05"),
        (4, 3, 1, 1, "2024-06-07"),
        (5, 4, 5, 1, "2024-06-10"),
        (6, 5, 2, 3, "2024-06-12"),
        (7, 2, 4, 2, "2024-06-15"),
        (8, 3, 5, 1, "2024-06-18"),
        (9, 1, 2, 1, "2024-06-20"),
        (10, 4, 1, 1, "2024-06-25"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO orders VALUES (?, ?, ?, ?, ?)", orders
    )

    # Save changes and close
    conn.commit()
    conn.close()
    print("✅ Database created successfully as store.db")

if __name__ == "__main__":
    create_database()
    