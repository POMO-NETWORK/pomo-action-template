from .brand import BrandService


async def prepare_staticfiles():
    await BrandService.update_brands_cache()
