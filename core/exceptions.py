from fastapi.exceptions import HTTPException as FastApiHttpException


class HTTPException(FastApiHttpException):
    """
    Base class for all exceptions raised in this app.
    """
    pass


class FatalError(HTTPException):
    """
    Raised when need to log FATAL errors.
    """
    pass
