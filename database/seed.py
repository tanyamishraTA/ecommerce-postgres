import random
from datetime import datetime, timedelta
from decimal import Decimal

from faker import Faker

from connection import get_connection

fake = Faker()

# Volume config 
NUM_CUSTOMERS   = 500
NUM_PRODUCTS    = 1_000
NUM_ORDERS      = 5_000
NUM_ORDER_ITEMS = 15_000
NUM_PAYMENTS    = 5_000   # 1-to-1 with orders (UNIQUE constraint on order_id)

# Domain data 
CATEGORY_NAMES = [
    "Electronics", "Clothing", "Books", "Home & Kitchen",
    "Sports & Outdoors", "Beauty & Personal Care", "Toys & Games",
    "Automotive", "Health & Wellness", "Office Supplies",
]

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled", "returned"]

PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer", "cash_on_delivery"]

PAYMENT_STATUSES = ["pending", "completed", "failed", "refunded"]


def random_date(start_days_ago: int = 730, end_days_ago: int = 0) -> datetime:
    """Return a random datetime between `start_days_ago` and `end_days_ago` ago."""
    start = datetime.now() - timedelta(days=start_days_ago)
    end   = datetime.now() - timedelta(days=end_days_ago)
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


# Seed functions

def seed_categories(cur) -> list[int]:
    print(f"  Seeding {len(CATEGORY_NAMES)} categories …")
    ids = []
    for name in CATEGORY_NAMES:
        cur.execute(
            "INSERT INTO categories (category_name) VALUES (%s) RETURNING category_id;",
            (name,)
        )
        ids.append(cur.fetchone()[0])
    print(f"  {len(ids)} categories inserted.")
    return ids


def seed_customers(cur) -> list[int]:
    print(f"  Seeding {NUM_CUSTOMERS} customers …")
    ids = []
    emails_seen: set[str] = set()
    phones_seen: set[str] = set()

    while len(ids) < NUM_CUSTOMERS:
        # Guarantee uniqueness for email & phone
        email = fake.unique.email()
        # Generate a phone that fits VARCHAR(15) and is unique
        phone = fake.numerify("##########")   # 10-digit numeric string
        while phone in phones_seen:
            phone = fake.numerify("##########")
        phones_seen.add(phone)

        cur.execute(
            """
            INSERT INTO customers (first_name, last_name, email, phone, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING customer_id;
            """,
            (
                fake.first_name(),
                fake.last_name(),
                email,
                phone,
                random_date(730, 0),
            )
        )
        ids.append(cur.fetchone()[0])

    print(f"  {len(ids)} customers inserted.")
    return ids


def seed_products(cur, category_ids: list[int]) -> list[tuple[int, Decimal]]:
    """Return list of (product_id, price) tuples for use in order_items."""
    print(f"  Seeding {NUM_PRODUCTS} products …")
    products = []

    for _ in range(NUM_PRODUCTS):
        price = round(random.uniform(1.99, 999.99), 2)
        cur.execute(
            """
            INSERT INTO products (category_id, product_name, price, stock, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING product_id;
            """,
            (
                random.choice(category_ids),
                fake.catch_phrase()[:150],       # keep within VARCHAR(150)
                price,
                random.randint(0, 500),
                random_date(730, 0),
            )
        )
        pid = cur.fetchone()[0]
        products.append((pid, Decimal(str(price))))

    print(f"  {len(products)} products inserted.")
    return products


def seed_orders(cur, customer_ids: list[int]) -> list[tuple[int, str]]:
    """Return list of (order_id, status) so we can skip cancelled orders for payment."""
    print(f"  Seeding {NUM_ORDERS} orders …")
    orders = []

    for _ in range(NUM_ORDERS):
        status = random.choice(ORDER_STATUSES)
        order_date = random_date(720, 0)
        cur.execute(
            """
            INSERT INTO orders (customer_id, order_date, status, total_amount)
            VALUES (%s, %s, %s, %s)
            RETURNING order_id;
            """,
            (
                random.choice(customer_ids),
                order_date,
                status,
                0,          # will be updated after order_items are inserted
            )
        )
        oid = cur.fetchone()[0]
        orders.append((oid, status))

    print(f"  {len(orders)} orders inserted.")
    return orders


