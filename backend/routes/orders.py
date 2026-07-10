from fastapi import APIRouter

from backend.services.order_service import get_all_orders

router = APIRouter()


@router.get("/orders")
def fetch_orders():
    return get_all_orders()