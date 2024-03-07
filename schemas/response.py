from pydantic import BaseModel
from typing import Optional, Any, Union


class Response(BaseModel):
    message: Optional[Any] = None


class ValidationError(BaseModel):
    loc: list[Union[str, int]]
    msg: str
    type: str


class ValidationErrorResponse(Response):
    message: list[ValidationError]
