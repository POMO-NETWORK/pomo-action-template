from typing import Union, Any
from aiohttp import hdrs, ClientSession, ClientConnectorError, ClientResponseError, ContentTypeError
from json import JSONDecodeError
from core.exceptions import HTTPException
from core.logger import Logger, LogLevel


class AsyncHttpClient:

    async def get(self, *, url: str, params: dict[str | int, Any] = None, session: ClientSession = None,
                  return_bytes: bool = False, **kwargs):
        return await self._do(method=hdrs.METH_GET, url=url, params=params, session=session, return_bytes=return_bytes,
                              **kwargs)

    async def post(self, *, url: str, data: Any = None, json: dict[str | int, Any] = None,
                   session: ClientSession = None, return_bytes: bool = False, **kwargs):
        return await self._do(method=hdrs.METH_POST, url=url, data=data, json=json, session=session,
                              return_bytes=return_bytes, **kwargs)

    async def put(self, *, url: str, data: Any = None, json: dict[str | int, Any] = None, return_bytes: bool = False,
                  session: ClientSession = None, **kwargs):
        return await self._do(method=hdrs.METH_PUT, url=url, data=data, json=json, session=session,
                              return_bytes=return_bytes, **kwargs)

    async def delete(self, *, url: str, session: ClientSession = None, return_bytes: bool = False, **kwargs):
        return await self._do(method=hdrs.METH_DELETE, url=url, session=session, return_bytes=return_bytes, **kwargs)

    @staticmethod
    async def _perform_request(
            *,
            method: str,
            url: str,
            params: dict[str | int, Any] = None,
            data: Any = None,
            json: dict[str | int, Any] = None,
            session: ClientSession,
            return_bytes: bool = False,
            **kwargs
    ) -> Union[str, list, dict, bytes]:
        try:
            response = await session.request(method, url, params=params, data=data, json=json, **kwargs)

            if return_bytes:
                res = await response.read()
            else:
                try:
                    res = await response.json()
                except (JSONDecodeError, ContentTypeError):
                    res = await response.text()

            try:
                response.raise_for_status()
            except ClientResponseError as e:
                raise HTTPException(status_code=e.status, detail=f"{e.message}: {res}")

            req = {
                "json": json,
                "data": data,
                "params": params
            }

            Logger.log(LogLevel.DEBUG, f"{method} {url}", req, res, "")
            return res
        except ClientConnectorError as e:
            raise HTTPException(status_code=500, detail=str(e.args))

    async def _do(
            self,
            *,
            method: str,
            url: str,
            params=None,
            data=None,
            json=None,
            session: ClientSession = None,
            **kwargs
    ):
        if session is None:
            async with ClientSession() as session:
                return await self._perform_request(method=method, url=url, data=data, params=params,
                                                   json=json, session=session, **kwargs)
        else:
            return await self._perform_request(method=method, url=url, data=data, json=json, params=params,
                                               session=session, **kwargs)


client = AsyncHttpClient()
