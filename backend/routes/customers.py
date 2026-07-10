from fastapi import APIRouter

from backend.services.customer_service import get_all_customers
from backend.services.customer_order_service import get_customer_orders

router = APIRouter()


@router.get("/customers")
def fetch_customers():
    return get_all_customers()


@router.get("/customers/{customer_id}/orders")
def fetch_customer_orders(customer_id: int):
    return get_customer_orders(customer_id)