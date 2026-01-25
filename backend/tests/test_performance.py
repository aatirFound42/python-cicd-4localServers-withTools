"""
Performance tests for Flask application.
Measures response times, throughput, and ensures performance standards.
"""

# pylint: disable=redefined-outer-name

import time

import pytest

from app.main import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


class TestResponseTimes:
    """Tests for response time performance."""

    def _measure_response_time(self, client, endpoint):
        """
        Measure response time in milliseconds.

        Args:
            client: Flask test client
            endpoint: API endpoint URL

        Returns:
            tuple: (elapsed_ms, response_object)
        """
        start = time.perf_counter()
        response = client.get(endpoint)
        elapsed = (time.perf_counter() - start) * 1000
        return elapsed, response

    def test_health_endpoint_response_time(self, client):
        """Health endpoint must respond within 50ms."""
        elapsed, response = self._measure_response_time(client, "/api/health")
        assert response.status_code == 200
        assert elapsed < 50, f"Health check too slow: {elapsed:.2f}ms"

    def test_add_endpoint_response_time(self, client):
        """Math endpoints must respond within 100ms."""
        endpoints = [
            "/api/add?a=5&b=3",
            "/api/subtract?a=10&b=5",
            "/api/multiply?a=5&b=3",
            "/api/divide?a=10&b=2",
        ]

        for endpoint in endpoints:
            elapsed, response = self._measure_response_time(client, endpoint)
            assert response.status_code == 200
            assert elapsed < 100, f"{endpoint} too slow: {elapsed:.2f}ms (must be < 100ms)"

    def test_utility_endpoint_response_time(self, client):
        """Utility endpoints must respond within 75ms."""
        endpoints = [
            "/api/square?n=5",
            "/api/abs?n=-5",
            "/api/parity/4",
        ]

        for endpoint in endpoints:
            elapsed, response = self._measure_response_time(client, endpoint)
            assert response.status_code == 200
            assert elapsed < 75, f"{endpoint} too slow: {elapsed:.2f}ms (must be < 75ms)"

    def test_info_endpoint_response_time(self, client):
        """Info endpoint must respond within 150ms."""
        elapsed, response = self._measure_response_time(client, "/api/info")
        assert response.status_code == 200
        assert elapsed < 150, f"Info endpoint too slow: {elapsed:.2f}ms"

    def test_echo_endpoint_response_time(self, client):
        """Echo endpoint must respond within 50ms."""
        elapsed, response = self._measure_response_time(client, "/api/echo?message=test")
        assert response.status_code == 200
        assert elapsed < 50, f"Echo endpoint too slow: {elapsed:.2f}ms"


class TestThroughput:
    """Tests for throughput and concurrent request handling."""

    def test_multiple_sequential_requests(self, client):
        """
        Simulate multiple users making requests.
        Should handle 100 requests in reasonable time.
        """
        start = time.perf_counter()

        for i in range(100):
            response = client.get(f"/api/add?a={i}&b=1")
            assert response.status_code == 200

        elapsed = (time.perf_counter() - start) * 1000
        # Average per request
        avg_time = elapsed / 100

        # Should average < 10ms per request
        assert avg_time < 10, f"Average response time too high: {avg_time:.2f}ms"

        # Print metrics for visibility
        print(f"\n100 requests in {elapsed:.2f}ms ({avg_time:.2f}ms each)")

    def test_mixed_endpoint_throughput(self, client):
        """Test throughput with mixed endpoint types."""
        endpoints = [
            "/api/health",
            "/api/add?a=5&b=3",
            "/api/multiply?a=2&b=3",
            "/api/parity/4",
        ]

        start = time.perf_counter()

        # Make 50 requests across all endpoint types
        for _ in range(50):
            for endpoint in endpoints:
                response = client.get(endpoint)
                assert response.status_code == 200

        elapsed = (time.perf_counter() - start) * 1000
        total_requests = 50 * len(endpoints)
        avg_time = elapsed / total_requests

        # Print metrics for visibility
        print(f"\n{total_requests} requests in {elapsed:.2f}ms")
        print(f"Average: {avg_time:.2f}ms per request")

        # Should average < 15ms per request
        assert avg_time < 15, f"Average response time too high: {avg_time:.2f}ms"


class TestErrorHandlingPerformance:
    """Tests for performance under error conditions."""

    def test_error_response_time(self, client):
        """Error responses should still be fast."""
        error_endpoints = [
            "/api/add?a=invalid&b=5",  # Invalid input
            "/api/divide?a=5&b=0",  # Division by zero
            "/api/nonexistent",  # 404
        ]

        for endpoint in error_endpoints:
            start = time.perf_counter()
            response = client.get(endpoint)
            elapsed = (time.perf_counter() - start) * 1000

            assert response.status_code >= 400
            # Error responses should be fast
            assert elapsed < 50, f"Error response too slow: {elapsed:.2f}ms"

    def test_invalid_input_handling_performance(self, client):
        """Test that invalid inputs are rejected quickly."""
        start = time.perf_counter()

        # Make 50 bad requests
        for i in range(50):
            response = client.get(f"/api/add?a=bad{i}&b=input{i}")
            assert response.status_code == 400

        elapsed = (time.perf_counter() - start) * 1000
        avg_time = elapsed / 50

        # Should still be fast with invalid inputs
        assert avg_time < 5, f"Invalid input handling too slow: {avg_time:.2f}ms avg"


class TestLoadCharacteristics:
    """Tests for behavior under load."""

    def test_consistent_performance_under_load(self, client):
        """Performance should remain consistent as load increases."""
        measurements = []

        # Measure performance at different load levels
        requests_counts = [10, 25, 50, 100]
        for requests_count in requests_counts:
            start = time.perf_counter()

            for i in range(requests_count):
                response = client.get(f"/api/add?a={i}&b=1")
                assert response.status_code == 200

            elapsed = (time.perf_counter() - start) * 1000
            avg_time = elapsed / requests_count
            measurements.append(avg_time)

        # Performance should not degrade significantly
        # Last measurement should not be much slower than first
        degradation = ((measurements[-1] - measurements[0]) / measurements[0]) * 100
        assert degradation < 50, f"Performance degraded {degradation:.2f}% under load"

        # Print metrics for visibility
        print("\nPerformance measurements:")
        for i, m in enumerate(measurements):
            print(
                f"  {requests_counts[i]} requests: {m:.2f}ms avg | degradation: "
                + f"{(m - measurements[0]) / measurements[0] * 100:.2f}%"
            )


class TestMemoryAwareOperations:
    """Tests for memory-conscious behavior."""

    def test_large_number_operations(self, client):
        """Test operations with large numbers."""
        large_num = 999999999

        start = time.perf_counter()
        response = client.get(f"/api/add?a={large_num}&b=1")
        elapsed = (time.perf_counter() - start) * 1000

        assert response.status_code == 200
        assert elapsed < 100, "Large number operation too slow"

    def test_zero_and_one_operations(self, client):
        """Special values should be handled efficiently."""
        special_values = [
            ("/api/add?a=0&b=0", 0),
            ("/api/multiply?a=0&b=999", 0),
            ("/api/multiply?a=1&b=999", 999),
            ("/api/add?a=1&b=1", 2),
        ]

        for endpoint, _ in special_values:
            start = time.perf_counter()
            response = client.get(endpoint)
            elapsed = (time.perf_counter() - start) * 1000

            assert response.status_code == 200
            assert elapsed < 50, f"{endpoint} too slow: {elapsed:.2f}ms"
