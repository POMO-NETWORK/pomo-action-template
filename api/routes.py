from core.router import get_router
from .health import health_router
from . import v4


root_router = get_router()


root_router.include_router(health_router, tags=["Health"])

root_router.include_router(v4.api_router, prefix="/api/v4")
