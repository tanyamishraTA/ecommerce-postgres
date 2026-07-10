from fastapi import FastAPI

from backend.routes.customers import router as customer_router
from backend.routes.products import router as product_router
from backend.routes.orders import router as order_router

app = FastAPI(
    title="E-Commerce PostgreSQL API",
    description="Backend API for PostgreSQL Assignment",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
def home():
    return {
        "message": "E-Commerce PostgreSQL API is running"
    }