from database.connection import get_connection


def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                customer_id,
                first_name,
                last_name,
                email,
                phone,
                created_at
            FROM customers
            ORDER BY customer_id;
        """)

        rows = cursor.fetchall()

        customers = []

        for row in rows:
            customers.append({
                "customer_id": row[0],
                "first_name": row[1],
                "last_name": row[2],
                "email": row[3],
                "phone": row[4],
                "created_at": row[5]
            })

        return customers

    finally:
        cursor.close()
        conn.close()