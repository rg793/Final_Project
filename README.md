# Dosa Restaurant REST API

## Project Description
This project implements a REST API backend for a dosa restaurant, using FastAPI and SQLite. The application provides CRUD (Create, Read, Update, Delete) functionality for managing the following entities:
- Customers
- Items
- Orders

### Features
The application includes the following endpoints for interacting with the database:

#### Customers Endpoints
- **POST /customers**: Creates a customer in the database.
- **GET /customers/{id}**: Retrieves details of a specific customer by ID.
- **DELETE /customers/{id}**: Deletes a customer by ID.
- **PUT /customers/{id}**: Updates details of a customer by ID.

#### Items Endpoints
- **POST /items**: Creates an item in the database.
- **GET /items/{id}**: Retrieves details of a specific item by ID.
- **DELETE /items/{id}**: Deletes an item by ID.
- **PUT /items/{id}**: Updates details of an item by ID.

#### Orders Endpoints
- **POST /orders**: Creates an order in the database.
- **GET /orders/{id}**: Retrieves details of a specific order by ID.
- **DELETE /orders/{id}**: Deletes an order by ID.
- **PUT /orders/{id}**: Updates details of an order by ID.

### Relational Database
The database is an SQLite file named `db.sqlite`, initialized using the `init_db.py` script. It enforces relational constraints such as primary and foreign keys, as defined in the `example_orders.json` file.

## Implementation Details
### Code Walkthrough

#### `init_db.py`
The `init_db.py` script is responsible for setting up the SQLite database and populating it with the necessary structure and initial data. It achieves this by:
1. Parsing the `example_orders.json` file to extract data for customers, items, and orders.
2. Creating the SQLite database file `db.sqlite` and defining the schema using SQL statements.
3. Enforcing relational constraints such as primary keys and foreign keys to maintain data integrity.

**Highlights of `init_db.py` implementation:**
- **Database Connection**: The script connects to SQLite using the `sqlite3` library.
- **Table Creation**: SQL statements are used to create tables for customers, items, and orders, each with carefully defined columns and constraints.
  - For example, the `orders` table includes foreign keys linking to `customers` and `items`, ensuring relational integrity.
- **Data Initialization**: The script reads the `example_orders.json` file to populate initial data. Iterative inserts are performed to add rows to the tables.
- **Error Handling**: The script captures exceptions during database operations, ensuring the script exits gracefully on errors.

#### `main.py`
The `main.py` script implements the FastAPI application, defining endpoints for interacting with the database. The script uses SQL queries to perform CRUD operations.

**Key features of `main.py`:**
- **Dependency Injection**: Database connections are managed using a dependency that ensures clean opening and closing of connections.
- **Models**: Pydantic models are used to validate request and response data, ensuring type safety and consistency.
- **Endpoint Handlers**: Functions corresponding to each CRUD operation are defined for customers, items, and orders.

**Detailed Example:**
- **Creating a Customer (`POST /customers`)**:
  - Parses the incoming JSON payload.
  - Inserts the new customer into the `customers` table.
  - Returns the created customer’s ID as a response.

  ```python
  @app.post("/customers")
  async def create_customer(customer: Customer):
      query = "INSERT INTO customers (name, email) VALUES (?, ?)"
      cursor.execute(query, (customer.name, customer.email))
      db.commit()
      return {"id": cursor.lastrowid}
  ```

- **Retrieving an Order (`GET /orders/{id}`)**:
  - Fetches the order details from the `orders` table by ID.
  - Joins data from related tables to provide comprehensive order details (e.g., customer and item information).

- **Updating a Record (`PUT /items/{id}`)**:
  - Accepts updated data as JSON.
  - Updates the respective fields in the database using a parameterized query to prevent SQL injection.

- **Deleting a Record (`DELETE /customers/{id}`)**:
  - Removes the record from the database.
  - Ensures relational constraints are respected (e.g., cascading deletions or error handling).

### Error Handling
Both scripts include robust error handling:
- Database connection errors are logged and handled.
- Missing records result in clear 404 responses with descriptive messages.
- Validation errors from Pydantic models provide detailed feedback to API users.

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- FastAPI
- SQLite
- uvicorn

   ```

1. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Accessing the API
After starting the server, access the API documentation at:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Project Structure
```
.
├── db.sqlite
├── example_orders.json
├── init_db.py
├── main.py
├── requirements.txt
└── README.md
```

- **db.sqlite**: SQLite database file.
- **example_orders.json**: Example JSON file used to initialize the database.
- **init_db.py**: Script to set up the database structure and populate initial data.
- **main.py**: FastAPI application with CRUD endpoints.
- **requirements.txt**: Dependencies for the project.
- **README.md**: Project documentation.

---

Thank you for using the Dosa Restaurant REST API!

