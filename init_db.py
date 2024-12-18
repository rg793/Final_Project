import sqlite3
import json
from collections import defaultdict

def init_database():
    # Connect to SQLite database (creates if not exists)
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Create tables
    cursor.executescript('''
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS items;
        DROP TABLE IF EXISTS customers;

        -- Customers table with ID, name, and phone
        CREATE TABLE customers (
            customer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL
        );

        -- Items table with ID, name, and price
        CREATE TABLE items (
            item_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            price DECIMAL(10,2) NOT NULL
        );

        -- Orders table with all order details
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date INTEGER NOT NULL,  -- timestamp
            total_amount DECIMAL(10,2) NOT NULL,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        );

        -- Order items junction table
        CREATE TABLE order_items (
            order_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_at_time DECIMAL(10,2) NOT NULL,
            PRIMARY KEY (order_id, item_id),
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (item_id) REFERENCES items (item_id)
        );
    ''')

    # Load data from example_orders.json
    with open('example_orders.json') as f:
        orders_data = json.load(f)

    # Insert unique customers
    for order in orders_data:
        cursor.execute('''
            INSERT OR IGNORE INTO customers (name, phone)
            VALUES (?, ?)
        ''', (order['name'], order['phone']))

    # Insert unique items
    for order in orders_data:
        for item in order['items']:
            cursor.execute('''
                INSERT OR IGNORE INTO items (name, price)
                VALUES (?, ?)
            ''', (item['name'], item['price']))

    # Insert orders and their items
    for order in orders_data:
        # Calculate total amount
        total_amount = sum(item['price'] for item in order['items'])
        
        # Get customer_id
        cursor.execute('SELECT customer_id FROM customers WHERE phone = ?', (order['phone'],))
        customer_id = cursor.fetchone()[0]

        # Insert order
        cursor.execute('''
            INSERT INTO orders (customer_id, order_date, total_amount, notes)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, order['timestamp'], total_amount, order.get('notes', '')))
        
        order_id = cursor.lastrowid

        # Count quantities for each item in this order
        item_quantities = defaultdict(int)
        for item in order['items']:
            item_quantities[item['name']] += 1

        # Insert order items with quantities
        for item_name, quantity in item_quantities.items():
            cursor.execute('SELECT item_id FROM items WHERE name = ?', (item_name,))
            item_id = cursor.fetchone()[0]
            
            # Get price from the original order
            price = next(item['price'] for item in order['items'] if item['name'] == item_name)
            
            cursor.execute('''
                INSERT INTO order_items (order_id, item_id, quantity, price_at_time)
                VALUES (?, ?, ?, ?)
            ''', (order_id, item_id, quantity, price))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_database()