from database.connection import get_connection


def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                o.order_id,
                c.customer_id,
                c.first_name,
                c.last_name,
                o.order_date,
                o.status,
                o.total_amount
            FROM orders o
            INNER JOIN customers c
                ON o.customer_id = c.customer_id
            ORDER BY o.order_id;
        """)

        rows = cursor.fetchall()

        orders = []

        for row in rows:
            orders.append({
                "order_id": row[0],
                "customer_id": row[1],
                "customer_name": f"{row[2]} {row[3]}",
                "order_date": row[4],
                "status": row[5],
                "total_amount": float(row[6])
            })

        return orders

    finally:
        cursor.close()
        conn.close()