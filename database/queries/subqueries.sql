-- Query 1: Customers Who Have Placed Orders (IN)
SELECT * FROM customers
WHERE customer_id IN (
SELECT customer_id FROM orders
);

-- Query 2: Customers With No Orders (NOT EXISTS)
SELECT * FROM customers c
WHERE NOT EXISTS (
SELECT 1 FROM orders o
WHERE o.customer_id = c.customer_id
);

-- Query 3: Products Never Ordered (NOT EXISTS)
SELECT * FROM products p
WHERE NOT EXISTS (
SELECT 1 FROM order_items oi
WHERE oi.product_id = p.product_id
);

-- Query 4: Orders Above Average Order Value (Scalar Subquery)
SELECT * FROM orders
WHERE total_amount >
(SELECT AVG(total_amount) FROM orders
);

-- Query 5: Most Expensive Product in Each Category (Correlated Subquery)
SELECT p.product_name, p.category_id, p.price
FROM products p
WHERE price =
( SELECT MAX(price) FROM products
WHERE category_id = p.category_id
);