def seed_order_items(
    cur,
    orders: list[tuple[int, str]],
    products: list[tuple[int, Decimal]],
) -> dict[int, Decimal]:
    """
    Distribute NUM_ORDER_ITEMS across all orders.
    Returns a dict mapping order_id → computed total_amount.
    """
    print(f"  Seeding {NUM_ORDER_ITEMS} order items …")

    order_ids = [o[0] for o in orders]
    # Pre-assign item counts so total sums to NUM_ORDER_ITEMS
    counts = [1] * len(order_ids)
    remaining = NUM_ORDER_ITEMS - len(order_ids)
    for _ in range(remaining):
        counts[random.randint(0, len(counts) - 1)] += 1

    order_totals: dict[int, Decimal] = {}
    total_inserted = 0

    for order_id, item_count in zip(order_ids, counts):
        running_total = Decimal("0.00")
        # Avoid duplicate products in the same order
        chosen_products = random.sample(products, min(item_count, len(products)))

        for prod_id, prod_price in chosen_products:
            quantity = random.randint(1, 10)
            item_price = prod_price
            cur.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s);
                """,
                (order_id, prod_id, quantity, float(item_price))
            )
            running_total += item_price * quantity
            total_inserted += 1

        order_totals[order_id] = running_total

    print(f"  {total_inserted} order items inserted.")
    return order_totals


def update_order_totals(cur, order_totals: dict[int, Decimal]) -> None:
    print(f"  Updating order total_amounts …")
    for order_id, total in order_totals.items():
        cur.execute(
            "UPDATE orders SET total_amount = %s WHERE order_id = %s;",
            (float(total), order_id)
        )
    print(f"  {len(order_totals)} order totals updated.")


def seed_payments(
    cur,
    orders: list[tuple[int, str]],
    order_totals: dict[int, Decimal],
) -> None:
    """
    payments.order_id has a UNIQUE constraint → exactly one payment per order.
    We create a payment for every order (NUM_PAYMENTS == NUM_ORDERS).
    Cancelled/returned orders get a 'refunded' or 'failed' payment status.
    """
    print(f"  Seeding {NUM_PAYMENTS} payments …")
    inserted = 0

    for order_id, order_status in orders:
        # Derive a realistic payment status from the order status
        if order_status == "cancelled":
            pay_status = random.choice(["failed", "refunded"])
        elif order_status == "returned":
            pay_status = "refunded"
        elif order_status == "pending":
            pay_status = "pending"
        else:
            pay_status = "completed"

        amount = order_totals.get(order_id, Decimal("0.00"))
        payment_date = random_date(700, 0)

        cur.execute(
            """
            INSERT INTO payments (order_id, payment_method, payment_status, payment_date, amount)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (
                order_id,
                random.choice(PAYMENT_METHODS),
                pay_status,
                payment_date,
                float(amount),
            )
        )
        inserted += 1

    print(f"  {inserted} payments inserted.")


# Main 
def main() -> None:
    print("Connecting to database …")
    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()

    try:
        print("\n Truncating existing data ")
        # Truncate in reverse FK dependency order and restart sequences
        cur.execute("""
            TRUNCATE TABLE payments, order_items, orders, products, customers, categories
            RESTART IDENTITY CASCADE;
        """)

        print("\n Inserting seed data")
        category_ids = seed_categories(cur)
        customer_ids = seed_customers(cur)
        products     = seed_products(cur, category_ids)
        orders       = seed_orders(cur, customer_ids)
        order_totals = seed_order_items(cur, orders, products)

        update_order_totals(cur, order_totals)
        seed_payments(cur, orders, order_totals)

        conn.commit()
        print("\n  Seed completed successfully!\n")

        # Quick row-count verification 
        print("Row counts ")
        for table in ("categories", "customers", "products", "orders", "order_items", "payments"):
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]
            print(f" {table:<20} {count:>6} rows")
        print()

    except Exception as exc:
        conn.rollback()
        print(f"\n  Seed failed — rolled back. Error: {exc}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
