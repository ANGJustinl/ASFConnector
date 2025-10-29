class ASFConnectorError(Exception):
    """Base exception for all ASFConnector errors."""

    default_message = "ASFConnector encountered an error"

    def __init__(self, message=None, *, status_code=None, payload=None):
        if message is None:
            message = self.default_message
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload

    def __repr__(self):
        status = f" status_code={self.status_code}" if self.status_code is not None else ""
        return f"<{self.__class__.__name__}{status} message={self.args[0]!r}>"


class ASFIPCError(ASFConnectorError):
    """Base exception for ASF IPC communication errors."""

    default_message = "ASF IPC communication error"


class ASFHTTPError(ASFIPCError):
    """Base exception for ASF IPC HTTP errors."""

    default_message = "ASF IPC HTTP error"


class ASFNetworkError(ASFIPCError):
    """Exception raised for transport-level errors while talking to ASF IPC."""

    default_message = "Network error while communicating with ASF IPC"


class ASF_BadRequest(ASFHTTPError):
    default_message = "Bad request"


class ASF_Unauthorized(ASFHTTPError):
    default_message = "Unauthorized request"


class ASF_Forbidden(ASFHTTPError):
    default_message = "Forbidden request"


class ASF_NotFound(ASFHTTPError):
    default_message = "Requested resource not found"


class ASF_NotAllowed(ASFHTTPError):
    default_message = "Method not allowed"


class ASF_NotAcceptable(ASFHTTPError):
    default_message = "Requested format not acceptable"


class ASF_LengthRequired(ASFHTTPError):
    default_message = "Content-Length header required"


class ASF_NotImplemented(ASFHTTPError):
    default_message = "Requested functionality not implemented"


HTTP_STATUS_EXCEPTION_MAP = {
    400: ASF_BadRequest,
    401: ASF_Unauthorized,
    403: ASF_Forbidden,
    404: ASF_NotFound,
    405: ASF_NotAllowed,
    406: ASF_NotAcceptable,
    411: ASF_LengthRequired,
    501: ASF_NotImplemented,
}


__all__ = [
    "ASFConnectorError",
    "ASFIPCError",
    "ASFHTTPError",
    "ASFNetworkError",
    "ASF_BadRequest",
    "ASF_Unauthorized",
    "ASF_Forbidden",
    "ASF_NotFound",
    "ASF_NotAllowed",
    "ASF_NotAcceptable",
    "ASF_LengthRequired",
    "ASF_NotImplemented",
    "HTTP_STATUS_EXCEPTION_MAP",
]
