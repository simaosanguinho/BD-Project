-- Start a transaction
BEGIN;

-- Insert a product
INSERT INTO product(SKU, name, description, price, ean)
VALUES ('SKU123', 'Product Name', 'Product Description', 10.99, 1234567890123);

-- Create an order
INSERT INTO orders(order_no, cust_no, date)
VALUES (1, 123, '2023-06-10');

-- Add corresponding entry in the contains table
INSERT INTO contains(order_no, SKU, qty)
VALUES (1, 'SKU123', 10);

-- Commit the transaction
COMMIT;

-- Start a transaction
BEGIN;

-- Delete the corresponding entry from the contains table
DELETE FROM contains WHERE order_no = 1 AND SKU = 'SKU123';

-- Delete the created order
DELETE FROM orders WHERE order_no = 1;

-- Delete the inserted product
DELETE FROM product WHERE SKU = 'SKU123';

-- Commit the transaction
COMMIT;
