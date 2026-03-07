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
    strftime('%Y-%m', OrderDate) AS Year_Month,
    ROUND(SUM(Revenue), 2) AS Monthly_Revenue,
    COUNT(DISTINCT OrderID) AS Number_of_Orders
FROM sales
GROUP BY Year_Month
ORDER BY Year_Month;