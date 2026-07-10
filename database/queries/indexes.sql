-- Composite Index 1
-- Table: orders
-- Purpose: Optimize queries that search orders by customer and date.

CREATE INDEX idx_orders_customer_date
ON orders (customer_id, order_date);



-- Composite Index 2
-- Table: products
-- Purpose: Optimize queries filtering products by category and price.

CREATE INDEX idx_products_category_price
ON products (category_id, price);