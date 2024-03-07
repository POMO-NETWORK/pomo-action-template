from pydantic import BaseModel, AnyHttpUrl, validator

from schemas.utils import empty_string_to_null


class Service(BaseModel):
    point: bool
    ticket: bool
    nft: bool


class Website(BaseModel):
    name: str

    # fixme
    url: AnyHttpUrl | str
    type: str
    # id: str = Field(alias="website_id")

    # @validator("url", pre=True)
    # def empty_string_to_none(cls, v: str) -> str | None:
    #     return empty_string_to_null(v)


class BrandInfo(BaseModel):
    id: str
    name: str


class Brand(BrandInfo):

    code: str
    type: str
    alias: str

    eshop_name: str = ""
    eshop_url: str = ""
    foodpanda_url: str | None
    facebook_fanpage_url: str | None
    line_official_account: str | None

    intro: str
    about: str
    small_logo: AnyHttpUrl | None
    large_logo: AnyHttpUrl | None
    # white_logo_image: AnyHttpUrl
    # transparency_logo_image: AnyHttpUrl
    banner_url: AnyHttpUrl | str
    illustrate: str

    subbrands_img: str | None

    # fixme
    # is_online: bool
    is_online: str
    reward: str

    website_list: list[Website]
    service_list: Service
    tag_list: list = []
    news_list: list

    @validator("small_logo", "large_logo", pre=True)
    def empty_string_to_none(cls, v: str | None) -> str | None:
        return empty_string_to_null(v)


class Brands(BaseModel):
    brands: list[Brand]
