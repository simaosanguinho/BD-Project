-- Start a transaction
BEGIN;

-- Attempt to create an order without a corresponding entry in the contains table
INSERT INTO orders(order_no, cust_no, date)
VALUES (2, 456, '2023-06-10');

-- Don't add a corresponding entry in the contains table

-- Attempt to commit the transaction
COMMIT;
