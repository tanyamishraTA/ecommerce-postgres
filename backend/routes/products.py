from fastapi import APIRouter

from backend.services.product_service import get_all_products

router = APIRouter()


@router.get("/products")
def fetch_products():
    return get_all_products()