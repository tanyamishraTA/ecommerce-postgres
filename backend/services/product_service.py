from database.connection import get_connection


def get_all_products():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                p.product_id,
                p.product_name,
                c.category_name,
                p.price,
                p.stock,
                p.created_at
            FROM products p
            INNER JOIN categories c
                ON p.category_id = c.category_id
            ORDER BY p.product_id;
        """)

        rows = cursor.fetchall()

        products = []

        for row in rows:
            products.append({
                "product_id": row[0],
                "product_name": row[1],
                "category": row[2],
                "price": float(row[3]),
                "stock": row[4],
                "created_at": row[5]
            })

        return products

    finally:
        cursor.close()
        conn.close()