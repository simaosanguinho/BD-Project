-- Query 01 - name clients who have placed orders for products with price > 5000    
SELECT customer_name
FROM Customer
WHERE cust_no IN
    (SELECT cust_no
    FROM Order_
    WHERE order_no IN
        (SELECT order_no
        FROM contains_
        WHERE sku IN
            (SELECT sku
            FROM Product
            WHERE price > 5000)));  

()

