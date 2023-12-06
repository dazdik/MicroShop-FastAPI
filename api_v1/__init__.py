from fastapi import APIRouter

from .products.views import router as product_router

router = APIRouter()
router.include_router(product_router, prefix="/products")
