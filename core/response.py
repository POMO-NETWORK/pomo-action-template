import typing
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask

"""
Return response class directly is faster than let FastAPI serialize arbitrary object to json.

Reference: https://fastapi.tiangolo.com/advanced/custom-response/#use-orjsonresponse
"""


class JsonResponse(JSONResponse):
    """
    Pydantic compatible json response class.

    For further performance improvements, we could change json encoder to orjson, which trade memory for speed.
    """
    def __init__(
        self,
        content: typing.Any,
        status_code: int = 200,
        headers: typing.Optional[typing.Dict[str, str]] = None,
        media_type: typing.Optional[str] = None,
        background: typing.Optional[BackgroundTask] = None,
        dump: bool = True,
    ) -> None:
        self.dump = dump
        super().__init__(content, status_code, headers, media_type, background)

    def render(self, content: typing.Any) -> bytes:
        if self.dump:
            if isinstance(content, BaseModel):
                return content.json(
                    by_alias=True,
                    ensure_ascii=False,
                    allow_nan=False,
                    indent=None,
                    separators=(",", ":"),
                ).encode(self.charset)
            return super().render(content)
        else:
            return super(JSONResponse, self).render(content)
