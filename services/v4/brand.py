from schemas.brand import Brand, Brands
from .http import HttpService
from services.staticfile import StaticFileService


class BrandService:

    BRANDS_KEY = "brands_v4.json"

    @classmethod
    async def update_brands_cache(cls) -> None:
        brands: list[Brand] = []
        raw_brands = await HttpService.get_brands_from_source()
        for b in raw_brands:
            b["illustrate"] = ''
            b["reward"] = '0%'
            b["small_logo"] = i if (i := b.get("transparency_logo_image")) != "None" else None
            b["large_logo"] = i if (i := b.get("white_logo_image")) != "None" else None
            b["is_online"] = str(b["is_online"]).lower()
            brands.append(Brand(**b))

        StaticFileService.write_file(cls.BRANDS_KEY, Brands(brands=brands).json(ensure_ascii=False))

    @classmethod
    async def update_staticfiles(cls):
        await cls.update_brands_cache()
