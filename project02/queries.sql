--Pergunta 1
SELECT name 
FROM Customer
    NATURAL JOIN Order_
    NATURAL JOIN contains_
    NATURAL JOIN (SELECT sku FROM Product WHERE price > 5000) 
                        AS product_above_50
WHERE 
    EXTRACT(YEAR FROM date) = 2023;


-- Pergunta 2

SELECT  DISTINCT name
FROM Employee
    NATURAL JOIN (SELECT order_no FROM process)
        AS processed_order
    NATURAL JOIN (SELECT date FROM Order_)
        AS order_date
    NATURAL JOIN (SELECT ssn, address FROM works) 
        AS working_employees
    NATURAL JOIN (
        (SELECT address FROM Warehouse AS w_employee)
        EXCEPT
        (SELECT address FROM Office AS o_employee)
    ) AS w_only_employees    
WHERE EXTRACT(YEAR FROM date) = 2023 
        AND EXTRACT(MONTH FROM date) = 1;


-- Pergunta 3
WITH qty_sold_by_product AS (
    SELECT sku, SUM(quantity) AS total_qty
    FROM (contains_ NATURAL JOIN Sale)
    GROUP BY sku
)
SELECT name AS most_sold
FROM Product NATURAL JOIN
    (SELECT *
    FROM qty_sold_by_product
        WHERE total_qty = (
        SELECT MAX(total_qty)
        FROM qty_sold_by_product
    )) AS most_sold_products;


-- Pergunta 4
SELECT order_no AS sale, SUM(price * quantity) AS total_value
FROM Sale
    INNER JOIN contains_ c USING (order_no)
    INNER JOIN Product USING (sku)
    GROUP BY order_no;
        