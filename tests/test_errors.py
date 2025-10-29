"""
Tests for ASFConnector error handling and exceptions.
"""

from unittest.mock import Mock

import httpx
import pytest

from ASFConnector.error import (
    HTTP_STATUS_EXCEPTION_MAP,
    ASF_BadRequest,
    ASF_Forbidden,
    ASF_LengthRequired,
    ASF_NotAcceptable,
    ASF_NotAllowed,
    ASF_NotFound,
    ASF_NotImplemented,
    ASF_Unauthorized,
    ASFConnectorError,
    ASFHTTPError,
    ASFIPCError,
    ASFNetworkError,
)
from ASFConnector.IPCProtocol import (
    build_error_payload,
    extract_reason_from_exception,
    raise_asf_exception,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""

    def test_base_exception(self):
        """Test ASFConnectorError base exception."""
        exc = ASFConnectorError("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_exception_with_status_code(self):
        """Test exception with status code."""
        exc = ASFHTTPError("HTTP error", status_code=404)
        assert exc.status_code == 404
        assert "404" in repr(exc)

    def test_exception_with_payload(self):
        """Test exception with payload."""
        payload = {"error": "details"}
        exc = ASFHTTPError("HTTP error", status_code=400, payload=payload)
        assert exc.payload == payload

    def test_ipc_error_inheritance(self):
        """Test ASFIPCError inherits from ASFConnectorError."""
        exc = ASFIPCError("IPC error")
        assert isinstance(exc, ASFConnectorError)

    def test_http_error_inheritance(self):
        """Test ASFHTTPError inherits from ASFIPCError."""
        exc = ASFHTTPError("HTTP error")
        assert isinstance(exc, ASFIPCError)
        assert isinstance(exc, ASFConnectorError)

    def test_network_error_inheritance(self):
        """Test ASFNetworkError inherits from ASFIPCError."""
        exc = ASFNetworkError("Network error")
        assert isinstance(exc, ASFIPCError)
        assert isinstance(exc, ASFConnectorError)

    def test_specific_http_errors_inheritance(self):
        """Test specific HTTP error classes inherit from ASFHTTPError."""
        assert isinstance(ASF_BadRequest("test"), ASFHTTPError)
        assert isinstance(ASF_Unauthorized("test"), ASFHTTPError)
        assert isinstance(ASF_Forbidden("test"), ASFHTTPError)
        assert isinstance(ASF_NotFound("test"), ASFHTTPError)
        assert isinstance(ASF_NotAllowed("test"), ASFHTTPError)
        assert isinstance(ASF_NotAcceptable("test"), ASFHTTPError)
        assert isinstance(ASF_LengthRequired("test"), ASFHTTPError)
        assert isinstance(ASF_NotImplemented("test"), ASFHTTPError)


class TestHTTPStatusExceptionMap:
    """Test HTTP status code to exception mapping."""

    def test_status_map_completeness(self):
        """Test that all expected status codes are mapped."""
        expected_statuses = [400, 401, 403, 404, 405, 406, 411, 501]
        for status in expected_statuses:
            assert status in HTTP_STATUS_EXCEPTION_MAP

    def test_status_map_400(self):
        """Test 400 maps to ASF_BadRequest."""
        assert HTTP_STATUS_EXCEPTION_MAP[400] == ASF_BadRequest

    def test_status_map_401(self):
        """Test 401 maps to ASF_Unauthorized."""
        assert HTTP_STATUS_EXCEPTION_MAP[401] == ASF_Unauthorized

    def test_status_map_403(self):
        """Test 403 maps to ASF_Forbidden."""
        assert HTTP_STATUS_EXCEPTION_MAP[403] == ASF_Forbidden

    def test_status_map_404(self):
        """Test 404 maps to ASF_NotFound."""
        assert HTTP_STATUS_EXCEPTION_MAP[404] == ASF_NotFound

    def test_status_map_405(self):
        """Test 405 maps to ASF_NotAllowed."""
        assert HTTP_STATUS_EXCEPTION_MAP[405] == ASF_NotAllowed

    def test_status_map_406(self):
        """Test 406 maps to ASF_NotAcceptable."""
        assert HTTP_STATUS_EXCEPTION_MAP[406] == ASF_NotAcceptable

    def test_status_map_411(self):
        """Test 411 maps to ASF_LengthRequired."""
        assert HTTP_STATUS_EXCEPTION_MAP[411] == ASF_LengthRequired

    def test_status_map_501(self):
        """Test 501 maps to ASF_NotImplemented."""
        assert HTTP_STATUS_EXCEPTION_MAP[501] == ASF_NotImplemented


class TestExtractReasonFromException:
    """Test extract_reason_from_exception function."""

    def test_extract_from_http_status_error_with_json(self):
        """Test extracting reason from HTTPStatusError with JSON response."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"Message": "Not found"}
        mock_response.text = ""

        exc = httpx.HTTPStatusError("404 Not Found", request=Mock(), response=mock_response)

        reason = extract_reason_from_exception(exc)
        assert reason == "Not found"

    def test_extract_from_http_status_error_with_text(self):
        """Test extracting reason from HTTPStatusError with text response."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "Internal Server Error"

        exc = httpx.HTTPStatusError("500 Server Error", request=Mock(), response=mock_response)

        reason = extract_reason_from_exception(exc)
        assert reason == "Internal Server Error"

    def test_extract_from_request_error(self):
        """Test extracting reason from RequestError."""
        exc = httpx.RequestError("Connection timeout")
        reason = extract_reason_from_exception(exc)
        assert "Connection timeout" in reason

    def test_extract_from_generic_exception(self):
        """Test extracting reason from generic exception."""
        exc = Exception("Generic error message")
        reason = extract_reason_from_exception(exc)
        assert "Generic error message" in reason


class TestRaiseASFException:
    """Test raise_asf_exception function."""

    def test_raise_network_error_for_request_error(self):
        """Test that RequestError raises ASFNetworkError."""
        exc = httpx.RequestError("Connection failed")

        with pytest.raises(ASFNetworkError) as exc_info:
            raise_asf_exception(exc)

        assert "Connection failed" in str(exc_info.value)

    def test_raise_specific_http_error_400(self):
        """Test that 400 status raises ASF_BadRequest."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"Message": "Bad request"}
        mock_response.text = ""

        exc = httpx.HTTPStatusError("400 Bad Request", request=Mock(), response=mock_response)

        with pytest.raises(ASF_BadRequest) as exc_info:
            raise_asf_exception(exc)

        assert exc_info.value.status_code == 400

    def test_raise_specific_http_error_404(self):
        """Test that 404 status raises ASF_NotFound."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"Message": "Not found"}
        mock_response.text = ""

        exc = httpx.HTTPStatusError("404 Not Found", request=Mock(), response=mock_response)

        with pytest.raises(ASF_NotFound) as exc_info:
            raise_asf_exception(exc)

        assert exc_info.value.status_code == 404

    def test_raise_generic_http_error_for_unmapped_status(self):
        """Test that unmapped status codes raise ASFHTTPError."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"Message": "Server error"}
        mock_response.text = ""

        exc = httpx.HTTPStatusError("500 Server Error", request=Mock(), response=mock_response)

        with pytest.raises(ASFHTTPError) as exc_info:
            raise_asf_exception(exc)

        assert exc_info.value.status_code == 500
        assert not isinstance(exc_info.value, ASF_NotFound)

    def test_raise_ipc_error_for_other_exceptions(self):
        """Test that other httpx errors raise ASFIPCError."""
        exc = httpx.HTTPError("Generic HTTP error")

        with pytest.raises(ASFIPCError):
            raise_asf_exception(exc)


class TestBuildErrorPayload:
    """Test build_error_payload function."""

    def test_build_payload_from_http_status_error(self):
        """Test building error payload from HTTPStatusError."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"Message": "Resource not found"}
        mock_response.text = ""

        exc = httpx.HTTPStatusError("404 Not Found", request=Mock(), response=mock_response)

        payload = build_error_payload(exc)

        assert payload["Success"] is False
        assert payload["Message"] == "Resource not found"
        assert payload["StatusCode"] == 404
        assert payload["ExceptionType"] == "ASF_NotFound"
        assert isinstance(payload["Exception"], ASF_NotFound)
        assert payload["ResponsePayload"] == {"Message": "Resource not found"}

    def test_build_payload_from_request_error(self):
        """Test building error payload from RequestError."""
        exc = httpx.RequestError("Network unreachable")

        payload = build_error_payload(exc)

        assert payload["Success"] is False
        assert "Network unreachable" in payload["Message"]
        assert payload["ExceptionType"] == "ASFNetworkError"
        assert isinstance(payload["Exception"], ASFNetworkError)
        assert "StatusCode" not in payload

    def test_build_payload_preserves_response_payload(self):
        """Test that response payload is preserved in error payload."""
        response_data = {"error": "details", "code": 123}
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = response_data
        mock_response.text = ""

        exc = httpx.HTTPStatusError("400 Bad Request", request=Mock(), response=mock_response)

        payload = build_error_payload(exc)

        assert payload["ResponsePayload"] == response_data


class TestDefaultMessages:
    """Test default error messages for exception classes."""

    def test_default_messages_set(self):
        """Test that all exception classes have default messages."""
        exceptions_to_test = [
            ASFConnectorError,
            ASFIPCError,
            ASFHTTPError,
            ASFNetworkError,
            ASF_BadRequest,
            ASF_Unauthorized,
            ASF_Forbidden,
            ASF_NotFound,
            ASF_NotAllowed,
            ASF_NotAcceptable,
            ASF_LengthRequired,
            ASF_NotImplemented,
        ]

        for exc_class in exceptions_to_test:
            exc = exc_class()
            assert str(exc) != ""
            assert str(exc) == exc_class.default_message
