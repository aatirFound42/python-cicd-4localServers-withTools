"""
Flask web application - Main application file.
Provides REST API endpoints for the CI/CD learning project.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.utils import (
    absolute_value,
    add_numbers,
    divide_numbers,
    get_current_time,
    is_even,
    is_odd,
    multiply_numbers,
    square,
    subtract_numbers,
)

app = Flask(__name__)
CORS(app)


# ============= HEALTH CHECK ENDPOINTS =============


@app.route("/", methods=["GET"])
def health_check():
    """
    Basic health check endpoint.
    Returns: JSON with status and timestamp
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "message": "Python CI/CD App is running!",
                "timestamp": get_current_time(),
            }
        ),
        200,
    )


@app.route("/api/health", methods=["GET"])
def detailed_health_check():
    """
    Detailed health check with more information.
    Returns: JSON with comprehensive health status
    """
    return (
        jsonify(
            {
                "status": "healthy",
                "service": "python-cicd-app",
                "version": "1.0.0",
                "message": "Application is operational",
                "timestamp": get_current_time(),
                "environment": "development",
            }
        ),
        200,
    )


@app.route("/api/info", methods=["GET"])
def app_info():
    """
    Application information endpoint.
    Returns: JSON with app metadata
    """
    return (
        jsonify(
            {
                "app_name": "Python CI/CD Learning Project",
                "version": "1.0.0",
                "description": "Educational CI/CD pipeline demonstration",
                "endpoints": [
                    {"path": "/", "method": "GET", "description": "Health check"},
                    {"path": "/api/health", "method": "GET", "description": "Detailed health"},
                    {"path": "/api/info", "method": "GET", "description": "App info"},
                    {
                        "path": "/api/add?a=<num>&b=<num>",
                        "method": "GET",
                        "description": "Add numbers",
                    },
                    {
                        "path": "/api/subtract?a=<num>&b=<num>",
                        "method": "GET",
                        "description": "Subtract numbers",
                    },
                    {
                        "path": "/api/multiply?a=<num>&b=<num>",
                        "method": "GET",
                        "description": "Multiply numbers",
                    },
                    {
                        "path": "/api/divide?a=<num>&b=<num>",
                        "method": "GET",
                        "description": "Divide numbers",
                    },
                    {
                        "path": "/api/square?n=<num>",
                        "method": "GET",
                        "description": "Square number",
                    },
                    {"path": "/api/abs?n=<num>", "method": "GET", "description": "Absolute value"},
                    {"path": "/api/parity/<n>", "method": "GET", "description": "Check even/odd"},
                    {"path": "/api/echo", "method": ["GET", "POST"], "description": "Echo data"},
                ],
                "timestamp": get_current_time(),
            }
        ),
        200,
    )


# ============= MATHEMATICAL ENDPOINTS =============


