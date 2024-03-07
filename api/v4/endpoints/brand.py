from fastapi.responses import FileResponse
from api.config import responses
from core.config import settings
from core.response import JsonResponse
from core.router import get_router
from schemas.brand import Brands
from schemas.point_rules import BrandPointRules
from services.v4.brand import BrandService

router = get_router()


@router.get("/all", responses=responses, response_model=Brands)
async def get_brands():
    return FileResponse(
        settings.PROJECT_ROOT / settings.STATIC_ROOT / BrandService.BRANDS_KEY
    )


@router.get("/point_rules", responses=responses, response_model=BrandPointRules)
async def get_point_rules():
    return JsonResponse(BrandPointRules(brand_rules=[]))


@router.put("/staticfiles", responses=responses)
async def update_staticfiles():
    await BrandService.update_staticfiles()
