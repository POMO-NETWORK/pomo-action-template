from pydantic import BaseModel

from schemas.brand import BrandInfo


class PointSetting(BaseModel):
    ref_type: str
    point_reward_value: int


class SellerTaxId(BaseModel):
    id: str
    seller_taxid: str
    brand_id: str


class BrandPointRule(BrandInfo):
    point_settings: list[PointSetting]
    keywords: list[list[str]]
    excluded_keywords: list[list[str]]
    seller_taxids: list[SellerTaxId]


class BrandPointRules(BaseModel):
    brand_rules: list[BrandPointRule]
