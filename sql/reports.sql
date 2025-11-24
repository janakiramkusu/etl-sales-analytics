SELECT 
    SaleDate,
    SUM(TotalAmount) as DailySales
FROM FactSales
GROUP BY SaleDate
ORDER BY SaleDate;

SELECT 
    p.Name as Product,
    SUM(f.Quantity) as TotalQty
FROM FactSales f
JOIN Products p ON f.ProductID = p.ProductID
GROUP BY p.Name
ORDER BY TotalQty DESC;

SELECT 
    c.Name as Customer,
    SUM(f.TotalAmount) as TotalSpent
FROM FactSales f
JOIN Customers c ON f.CustomerID = c.CustomerID
GROUP BY c.Name
ORDER BY TotalSpent DESC;
