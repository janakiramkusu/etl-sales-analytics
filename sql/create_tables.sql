CREATE DATABASE SalesETL;
GO
USE SalesETL;
GO

CREATE TABLE Customers (
    CustomerID INT IDENTITY PRIMARY KEY,
    Name VARCHAR(100),
    City VARCHAR(100)
);

CREATE TABLE Products (
    ProductID INT IDENTITY PRIMARY KEY,
    Name VARCHAR(100),
    Category VARCHAR(100),
    UnitPrice DECIMAL(10,2)
);

CREATE TABLE RawSales (
    RawSaleID INT IDENTITY PRIMARY KEY,
    CustomerName VARCHAR(100),
    ProductName VARCHAR(100),
    Quantity INT,
    Price DECIMAL(10,2),
    TotalAmount DECIMAL(10,2),
    SaleDate DATE,
    City VARCHAR(100)
);

CREATE TABLE FactSales (
    SaleID INT IDENTITY PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    Quantity INT,
    TotalAmount DECIMAL(10,2),
    SaleDate DATE
);
