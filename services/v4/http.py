from typing import Any
from aiohttp import ClientSession

from core.config import settings
from services.http import client


class HttpService:

    @staticmethod
    async def get_brands_from_source(session: ClientSession = None) -> list[dict[str, Any]]:
        return await client.get(url=f"{settings.BRAND_SOURCE_URL}/api/brands/v1/all", session=session)
