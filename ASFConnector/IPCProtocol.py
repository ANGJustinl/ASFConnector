# 25.10.28 Modified by angjustinl from dmcallejo/ASFBot/IPCProtocol
# source code at https://github.com/dmcallejo/ASFBot/IPCProtocol

import re

import httpx
from loguru import logger

from . import error


class IPCProtocolHandler:
    AUTH_HEADER = "Authentication"
    _DEFAULT_HEADERS = {  # noqa
        "user-agent": "ASFBot",
        "Accept": "application/json",
    }

    def __init__(self, host, port, path="/", password=None):
        self.base_url = "http://" + host + ":" + port + path
        self.headers = self._DEFAULT_HEADERS.copy()
        if password:
            self.headers[self.AUTH_HEADER] = password
        self._client = None
        logger.debug(f"Initialized. Host: {self.base_url}")

    async def __aenter__(self):
        """Support async context manager for connection pool reuse"""
        self._client = httpx.AsyncClient(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the client when exiting context"""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_client(self):
        """Get or create AsyncClient instance"""
        if self._client is None:
            # For backward compatibility, create a temporary client
            return httpx.AsyncClient(headers=self.headers)
        return self._client

    async def get(self, resource, parameters=None):
        if parameters is None:
            parameters = {}
        if not isinstance(parameters, dict):
            message = '"parameters" variable must be a dictionary'
            logger.error(message)
            raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        logger.debug(f"Requesting {url} with parameters {parameters}")

        # Use reusable client if available, otherwise create temporary one
        if self._client:
            client = self._client
            should_close = False
        else:
            client = httpx.AsyncClient(headers=self.headers)
            should_close = True

        try:
            response = await client.get(url, params=parameters)
            response.raise_for_status()
            logger.debug(f"{response.url}")
            logger.debug(f"{response.json()}")
            return response.json()
        except httpx.HTTPError as ex:
            logger.error(f"Error Requesting {url} with parameters {parameters}")
            logger.exception(ex)
            raise_asf_exception(ex)
        finally:
            if should_close:
                await client.aclose()

    async def post(self, resource, payload=None):
        if payload:
            if not isinstance(payload, dict):
                message = '"payload" must be a dictionary'
                logger.error(message)
                raise TypeError(message)
        url = self.base_url + resource  # TODO: refactor
        logger.debug(f"Requesting {url} with payload {payload}")

        # Use reusable client if available, otherwise create temporary one
        if self._client:
            client = self._client
            should_close = False
        else:
            client = httpx.AsyncClient(headers=self.headers)
            should_close = True

        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.debug(f"{response.url}")
            logger.debug(f"{response.json()}")
            return response.json()
        except httpx.HTTPError as ex:
            logger.error(f"Error Requesting {url} with payload {payload}")
            logger.exception(ex)
            raise_asf_exception(ex)
        finally:
            if should_close:
                await client.aclose()

    async def delete(self, resource, parameters=None):
        if parameters is None:
            parameters = {}
        if not isinstance(parameters, dict):
            message = '"parameters" variable must be a dictionary'
            logger.error(message)
            raise TypeError(message)
        url = self.base_url + resource
        logger.debug(f"Requesting DELETE {url} with parameters {parameters}")

        if self._client:
            client = self._client
            should_close = False
        else:
            client = httpx.AsyncClient(headers=self.headers)
            should_close = True

        try:
            response = await client.delete(url, params=parameters)
            response.raise_for_status()
            logger.debug(f"{response.url}")
            logger.debug(f"{response.json()}")
            return response.json()
        except httpx.HTTPError as ex:
            logger.error(f"Error DELETE {url} with parameters {parameters}")
            logger.exception(ex)
            raise_asf_exception(ex)
        finally:
            if should_close:
                await client.aclose()


def _safe_response_payload(response: httpx.Response):
    """Extract response payload safely, trying JSON first, then text."""
    try:
        return response.json()
    except ValueError:
        text = response.text.strip()
        return text or None


def extract_reason_from_exception(ex: Exception):
    """Extract human-readable error message from an exception."""
    if isinstance(ex, httpx.HTTPStatusError):
        response = ex.response
        if response is not None:
            try:
                data = response.json()
                for key in ("Message", "message", "Error", "error", "detail"):
                    if key in data:
                        return str(data[key])
            except ValueError:
                text = response.text.strip()
                if text:
                    return text
            return f"HTTP {response.status_code}"
    if isinstance(ex, httpx.RequestError):
        return str(ex)
    if len(ex.args) > 0:
        ex_args = ex.args[0]
        if isinstance(ex_args, Exception):
            ex_reason = ex_args.reason
            return extract_reason_from_exception(ex_reason)
        match = re.match("(^.*0x\\w+>:\\s+)?(?P<reason>.*)$", str(ex_args))
        if match:
            return match.group("reason")
    return str(ex)


def raise_asf_exception(ex: httpx.HTTPError):
    """
    Convert httpx exceptions to ASFConnector exceptions and raise them.

    Args:
        ex: The httpx exception to convert

    Raises:
        ASFNetworkError: For network/connection errors
        ASF_* exceptions: For specific HTTP status codes (400, 401, 403, etc.)
        ASFHTTPError: For other HTTP errors
        ASFIPCError: For other IPC errors
    """
    status_code = None
    response_payload = None

    if isinstance(ex, httpx.HTTPStatusError) and ex.response is not None:
        status_code = ex.response.status_code
        response_payload = _safe_response_payload(ex.response)
        exception_cls = error.HTTP_STATUS_EXCEPTION_MAP.get(status_code, error.ASFHTTPError)
    elif isinstance(ex, httpx.RequestError):
        exception_cls = error.ASFNetworkError
    else:
        exception_cls = error.ASFIPCError

    message = extract_reason_from_exception(ex)
    asf_exception = exception_cls(message, status_code=status_code, payload=response_payload)

    raise asf_exception from ex


def build_error_payload(ex: httpx.HTTPError):
    """
    Build an error payload dictionary from an httpx exception.

    This is kept for backward compatibility and debugging purposes.
    New code should use raise_asf_exception() instead to properly propagate exceptions.

    Args:
        ex: The httpx exception to convert

    Returns:
        dict: Error information dictionary
    """
    status_code = None
    response_payload = None

    if isinstance(ex, httpx.HTTPStatusError) and ex.response is not None:
        status_code = ex.response.status_code
        response_payload = _safe_response_payload(ex.response)
        exception_cls = error.HTTP_STATUS_EXCEPTION_MAP.get(status_code, error.ASFHTTPError)
    elif isinstance(ex, httpx.RequestError):
        exception_cls = error.ASFNetworkError
    else:
        exception_cls = error.ASFIPCError

    message = extract_reason_from_exception(ex)
    asf_exception = exception_cls(message, status_code=status_code, payload=response_payload)

    payload = {
        "Success": False,
        "Message": message,
        "ExceptionType": asf_exception.__class__.__name__,
        "Exception": asf_exception,
    }

    if status_code is not None:
        payload["StatusCode"] = status_code
    if response_payload is not None:
        payload["ResponsePayload"] = response_payload

    return payload
