-- Display every order along with the customer who placed it. (INNER JOIN)
SELECT o.order_id, c.customer_id, c.first_name, c.last_name, o.order_date, o.status, o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id
ORDER BY o.order_id;

-- Show every customer, including customers who have never placed an order. (LEFT JOIN)
SELECT c.customer_id, c.first_name, c.last_name, o.order_id, o.order_date, o.status
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id
ORDER BY c.customer_id;

-- Show every order together with its customer. (RIGHT JOIN)
SELECT c.customer_id, c.first_name, o.order_id, o.status
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id
ORDER BY o.order_id;

-- Display every customer and every order, even if there is no matching record. (FULL OUTER JOIN)
SELECT c.customer_id, c.first_name, o.order_id, o.status
FROM customers c
FULL OUTER JOIN orders o
ON c.customer_id = o.customer_id
ORDER BY c.customer_id NULLS LAST;

-- Display complete order details. (Multiple INNER JOIN)
SELECT o.order_id, c.first_name, p.product_name, oi.quantity, oi.price, (oi.quantity * oi.price) AS item_total
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id
INNER JOIN order_items oi
ON o.order_id = oi.order_id
INNER JOIN products p
ON oi.product_id = p.product_id
ORDER BY o.order_id;