@app.route("/api/add", methods=["GET"])
def add():
    """
    Add two numbers endpoint.
    Query Parameters: a, b (integers)
    Returns: JSON with operation result
    Example: /api/add?a=5&b=3
    """
    try:
        a = request.args.get("a")
        b = request.args.get("b")

        if a is None or b is None:
            return jsonify({"error": "Parameters 'a' and 'b' are required"}), 400

        a = int(a)
        b = int(b)

        result = add_numbers(a, b)
        return (
            jsonify(
                {
                    "operation": "add",
                    "a": a,
                    "b": b,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameters must be valid integers"}), 400


@app.route("/api/subtract", methods=["GET"])
def subtract():
    """
    Subtract two numbers endpoint.
    Query Parameters: a, b (integers)
    Returns: JSON with operation result (a - b)
    Example: /api/subtract?a=10&b=3
    """
    try:
        a = request.args.get("a")
        b = request.args.get("b")

        if a is None or b is None:
            return jsonify({"error": "Parameters 'a' and 'b' are required"}), 400

        a = int(a)
        b = int(b)

        result = subtract_numbers(a, b)
        return (
            jsonify(
                {
                    "operation": "subtract",
                    "a": a,
                    "b": b,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameters must be valid integers"}), 400


@app.route("/api/multiply", methods=["GET"])
def multiply():
    """
    Multiply two numbers endpoint.
    Query Parameters: a, b (integers)
    Returns: JSON with operation result (a * b)
    Example: /api/multiply?a=5&b=3
    """
    try:
        a = request.args.get("a")
        b = request.args.get("b")

        if a is None or b is None:
            return jsonify({"error": "Parameters 'a' and 'b' are required"}), 400

        a = int(a)
        b = int(b)

        result = multiply_numbers(a, b)
        return (
            jsonify(
                {
                    "operation": "multiply",
                    "a": a,
                    "b": b,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameters must be valid integers"}), 400


@app.route("/api/divide", methods=["GET"])
def divide():
    """
    Divide two numbers endpoint.
    Query Parameters: a, b (integers)
    Returns: JSON with operation result (a / b)
    Example: /api/divide?a=10&b=2
    """
    try:
        a = request.args.get("a")
        b = request.args.get("b")

        if a is None or b is None:
            return jsonify({"error": "Parameters 'a' and 'b' are required"}), 400

        a = int(a)
        b = int(b)

        result = divide_numbers(a, b)
        return (
            jsonify(
                {
                    "operation": "divide",
                    "a": a,
                    "b": b,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameters must be valid integers"}), 400
    except ZeroDivisionError:
        return jsonify({"error": "Division by zero is not allowed"}), 400


# ============= UTILITY ENDPOINTS =============


@app.route("/api/square", methods=["GET"])
def square_endpoint():
    """
    Square a number endpoint.
    Query Parameter: n (integer)
    Returns: JSON with squared result (n^2)
    Example: /api/square?n=5
    """
    try:
        n = request.args.get("n")

        if n is None:
            return jsonify({"error": "Parameter 'n' is required"}), 400

        n = int(n)

        result = square(n)
        return (
            jsonify(
                {
                    "operation": "square",
                    "input": n,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameter must be a valid integer"}), 400


@app.route("/api/abs", methods=["GET"])
def absolute_endpoint():
    """
    Get absolute value endpoint.
    Query Parameter: n (integer, can be negative)
    Returns: JSON with absolute value
    Example: /api/abs?n=-5
    """
    try:
        n = request.args.get("n")

        if n is None:
            return jsonify({"error": "Parameter 'n' is required"}), 400

        n = int(n)

        result = absolute_value(n)
        return (
            jsonify(
                {
                    "operation": "absolute_value",
                    "input": n,
                    "result": result,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError:
        return jsonify({"error": "Parameter must be a valid integer"}), 400


@app.route("/api/parity/<int:n>", methods=["GET"])
def parity_endpoint(n):
    """
    Check number parity (even/odd).
    Args: n (integer from URL path)
    Returns: JSON with parity information including is_even boolean
    Example: /api/parity/4
    """
    try:
        even = is_even(n)
        odd = is_odd(n)

        return (
            jsonify(
                {
                    "operation": "parity",
                    "input": n,
                    "is_even": even,
                    "is_odd": odd,
                    "parity": "even" if even else "odd",
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/odd_even/<int:n>", methods=["GET"])
def odd_even_endpoint(n):
    """
    Check number is odd or even (alias for parity).
    Args: n (integer from URL path)
    Returns: JSON with parity information
    Example: /api/odd_even/5
    """
    try:
        even = is_even(n)
        odd = is_odd(n)
        status = "even" if even else "odd"

        return (
            jsonify(
                {
                    "operation": "Odd/Even Check",
                    "input": n,
                    "is_even": even,
                    "is_odd": odd,
                    "status": status,
                    "timestamp": get_current_time(),
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/echo", methods=["GET", "POST"])
def echo():
    """
    Echo endpoint - returns what you send.
    Methods: GET (query params) or POST (JSON body)
    Returns: JSON with echoed data
    Example GET: /api/echo?message=hello
    Example POST: {"message": "hello"}
    """
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message", "") if data else ""
    else:
        message = request.args.get("message", "")

    return jsonify({"operation": "echo", "message": message, "timestamp": get_current_time()}), 200


# ============= ERROR HANDLERS =============


@app.errorhandler(404)
def not_found(_error):
    """Handle 404 Not Found errors."""
    return (
        jsonify(
            {
                "error": "Endpoint not found",
                "status": 404,
                "message": "The requested endpoint does not exist",
                "timestamp": get_current_time(),
            }
        ),
        404,
    )


@app.errorhandler(405)
def method_not_allowed(_error):
    """Handle 405 Method Not Allowed errors."""
    return (
        jsonify(
            {
                "error": "Method not allowed",
                "status": 405,
                "message": "The HTTP method is not allowed for this endpoint",
                "timestamp": get_current_time(),
            }
        ),
        405,
    )


@app.errorhandler(500)
def internal_server_error(_error):
    """Handle 500 Internal Server Error."""
    return (
        jsonify(
            {
                "error": "Internal server error",
                "status": 500,
                "message": "An unexpected error occurred",
                "timestamp": get_current_time(),
            }
        ),
        500,
    )


# ============= APPLICATION ENTRY POINT =============

if __name__ == "__main__":
    import os

    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(host=host, port=port, debug=debug)
