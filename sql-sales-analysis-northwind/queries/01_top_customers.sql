WITH sales AS (
    SELECT
        o.OrderID,
        o.OrderDate,
        c.CustomerID,
        c.CustomerName,
        e.FirstName || ' ' || e.LastName AS EmployeeName,
        p.ProductID,
        p.ProductName,
        cat.CategoryName,
        od.Quantity,
        p.Price,
        od.Quantity * p.Price AS Revenue
    FROM Orders o
    JOIN Customers c
        ON o.CustomerID = c.CustomerID
    JOIN Employees e
        ON o.EmployeeID = e.EmployeeID
    JOIN OrderDetails od
        ON o.OrderID = od.OrderID
    JOIN Products p
        ON od.ProductID = p.ProductID
    JOIN Categories cat
        ON p.CategoryID = cat.CategoryID
)
SELECT
    CustomerID,
    CustomerName,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    COUNT(DISTINCT OrderID) AS Number_of_Orders,
    ROUND(SUM(Revenue) * 1.0 / COUNT(DISTINCT OrderID), 2) AS Average_Ticket
FROM sales
GROUP BY CustomerID, CustomerName
ORDER BY Total_Revenue DESC
LIMIT 10;