from schemas.response import Response, ValidationErrorResponse


# Basic possible responses for each request
responses = {
    400: {"model": Response},
    404: {"model": Response},
    422: {"model": ValidationErrorResponse},
    500: {"model": Response},
}
