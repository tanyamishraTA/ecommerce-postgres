from database.connection import get_connection


def get_customer_orders(customer_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                o.order_id,
                o.order_date,
                o.status,
                o.total_amount
            FROM orders o
            WHERE o.customer_id = %s
            ORDER BY o.order_date DESC;
        """, (customer_id,))

        rows = cursor.fetchall()

        orders = []

        for row in rows:
            orders.append({
                "order_id": row[0],
                "order_date": row[1],
                "status": row[2],
                "total_amount": float(row[3])
            })

        return orders

    finally:
        cursor.close()
        conn.close()