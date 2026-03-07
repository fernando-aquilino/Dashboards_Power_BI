WITH sales AS (
    SELECT
        o.OrderID,
        o.OrderDate,
        c.CustomerID,
        c.CustomerName,
        e.EmployeeID,
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
),
product_revenue AS (
    SELECT
        ProductID,
        ProductName,
        ROUND(SUM(Revenue), 2) AS Total_Revenue
    FROM sales
    GROUP BY ProductID, ProductName
),
product_metrics AS (
    SELECT
        ProductID,
        ProductName,
        Total_Revenue,
        ROUND(
            100.0 * Total_Revenue / SUM(Total_Revenue) OVER (),
            2
        ) AS Revenue_Share,
        ROUND(
            100.0 * SUM(Total_Revenue) OVER (ORDER BY Total_Revenue DESC)
            / SUM(Total_Revenue) OVER (),
            2
        ) AS Cumulative_Share
    FROM product_revenue
)
SELECT
    ProductID,
    ProductName,
    Total_Revenue,
    Revenue_Share,
    Cumulative_Share,
    CASE
        WHEN Cumulative_Share <= 80 THEN 'Top 80% Revenue Group'
        ELSE 'Bottom 20% Revenue Group'
    END AS Pareto_Group
FROM product_metrics
ORDER BY Total_Revenue DESC;