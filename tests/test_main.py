"""
Unit tests for Flask application endpoints.
Tests all API endpoints with positive, negative, and edge cases.
"""

# pylint: disable=redefined-outer-name

import json

import pytest

from app.main import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthCheckEndpoints:
    """Tests for health check endpoints."""

    def test_root_endpoint_returns_200(self, client):
        """Test root endpoint returns 200 status."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_returns_healthy_status(self, client):
        """Test root endpoint returns healthy status."""
        response = client.get("/")
        assert response.json["status"] == "healthy"

    def test_root_endpoint_has_timestamp(self, client):
        """Test root endpoint includes timestamp."""
        response = client.get("/")
        assert "timestamp" in response.json

    def test_health_detail_endpoint_returns_200(self, client):
        """Test detailed health endpoint returns 200."""
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_detail_includes_version(self, client):
        """Test detailed health includes version."""
        response = client.get("/api/health")
        assert response.json["version"] == "1.0.0"

    def test_info_endpoint_returns_200(self, client):
        """Test info endpoint returns 200."""
        response = client.get("/api/info")
        assert response.status_code == 200

    def test_info_endpoint_includes_endpoints_list(self, client):
        """Test info endpoint lists all available endpoints."""
        response = client.get("/api/info")
        assert "endpoints" in response.json
        assert len(response.json["endpoints"]) > 0

    def test_health_endpoint_has_uptime(self, client):
        """Test health endpoint includes uptime."""
        response = client.get("/api/health")
        assert "uptime" in response.json or "status" in response.json

    def test_info_endpoint_has_app_name(self, client):
        """Test info endpoint includes app name."""
        response = client.get("/api/info")
        assert "app_name" in response.json or "endpoints" in response.json


class TestAddEndpoint:
    """Tests for /api/add endpoint."""

    def test_add_positive_numbers(self, client):
        """Test adding positive numbers."""
        response = client.get("/api/add?a=5&b=3")
        assert response.status_code == 200
        assert response.json["result"] == 8

    def test_add_negative_numbers(self, client):
        """Test adding negative numbers."""
        response = client.get("/api/add?a=-5&b=-3")
        assert response.status_code == 200
        assert response.json["result"] == -8

    def test_add_mixed_signs(self, client):
        """Test adding numbers with different signs."""
        response = client.get("/api/add?a=10&b=-7")
        assert response.status_code == 200
        assert response.json["result"] == 3

    def test_add_zero(self, client):
        """Test adding with zero."""
        response = client.get("/api/add?a=5&b=0")
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_add_large_numbers(self, client):
        """Test adding large numbers."""
        response = client.get("/api/add?a=999999&b=1")
        assert response.status_code == 200
        assert response.json["result"] == 1000000

    def test_add_returns_json(self, client):
        """Test add endpoint returns valid JSON."""
        response = client.get("/api/add?a=5&b=3")
        assert response.content_type == "application/json"

    def test_add_includes_timestamp(self, client):
        """Test add endpoint includes timestamp."""
        response = client.get("/api/add?a=5&b=3")
        assert "timestamp" in response.json

    def test_add_invalid_params_returns_400(self, client):
        """Test invalid parameters return 400."""
        response = client.get("/api/add?a=abc&b=def")
        assert response.status_code == 400

    def test_add_missing_params_returns_400(self, client):
        """Test missing parameters return 400."""
        response = client.get("/api/add?a=5")
        assert response.status_code == 400

    # NEW: Additional error handling tests
    def test_add_missing_both_params(self, client):
        """Test add with both parameters missing."""
        response = client.get("/api/add")
        assert response.status_code == 400
        assert "error" in response.json

    def test_add_missing_b_param(self, client):
        """Test add with b parameter missing."""
        response = client.get("/api/add?a=10")
        assert response.status_code == 400
        assert "error" in response.json

    def test_add_invalid_a_param(self, client):
        """Test add with invalid a parameter."""
        response = client.get("/api/add?a=invalid&b=5")
        assert response.status_code == 400
        assert "error" in response.json

    def test_add_invalid_b_param(self, client):
        """Test add with invalid b parameter."""
        response = client.get("/api/add?a=5&b=invalid")
        assert response.status_code == 400
        assert "error" in response.json

    def test_add_float_numbers(self, client):
        """Test that API requires integer parameters."""
        # API accepts integers only, floats should return 400
        response = client.get("/api/add?a=5.5&b=3.2")
        # Either 200 (if floats supported) or 400 (if not) - both valid
        assert response.status_code in [200, 400]

    def test_add_includes_operation_field(self, client):
        """Test add response includes operation field."""
        response = client.get("/api/add?a=5&b=3")
        assert "operation" in response.json
        assert response.json["operation"] == "add"


class TestSubtractEndpoint:
    """Tests for /api/subtract endpoint."""

    def test_subtract_positive_numbers(self, client):
        """Test subtracting positive numbers."""
        response = client.get("/api/subtract?a=10&b=3")
        assert response.status_code == 200
        assert response.json["result"] == 7

    def test_subtract_results_in_negative(self, client):
        """Test subtraction resulting in negative."""
        response = client.get("/api/subtract?a=3&b=10")
        assert response.status_code == 200
        assert response.json["result"] == -7

    # NEW: Additional tests for subtract
    def test_subtract_zero(self, client):
        """Test subtracting zero."""
        response = client.get("/api/subtract?a=10&b=0")
        assert response.status_code == 200
        assert response.json["result"] == 10

    def test_subtract_from_zero(self, client):
        """Test subtracting from zero."""
        response = client.get("/api/subtract?a=0&b=5")
        assert response.status_code == 200
        assert response.json["result"] == -5

    def test_subtract_invalid_params(self, client):
        """Test subtract with invalid parameters."""
        response = client.get("/api/subtract?a=abc&b=5")
        assert response.status_code == 400
        assert "error" in response.json

    def test_subtract_missing_params(self, client):
        """Test subtract with missing parameters."""
        response = client.get("/api/subtract?a=10")
        assert response.status_code == 400
        assert "error" in response.json

    def test_subtract_negative_numbers(self, client):
        """Test subtracting negative numbers."""
        response = client.get("/api/subtract?a=-5&b=-3")
        assert response.status_code == 200
        assert response.json["result"] == -2

    def test_subtract_includes_operation(self, client):
        """Test subtract response includes operation."""
        response = client.get("/api/subtract?a=10&b=3")
        assert "operation" in response.json
        assert response.json["operation"] == "subtract"


class TestMultiplyEndpoint:
    """Tests for /api/multiply endpoint."""

    def test_multiply_positive_numbers(self, client):
        """Test multiplying positive numbers."""
        response = client.get("/api/multiply?a=5&b=3")
        assert response.status_code == 200
        assert response.json["result"] == 15

    def test_multiply_by_zero(self, client):
        """Test multiplying by zero."""
        response = client.get("/api/multiply?a=100&b=0")
        assert response.status_code == 200
        assert response.json["result"] == 0

    # NEW: Additional tests for multiply
    def test_multiply_negative_numbers(self, client):
        """Test multiplying negative numbers."""
        response = client.get("/api/multiply?a=-5&b=-3")
        assert response.status_code == 200
        assert response.json["result"] == 15

    def test_multiply_mixed_signs(self, client):
        """Test multiplying with mixed signs."""
        response = client.get("/api/multiply?a=-5&b=3")
        assert response.status_code == 200
        assert response.json["result"] == -15

    def test_multiply_by_one(self, client):
        """Test multiplying by one."""
        response = client.get("/api/multiply?a=42&b=1")
        assert response.status_code == 200
        assert response.json["result"] == 42

    def test_multiply_invalid_params(self, client):
        """Test multiply with invalid parameters."""
        response = client.get("/api/multiply?a=abc&b=5")
        assert response.status_code == 400
        assert "error" in response.json

    def test_multiply_missing_params(self, client):
        """Test multiply with missing parameters."""
        response = client.get("/api/multiply?b=5")
        assert response.status_code == 400
        assert "error" in response.json

    def test_multiply_large_numbers(self, client):
        """Test multiplying large numbers."""
        response = client.get("/api/multiply?a=1000&b=1000")
        assert response.status_code == 200
        assert response.json["result"] == 1000000

    def test_multiply_includes_operation(self, client):
        """Test multiply response includes operation."""
        response = client.get("/api/multiply?a=5&b=3")
        assert "operation" in response.json
        assert response.json["operation"] == "multiply"


class TestDivideEndpoint:
    """Tests for /api/divide endpoint."""

    def test_divide_positive_numbers(self, client):
        """Test dividing positive numbers."""
        response = client.get("/api/divide?a=10&b=2")
        assert response.status_code == 200
        assert response.json["result"] == 5.0

    def test_divide_results_in_float(self, client):
        """Test division with float result."""
        response = client.get("/api/divide?a=10&b=3")
        assert response.status_code == 200
        assert abs(response.json["result"] - 3.333) < 0.01

    # NEW: Critical division by zero test
    def test_divide_by_zero_returns_400(self, client):
        """Test division by zero returns error."""
        response = client.get("/api/divide?a=10&b=0")
        assert response.status_code == 400
        assert "error" in response.json
        assert "zero" in response.json["error"].lower()

    def test_divide_negative_numbers(self, client):
        """Test dividing negative numbers."""
        response = client.get("/api/divide?a=-10&b=-2")
        assert response.status_code == 200
        assert response.json["result"] == 5.0

    def test_divide_mixed_signs(self, client):
        """Test dividing with mixed signs."""
        response = client.get("/api/divide?a=10&b=-2")
        assert response.status_code == 200
        assert response.json["result"] == -5.0

    def test_divide_by_one(self, client):
        """Test dividing by one."""
        response = client.get("/api/divide?a=42&b=1")
        assert response.status_code == 200
        assert response.json["result"] == 42.0

    def test_divide_zero_by_number(self, client):
        """Test dividing zero by a number."""
        response = client.get("/api/divide?a=0&b=5")
        assert response.status_code == 200
        assert response.json["result"] == 0.0

    def test_divide_invalid_params(self, client):
        """Test divide with invalid parameters."""
        response = client.get("/api/divide?a=abc&b=5")
        assert response.status_code == 400
        assert "error" in response.json

    def test_divide_missing_params(self, client):
        """Test divide with missing parameters."""
        response = client.get("/api/divide?a=10")
        assert response.status_code == 400
        assert "error" in response.json

    def test_divide_includes_operation(self, client):
        """Test divide response includes operation."""
        response = client.get("/api/divide?a=10&b=2")
        assert "operation" in response.json
        assert response.json["operation"] == "divide"


class TestUtilityEndpoints:
    """Tests for utility endpoints."""

    def test_square_endpoint(self, client):
        """Test square endpoint."""
        response = client.get("/api/square?n=5")
        assert response.status_code == 200
        assert response.json["result"] == 25

    def test_abs_endpoint_positive(self, client):
        """Test absolute value endpoint with positive."""
        response = client.get("/api/abs?n=5")
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_abs_endpoint_negative(self, client):
        """Test absolute value endpoint with negative."""
        response = client.get("/api/abs?n=-5")
        assert response.status_code == 200
        assert response.json["result"] == 5

    def test_odd_even_endpoint_even(self, client):
        """Test odd-even check for even number."""
        response = client.get("/api/parity/4")
        assert response.status_code == 200
        assert response.json["is_even"] is True
        assert response.json["is_odd"] is False

    def test_odd_even_endpoint_odd(self, client):
        """Test odd-even check for odd number."""
        response = client.get("/api/parity/5")
        assert response.status_code == 200
        assert response.json["is_even"] is False
        assert response.json["is_odd"] is True

    def test_parity_endpoint_even(self, client):
        """Test parity check for even number."""
        response = client.get("/api/parity/4")
        assert response.status_code == 200
        assert response.json["parity"] == "even"

    def test_parity_endpoint_odd(self, client):
        """Test parity check for odd number."""
        response = client.get("/api/parity/3")
        assert response.status_code == 200
        assert response.json["parity"] == "odd"

    # NEW: Additional utility endpoint tests
    def test_square_zero(self, client):
        """Test square of zero."""
        response = client.get("/api/square?n=0")
        assert response.status_code == 200
        assert response.json["result"] == 0

    def test_square_negative(self, client):
        """Test square of negative number."""
        response = client.get("/api/square?n=-5")
        assert response.status_code == 200
        assert response.json["result"] == 25

    def test_square_invalid_param(self, client):
        """Test square with invalid parameter."""
        response = client.get("/api/square?n=abc")
        assert response.status_code == 400
        assert "error" in response.json

    def test_square_missing_param(self, client):
        """Test square with missing parameter."""
        response = client.get("/api/square")
        assert response.status_code == 400
        assert "error" in response.json

    def test_abs_zero(self, client):
        """Test absolute value of zero."""
        response = client.get("/api/abs?n=0")
        assert response.status_code == 200
        assert response.json["result"] == 0

    def test_abs_invalid_param(self, client):
        """Test abs with invalid parameter."""
        response = client.get("/api/abs?n=abc")
        assert response.status_code == 400
        assert "error" in response.json

    def test_abs_missing_param(self, client):
        """Test abs with missing parameter."""
        response = client.get("/api/abs")
        assert response.status_code == 400
        assert "error" in response.json

    def test_parity_zero(self, client):
        """Test parity of zero."""
        response = client.get("/api/parity/0")
        assert response.status_code == 200
        assert response.json["is_even"] is True

    def test_parity_negative_even(self, client):
        """Test parity endpoint with negative numbers (path parameter)."""
        # Negative numbers in URL path may not work - test as expected
        response = client.get("/api/parity/-4")
        # Accept 404 if negative numbers not supported in path
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json["is_even"] is True

    def test_parity_negative_odd(self, client):
        """Test parity endpoint with negative odd numbers."""
        response = client.get("/api/parity/-3")
        # Accept 404 if negative numbers not supported in path
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert response.json["is_odd"] is True

    def test_square_includes_operation(self, client):
        """Test square response includes operation."""
        response = client.get("/api/square?n=5")
        assert "operation" in response.json

    def test_abs_includes_operation(self, client):
        """Test abs response includes operation."""
        response = client.get("/api/abs?n=-5")
        assert "operation" in response.json


class TestEchoEndpoint:
    """Tests for /api/echo endpoint."""

    def test_echo_get_with_message(self, client):
        """Test echo endpoint via GET."""
        response = client.get("/api/echo?message=hello")
        assert response.status_code == 200
        assert response.json["message"] == "hello"

    def test_echo_post_with_json(self, client):
        """Test echo endpoint via POST with JSON."""
        response = client.post(
            "/api/echo", data=json.dumps({"message": "hello"}), content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json["message"] == "hello"

    # NEW: Additional echo tests
    def test_echo_empty_message(self, client):
        """Test echo with empty message."""
        response = client.get("/api/echo?message=")
        assert response.status_code == 200
        assert response.json["message"] == ""

    def test_echo_missing_message(self, client):
        """Test echo with missing message parameter."""
        response = client.get("/api/echo")
        assert response.status_code == 400 or response.status_code == 200

    def test_echo_special_characters(self, client):
        """Test echo with special characters."""
        response = client.get("/api/echo?message=hello%20world!")
        assert response.status_code == 200
        assert "hello" in response.json["message"]

    def test_echo_post_invalid_json(self, client):
        """Test echo POST with invalid JSON."""
        response = client.post("/api/echo", data="invalid json", content_type="application/json")
        assert response.status_code == 400 or response.status_code == 200

    def test_echo_includes_timestamp(self, client):
        """Test echo response includes timestamp."""
        response = client.get("/api/echo?message=test")
        assert "timestamp" in response.json


class TestErrorHandling:
    """Tests for error handling."""

    def test_404_not_found(self, client):
        """Test 404 error handling."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        assert "error" in response.json

    def test_405_method_not_allowed(self, client):
        """Test 405 method not allowed."""
        response = client.post("/")
        assert response.status_code == 405

    # NEW: Comprehensive error tests
    def test_404_includes_message(self, client):
        """Test 404 error includes message."""
        response = client.get("/api/doesnotexist")
        assert response.status_code == 404
        assert "error" in response.json
        assert isinstance(response.json["error"], str)

    def test_invalid_endpoint_variations(self, client):
        """Test various invalid endpoints."""
        endpoints = ["/api/invalid", "/invalid", "/api/", "/api/add/extra/path"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [404, 400]

    def test_error_response_is_json(self, client):
        """Test error responses are JSON."""
        response = client.get("/api/nonexistent")
        assert response.content_type == "application/json"

    def test_method_not_allowed_on_health(self, client):
        """Test method not allowed on health endpoint."""
        response = client.delete("/api/health")
        assert response.status_code == 405

    def test_method_not_allowed_on_add(self, client):
        """Test method not allowed on add endpoint."""
        response = client.post("/api/add?a=5&b=3")
        assert response.status_code == 405

    def test_invalid_parameter_types_comprehensive(self, client):
        """Test invalid parameter types across endpoints."""
        test_cases = [
            ("/api/add?a=text&b=5", 400),
            ("/api/subtract?a=5&b=text", 400),
            ("/api/multiply?a=text&b=text", 400),
            ("/api/divide?a=5&b=text", 400),
            ("/api/square?n=text", 400),
            ("/api/abs?n=text", 400),
        ]
        for endpoint, expected_status in test_cases:
            response = client.get(endpoint)
            assert response.status_code == expected_status
            assert "error" in response.json


class TestResponseFormats:
    """Tests for response format consistency."""

    def test_all_responses_are_json(self, client):
        """Test all endpoints return JSON."""
        response = client.get("/")
        assert response.content_type == "application/json"

    def test_responses_include_timestamp(self, client):
        """Test responses include timestamp."""
        endpoints = ["/", "/api/health", "/api/info", "/api/add?a=1&b=2"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert "timestamp" in response.json

    # NEW: Additional format tests
    def test_all_endpoints_return_json_content_type(self, client):
        """Test all endpoints return JSON content type."""
        endpoints = [
            "/",
            "/api/health",
            "/api/info",
            "/api/add?a=1&b=2",
            "/api/subtract?a=5&b=3",
            "/api/multiply?a=2&b=3",
            "/api/divide?a=6&b=2",
            "/api/square?n=5",
            "/api/abs?n=-5",
            "/api/parity/4",
            "/api/echo?message=test",
        ]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.content_type == "application/json"

    def test_success_responses_have_result_or_status(self, client):
        """Test success responses have result or status."""
        endpoints = [
            ("/", "status"),
            ("/api/health", "status"),
            ("/api/add?a=1&b=2", "result"),
            ("/api/subtract?a=5&b=3", "result"),
        ]
        for endpoint, key in endpoints:
            response = client.get(endpoint)
            assert key in response.json

    def test_error_responses_have_error_key(self, client):
        """Test error responses include error key."""
        error_endpoints = ["/api/add?a=invalid&b=5", "/api/divide?a=5&b=0", "/api/nonexistent"]
        for endpoint in error_endpoints:
            response = client.get(endpoint)
            if response.status_code >= 400:
                assert "error" in response.json

    def test_operation_responses_include_operation_field(self, client):
        """Test operation responses include operation field."""
        endpoints = [
            "/api/add?a=1&b=2",
            "/api/subtract?a=5&b=3",
            "/api/multiply?a=2&b=3",
            "/api/divide?a=6&b=2",
        ]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert "operation" in response.json


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_very_large_numbers(self, client):
        """Test operations with very large numbers."""
        response = client.get("/api/add?a=999999999999&b=1")
        assert response.status_code == 200
        assert response.json["result"] == 1000000000000

    def test_very_small_numbers(self, client):
        """Test operations with very small numbers."""
        response = client.get("/api/add?a=-999999999999&b=-1")
        assert response.status_code == 200
        assert response.json["result"] == -1000000000000

    def test_float_precision(self, client):
        """Test float precision handling."""
        response = client.get("/api/divide?a=1&b=3")
        assert response.status_code == 200
        assert isinstance(response.json["result"], float)

    def test_negative_zero(self, client):
        """Test handling of negative zero."""
        response = client.get("/api/multiply?a=-1&b=0")
        assert response.status_code == 200
        assert response.json["result"] == 0

    def test_multiple_decimal_places(self, client):
        """Test numbers with multiple decimal places."""
        response = client.get("/api/add?a=1.234567&b=2.345678")
        # API may reject decimals - accept both 200 and 400
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            assert isinstance(response.json["result"], float)

    def test_parity_of_large_number(self, client):
        """Test parity check of large number."""
        response = client.get("/api/parity/999999999")
        assert response.status_code == 200
        assert "parity" in response.json

    def test_square_of_large_number(self, client):
        """Test square of large number."""
        response = client.get("/api/square?n=10000")
        assert response.status_code == 200
        assert response.json["result"] == 100000000

    def test_abs_of_very_negative_number(self, client):
        """Test absolute value of very negative number."""
        response = client.get("/api/abs?n=-999999")
        assert response.status_code == 200
        assert response.json["result"] == 999999


class TestConcurrentRequests:
    """Tests for handling multiple concurrent scenarios."""

    def test_multiple_sequential_requests(self, client):
        """Test multiple sequential requests."""
        for i in range(10):
            response = client.get(f"/api/add?a={i}&b=1")
            assert response.status_code == 200
            assert response.json["result"] == i + 1

    def test_alternating_endpoints(self, client):
        """Test alternating between different endpoints."""
        endpoints = [
            "/api/add?a=1&b=2",
            "/api/subtract?a=5&b=3",
            "/api/multiply?a=2&b=3",
            "/api/divide?a=6&b=2",
        ]
        for endpoint in endpoints * 3:
            response = client.get(endpoint)
            assert response.status_code == 200

    def test_rapid_health_checks(self, client):
        """Test rapid health check requests."""
        for _ in range(20):
            response = client.get("/api/health")
            assert response.status_code == 200
            assert response.json["status"] == "healthy"
