import pandas as pd
from sqlalchemy import create_engine, text

server = "localhost\\SQLEXPRESS"
database = "SalesETL"
driver = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"mssql+pyodbc://{server}/{database}"
    f"?driver={driver}&trusted_connection=yes"
)

engine = create_engine(connection_string)
print(engine)

raw_df = pd.read_sql("SELECT * FROM RawSales", engine)
customers_df = pd.read_sql("SELECT * FROM Customers", engine)
products_df = pd.read_sql("SELECT * FROM Products", engine)

customers_df = customers_df.rename(columns={"Name": "CustomerName"})
products_df = products_df.rename(columns={"Name": "ProductName"})

raw_df["SaleDate"] = pd.to_datetime(raw_df["SaleDate"])

fact_df = raw_df.merge(
    customers_df, on="CustomerName", how="left"
).merge(
    products_df, on="ProductName", how="left"
)

fact_df = fact_df[[
    "CustomerID",
    "ProductID",
    "Quantity",
    "TotalAmount",
    "SaleDate"
]]


fact_df = fact_df.dropna(subset=["CustomerID", "ProductID"])

with engine.connect() as conn:
    for _, row in fact_df.iterrows():

        query = text("""
            INSERT INTO FactSales
            (CustomerID, ProductID, Quantity, TotalAmount, SaleDate)
            VALUES
            (:CustomerID, :ProductID, :Quantity, :TotalAmount, :SaleDate)
        """)

        conn.execute(query, {
            "CustomerID": int(row["CustomerID"]),
            "ProductID": int(row["ProductID"]),
            "Quantity": int(row["Quantity"]),
            "TotalAmount": float(row["TotalAmount"]),
            "SaleDate": row["SaleDate"]
        })

    conn.commit()

print("FactSales Loaded Successfully!")
