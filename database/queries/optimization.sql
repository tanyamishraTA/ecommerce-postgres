-- Query Optimization Example 1
-- Table: orders
-- Purpose: Optimize queries that search orders by customer and date.


-- Before Index
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 100
AND order_date >= '2025-01-01';

-- output
"Seq Scan on orders  (cost=0.00..152.00 rows=11 width=32) (actual time=0.064..0.599 rows=11.00 loops=1)"
"  Filter: ((order_date >= '2025-01-01 00:00:00'::timestamp without time zone) AND (customer_id = 100))"
"  Rows Removed by Filter: 4989"
"  Buffers: shared hit=77"
"Planning Time: 0.084 ms"
"Execution Time: 0.634 ms"


-- Create Index
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, order_date);

-- After Index
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE customer_id = 100
AND order_date >= '2025-01-01';

-- output
"Bitmap Heap Scan on orders  (cost=4.40..36.09 rows=11 width=32) (actual time=0.066..0.082 rows=11.00 loops=1)"
"  Recheck Cond: ((customer_id = 100) AND (order_date >= '2025-01-01 00:00:00'::timestamp without time zone))"
"  Heap Blocks: exact=11"
"  Buffers: shared hit=13"
"  ->  Bitmap Index Scan on idx_orders_customer_date  (cost=0.00..4.39 rows=11 width=0) (actual time=0.043..0.043 rows=11.00 loops=1)"
"        Index Cond: ((customer_id = 100) AND (order_date >= '2025-01-01 00:00:00'::timestamp without time zone))"
"        Index Searches: 1"
"        Buffers: shared hit=2"
"Planning Time: 0.128 ms"
"Execution Time: 0.135 ms"



-- Query Optimization Example 2
-- Table: products
-- Purpose: Optimize queries filtering products by category and price.


-- Before Index
EXPLAIN ANALYZE
SELECT * FROM products
WHERE category_id = 2
AND price > 500;

-- output
"Seq Scan on products  (cost=0.00..27.00 rows=41 width=60) (actual time=0.046..0.878 rows=38.00 loops=1)"
"  Filter: ((price > '500'::numeric) AND (category_id = 2))"
"  Rows Removed by Filter: 962"
"  Buffers: shared hit=12"
"Planning:"
"  Buffers: shared hit=6 dirtied=1"
"Planning Time: 0.245 ms"
"Execution Time: 0.900 ms"

-- Create Index
CREATE INDEX idx_products_category_price
ON products(category_id, price);

-- After Index
EXPLAIN ANALYZE
SELECT * FROM products
WHERE category_id = 2
AND price > 500;   

-- output
"Bitmap Heap Scan on products  (cost=4.70..17.31 rows=41 width=60) (actual time=0.032..0.049 rows=38.00 loops=1)"
"  Recheck Cond: ((category_id = 2) AND (price > '500'::numeric))"
"  Heap Blocks: exact=11"
"  Buffers: shared hit=13"
"  ->  Bitmap Index Scan on idx_products_category_price  (cost=0.00..4.69 rows=41 width=0) (actual time=0.019..0.020 rows=38.00 loops=1)"
"        Index Cond: ((category_id = 2) AND (price > '500'::numeric))"
"        Index Searches: 1"
"        Buffers: shared hit=2"
"Planning Time: 0.130 ms"
"Execution Time: 0.067 ms"
