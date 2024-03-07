from core.router import get_router
from .endpoints import brand

api_router = get_router()


api_router.include_router(brand.router, prefix="/brand", tags=["Brand"])
