from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

app = FastAPI()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect("db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


class Customer(BaseModel):
    customer_id: Optional[int] = None
    name: str
    phone: str

    class Config:
        from_attributes = True  # This enables ORM mode
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "phone": "123-456-7890"
            }
        }

class Item(BaseModel):
    item_id: Optional[int] = None
    name: str
    price: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Sample Item",
                "price": 29.99
            }
        }

class Order(BaseModel):
    order_id: Optional[int] = None
    customer_id: int
    order_date: int  # Unix timestamp
    total_amount: float
    notes: Optional[str] = ""

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "order_date": 1678901234,
                "total_amount": 99.99,
                "notes": "Express delivery requested"
            }
        }

# Customers Endpoints
@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (customer.name, customer.phone))
    conn.commit()
    customer.customer_id = cursor.lastrowid
    conn.close()
    return customer

@app.get("/customers/{id}", response_model=Customer)
def get_customer(id: int):
    conn = get_db_connection()
    customer = conn.execute("SELECT * FROM customers WHERE customer_id = ?", (id,)).fetchone()
    conn.close()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return dict(customer)

@app.delete("/customers/{id}")
def delete_customer(id: int):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM customers WHERE customer_id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

@app.put("/customers/{id}", response_model=Customer)
def update_customer(id: int, customer: Customer):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE customer_id = ?", 
                   (customer.name, customer.phone, id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.customer_id = id
    return customer

# Items Endpoints
@app.post("/items", response_model=Item)
def create_item(item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item.name, item.price))
    conn.commit()
    item.item_id = cursor.lastrowid
    conn.close()
    return item

@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    conn = get_db_connection()
    item = conn.execute("SELECT * FROM items WHERE item_id = ?", (id,)).fetchone()
    conn.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return dict(item)

@app.delete("/items/{id}")
def delete_item(id: int):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM items WHERE item_id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

@app.put("/items/{id}", response_model=Item)
def update_item(id: int, item: Item):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, price = ? WHERE item_id = ?", 
                   (item.name, item.price, id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    item.item_id = id
    return item

# Orders Endpoints
@app.post("/orders", response_model=Order)
def create_order(order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO orders (customer_id, order_date, total_amount, notes) VALUES (?, ?, ?, ?)", 
        (order.customer_id, order.order_date, order.total_amount, order.notes)
    )
    conn.commit()
    order.order_id = cursor.lastrowid
    conn.close()
    return order

@app.get("/orders/{id}", response_model=Order)
def get_order(id: int):
    conn = get_db_connection()
    order = conn.execute("SELECT * FROM orders WHERE order_id = ?", (id,)).fetchone()
    conn.close()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return dict(order)

@app.delete("/orders/{id}")
def delete_order(id: int):
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM orders WHERE order_id = ?", (id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.put("/orders/{id}", response_model=Order)
def update_order(id: int, order: Order):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET customer_id = ?, order_date = ?, total_amount = ?, notes = ? WHERE order_id = ?", 
        (order.customer_id, order.order_date, order.total_amount, order.notes, id)
    )
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_id = id
    return order
