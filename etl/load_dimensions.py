import pandas as pd
from sqlalchemy import create_engine, text

connection_string = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/SalesETL"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(connection_string)

# -------------------------------
# LOAD CUSTOMERS DIMENSION
# -------------------------------
customers = pd.read_csv("data/customers.csv")

with engine.connect() as conn:
    for _, row in customers.iterrows():
        query = text("""
            INSERT INTO Customers (Name, City)
            VALUES (:Name, :City)
        """)
        conn.execute(query, {"Name": row["Name"], "City": row["City"]})
    conn.commit()

print("Customers Dimension Loaded Successfully!")

# -------------------------------
# LOAD PRODUCTS DIMENSION
# -------------------------------
products = pd.read_csv("data/products.csv")

with engine.connect() as conn:
    for _, row in products.iterrows():
        query = text("""
            INSERT INTO Products (Name, Category, UnitPrice)
            VALUES (:Name, :Category, :UnitPrice)
        """)
        conn.execute(query, {
            "Name": row["Name"],
            "Category": row["Category"],
            "UnitPrice": float(row["UnitPrice"])
        })
    conn.commit()

print("Products Dimension Loaded Successfully!")
