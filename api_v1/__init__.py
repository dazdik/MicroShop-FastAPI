from fastapi import APIRouter

from .demo_auth.views import router as demo_auth_router
from .demo_auth.demo_jwt import router as demo_jwt_auth_router
from .products.views import router as product_router

demo_auth_router.include_router(demo_jwt_auth_router)
router = APIRouter()
router.include_router(product_router, prefix="/products")
router.include_router(demo_auth_router)
