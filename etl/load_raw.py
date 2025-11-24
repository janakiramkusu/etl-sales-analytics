import pandas as pd
from sqlalchemy import create_engine, text

connection_string = (
    "mssql+pyodbc://localhost\\SQLEXPRESS/SalesETL"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)


engine = create_engine(connection_string)

df = pd.read_csv("data/sales_raw.csv")

df["TotalAmount"] = df["Quantity"] * df["Price"]

print("CSV Loaded Successfully:")
print(df.head())

with engine.connect() as conn:
    for _, row in df.iterrows():
        query = text("""
            INSERT INTO RawSales 
            (CustomerName, ProductName, Quantity, Price, TotalAmount, SaleDate, City)
            VALUES 
            (:CustomerName, :ProductName, :Quantity, :Price, :TotalAmount, :SaleDate, :City)
        """)

        conn.execute(query, {
            "CustomerName": row["CustomerName"],
            "ProductName": row["ProductName"],
            "Quantity": int(row["Quantity"]),
            "Price": float(row["Price"]),
            "TotalAmount": float(row["TotalAmount"]),
            "SaleDate": row["SaleDate"],
            "City": row["City"]
        })

    conn.commit()

print("Data inserted into RawSales successfully!")
