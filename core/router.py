import json
import traceback
from typing import Callable, Any, Coroutine
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from core.exceptions import FatalError, HTTPException
from core.logger import Logger, LogLevel
from fastapi import APIRouter, status
from fastapi.routing import (
    Request,
    Response,
    APIRoute as Route
)


class APIRoute(Route):
    """
    Handles logging for each request.
    """

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        handler = super().get_route_handler()

        async def logging_handler(request: Request) -> Response:

            log_handle = f"{request.method} {request.url.path}"

            inputs = {}  # slightly faster than calling dict()
            if len(request.path_params) > 0:
                inputs |= {"path_params": request.path_params}
            if len(request.query_params) > 0:
                log_handle = f"{request.method} {request.url.path}?{request.url.query}"
                inputs |= {"query_params": request.query_params._dict}

            # # needs to install `python-multipart` library if use form-data
            # if len(form := await request.form()) > 0:
            #     inputs |= {"form": form}

            body = await request.body()
            if len(body) > 0:
                try:
                    inputs |= {"body": json.loads(body)}
                except json.JSONDecodeError:
                    inputs |= {"body": body}

            try:
                response = await handler(request)
                if hasattr(response, "body"):
                    try:
                        outputs = json.loads(response.body)
                    except json.JSONDecodeError:
                        outputs = response.body
                else:
                    outputs = None

                Logger.log(LogLevel.INFO, log_handle, inputs, outputs, "success", log_user=get_request_user(request))
                return response
            except RequestValidationError as e:
                Logger.log(LogLevel.WARN, log_handle, inputs, e.errors(), traceback.format_exc(),
                           log_user=get_request_user(request))
                raise e
            except ValidationError as e:
                # catch pydantic root validator errors
                Logger.log(LogLevel.WARN, log_handle, inputs, e.errors(), traceback.format_exc(),
                           log_user=get_request_user(request))
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
            except FatalError as e:
                Logger.log(LogLevel.FATAL, log_handle, inputs, e.detail, traceback.format_exc(),
                           log_user=get_request_user(request))
                raise e
            except StarletteHTTPException as e:
                Logger.log(LogLevel.ERROR, log_handle, inputs, e.detail, traceback.format_exc(),
                           log_user=get_request_user(request))
                raise e
            except Exception as e:
                Logger.log(LogLevel.ERROR, log_handle, inputs, e.args, traceback.format_exc(),
                           log_user=get_request_user(request))
                # raise any unexpected error as HTTPException thus error handler can catch
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=str(e.args)
                )

        return logging_handler


def get_request_user(request: Request) -> str:
    try:
        return request.user
    except AssertionError:
        return "system"  # default


def get_router(**kwargs: Any) -> APIRouter:
    """
    Router factory with self defined route class.
    :return: APIRouter
    """
    return APIRouter(route_class=APIRoute, **kwargs)
