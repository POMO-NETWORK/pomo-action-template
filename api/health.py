from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health", description="Health Check API")
async def health() -> str:
    return "Hello"
