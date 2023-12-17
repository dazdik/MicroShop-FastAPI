from fastapi import APIRouter

from .products.views import router as product_router
from .demo_auth.views import router as demo_auth_router

router = APIRouter()
router.include_router(product_router, prefix="/products")
router.include_router(demo_auth_router)
