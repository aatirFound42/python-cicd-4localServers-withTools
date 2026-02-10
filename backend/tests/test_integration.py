"""
Integration tests for Flask application.
Tests multi-endpoint workflows and real-world usage patterns.
"""

# pylint: disable=redefined-outer-name

import json

import pytest

from app.main import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


class TestMathematicalWorkflows:
    """Integration tests for mathematical operation workflows."""

    def test_calculation_chain_add_then_multiply(self, client):
        """
        Test workflow: Add two numbers, then multiply result by another.
        This simulates a user doing multiple calculations.
        """
        # Step 1: Add 5 + 3 = 8
        response1 = client.get("/api/add?a=5&b=3")
        assert response1.status_code == 200
        result1 = response1.json["result"]
        assert result1 == 8

        # Step 2: Multiply result by 2: 8 * 2 = 16
        response2 = client.get(f"/api/multiply?a={result1}&b=2")
        assert response2.status_code == 200
        result2 = response2.json["result"]
        assert result2 == 16

        # Step 3: Verify both responses have timestamps
        assert "timestamp" in response1.json
        assert "timestamp" in response2.json

    def test_calculation_chain_subtract_then_square(self, client):
        """Test workflow: Subtract, then square the result."""
        # Step 1: Subtract 10 - 3 = 7
        response1 = client.get("/api/subtract?a=10&b=3")
        assert response1.status_code == 200
        result1 = response1.json["result"]
        assert result1 == 7

        # Step 2: Square result: 7^2 = 49
        response2 = client.get(f"/api/square?n={result1}")
        assert response2.status_code == 200
        result2 = response2.json["result"]
        assert result2 == 49

    def test_division_with_error_handling(self, client):
        """Test division endpoint error handling in workflow."""
        # Step 1: Successful division
        response1 = client.get("/api/divide?a=10&b=2")
        assert response1.status_code == 200
        assert response1.json["result"] == 5.0

        # Step 2: Division by zero (should fail gracefully)
        response2 = client.get("/api/divide?a=10&b=0")
        assert response2.status_code == 400
        assert "error" in response2.json
        assert "zero" in response2.json["error"].lower()


class TestEndpointCombinations:
    """Integration tests for combining different endpoints."""

    def test_get_info_then_use_endpoints(self, client):
        """
        Test workflow: Get app info, then verify all listed endpoints work.
        """
        # Step 1: Get app info
        response = client.get("/api/info")
        assert response.status_code == 200
        info = response.json

        # Step 2: Verify we got endpoint list
        assert "endpoints" in info
        endpoints = info["endpoints"]
        assert len(endpoints) > 5

        # Step 3: Verify at least one endpoint works
        add_endpoint_exists = any(ep.get("path", "").startswith("/api/add") for ep in endpoints)
        assert add_endpoint_exists

    def test_health_check_before_operations(self, client):
        """Test workflow: Check health, then perform operations."""
        # Step 1: Check health
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json["status"] == "healthy"

        # Step 2: If healthy, perform operation
        if health.json["status"] == "healthy":
            operation = client.get("/api/add?a=5&b=3")
            assert operation.status_code == 200
            assert operation.json["result"] == 8


class TestResponseFormatConsistency:
    """Integration tests for consistent response formats."""

    def test_all_endpoints_return_json(self, client):
        """Verify all endpoints return JSON content type."""
        endpoints = [
            "/",
            "/api/health",
            "/api/info",
            "/api/add?a=1&b=1",
            "/api/subtract?a=5&b=3",
            "/api/multiply?a=2&b=3",
            "/api/divide?a=6&b=2",
            "/api/square?n=5",
            "/api/abs?n=-5",
            "/api/parity/4",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.content_type == "application/json", f"{endpoint} did not return JSON"

    def test_all_responses_include_operation_or_status(self, client):
        """Verify all responses include operation/status information."""
        test_cases = [
            ("/", "status"),
            ("/api/add?a=1&b=1", "operation"),
            ("/api/health", "status"),
            ("/api/info", "app_name"),
        ]

        for endpoint, key in test_cases:
            response = client.get(endpoint)
            assert key in response.json, f"{endpoint} missing '{key}' in response"

    def test_error_responses_have_consistent_format(self, client):
        """Verify error responses follow consistent format."""
        error_cases = [
            "/api/add?a=abc&b=def",  # Invalid parameters
            "/api/add?a=5",  # Missing parameter
            "/api/divide?a=5&b=0",  # Division by zero
            "/api/nonexistent",  # Not found
        ]

        for endpoint in error_cases:
            response = client.get(endpoint)
            # Error response should have status code >= 400
            assert response.status_code >= 400
            # Error response should include 'error' key
            assert "error" in response.json


class TestComplexScenarios:
    """Integration tests for complex real-world scenarios."""

    def test_user_workflow_mathematical_analysis(self, client):
        """
        Simulate user workflow: Analyze numbers for properties.
        User wants to: Add two numbers, check if even/odd, square it.
        """
        # User input: 5 and 7
        numbers = [5, 7]

        # Step 1: Add them
        add_resp = client.get(f"/api/add?a={numbers[0]}&b={numbers[1]}")
        assert add_resp.status_code == 200
        sum_result = add_resp.json["result"]
        assert sum_result == 12

        # Step 2: Check if sum is even/odd
        parity_resp = client.get(f"/api/parity/{sum_result}")
        assert parity_resp.status_code == 200
        is_even = parity_resp.json["is_even"]
        assert is_even is True  # 12 is even

        # Step 3: Square the sum
        square_resp = client.get(f"/api/square?n={sum_result}")
        assert square_resp.status_code == 200
        squared = square_resp.json["result"]
        assert squared == 144  # 12^2 = 144

        # Verify all operations have timestamps
        for resp in [add_resp, parity_resp, square_resp]:
            assert "timestamp" in resp.json

    def test_user_workflow_with_error_recovery(self, client):
        """
        Test workflow with error handling.
        User tries invalid input, gets error, then succeeds.
        """
        # Step 1: Try invalid input
        bad_response = client.get("/api/add?a=invalid&b=5")
        assert bad_response.status_code == 400
        assert "error" in bad_response.json

        # Step 2: Recover and try valid input
        good_response = client.get("/api/add?a=5&b=3")
        assert good_response.status_code == 200
        assert good_response.json["result"] == 8


class TestSequentialOperations:
    """Integration tests for sequential operation chains."""

    def test_echo_endpoint_with_data_flow(self, client):
        """Test echo endpoint with JSON data."""
        test_data = {"message": "test data", "value": 42}

        # POST JSON data
        response = client.post(
            "/api/echo", data=json.dumps(test_data), content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json["message"] == test_data["message"]

    def test_sequential_mathematical_operations(self, client):
        """
        Test sequence: Start with 2, double it, add 10, divide by 3.
        2 → 4 → 14 → 4.67
        """
        value = 2

        # Step 1: Double (multiply by 2)
        resp1 = client.get(f"/api/multiply?a={value}&b=2")
        assert resp1.status_code == 200
        value = resp1.json["result"]
        assert value == 4

        # Step 2: Add 10
        resp2 = client.get(f"/api/add?a={value}&b=10")
        assert resp2.status_code == 200
        value = resp2.json["result"]
        assert value == 14

        # Step 3: Divide by 3
        resp3 = client.get(f"/api/divide?a={value}&b=3")
        assert resp3.status_code == 200
        final_value = resp3.json["result"]
        assert abs(final_value - 4.666) < 0.01
