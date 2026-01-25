"""
Utility functions for mathematical operations and helpers.
Provides reusable functions with comprehensive error handling.
"""

from datetime import datetime, timezone
from typing import Union

# ============= TIME UTILITIES =============


def get_current_time() -> str:
    """
    Return current UTC timestamp in ISO format.

    Returns:
        str: ISO format timestamp (e.g., "2024-01-01T12:00:00.000000")
    """
    return datetime.now(timezone.utc).isoformat()


# ============= MATHEMATICAL OPERATIONS =============


def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.

    Args:
        a: First number (int or float)
        b: Second number (int or float)

    Returns:
        Union[int, float]: Sum of a and b

    Raises:
        ValueError: If inputs are not numeric types

    Example:
        >>> add_numbers(5, 3)
        8
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both inputs must be integers or floats")
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not allowed")
    return a + b


def subtract_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Subtract two numbers.

    Args:
        a: First number (int or float)
        b: Second number (int or float)

    Returns:
        Union[int, float]: Difference (a - b)

    Raises:
        ValueError: If inputs are not numeric types

    Example:
        >>> subtract_numbers(10, 3)
        7
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both inputs must be integers or floats")
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not allowed")
    return a - b


def multiply_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiply two numbers.

    Args:
        a: First number (int or float)
        b: Second number (int or float)

    Returns:
        Union[int, float]: Product of a and b

    Raises:
        ValueError: If inputs are not numeric types

    Example:
        >>> multiply_numbers(5, 3)
        15
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both inputs must be integers or floats")
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not allowed")
    return a * b


def divide_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Divide two numbers with zero-check.

    Args:
        a: Numerator (int or float)
        b: Denominator (int or float, cannot be zero)

    Returns:
        Union[int, float]: Quotient (a / b)

    Raises:
        ValueError: If inputs are not numeric types
        ZeroDivisionError: If b is zero

    Example:
        >>> divide_numbers(10, 2)
        5.0
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both inputs must be integers or floats")
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not allowed")
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


# ============= NUMBER PROPERTIES =============


def even_parity(n: int) -> bool:
    """
    Determine if a number has even parity or not.

    Args:
        n: Integer to check

    Returns:
        bool: True if n has even parity, False if n has odd parity

    Raises:
        ValueError: If input is not an integer

    Example:
        >>> even_parity(4)
        True
        >>> even_parity(5)
        False
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Input must be an integer")
    count = 0
    for bit in bin(n)[2:]:
        if bit == "1":
            count += 1
    return not count & 1


def is_even(n: int) -> bool:
    """
    Check if a number is even.

    Args:
        n: Integer to check

    Returns:
        bool: True if n is even, False otherwise

    Raises:
        ValueError: If input is not an integer

    Example:
        >>> is_even(4)
        True
        >>> is_even(5)
        False
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Input must be an integer")
    return not n & 1


def is_odd(n: int) -> bool:
    """
    Check if a number is odd.

    Args:
        n: Integer to check

    Returns:
        bool: True if n is odd, False otherwise

    Raises:
        ValueError: If input is not an integer

    Example:
        >>> is_odd(5)
        True
        >>> is_odd(4)
        False
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Input must be an integer")
    return bool(n & 1)


def square(n: Union[int, float]) -> Union[int, float]:
    """
    Calculate the square of a number.

    Args:
        n: Number to square (int or float)

    Returns:
        Union[int, float]: n squared (n^2)

    Raises:
        ValueError: If input is not numeric

    Example:
        >>> square(5)
        25
        >>> square(2.5)
        6.25
    """
    if not isinstance(n, (int, float)) or isinstance(n, bool):
        raise ValueError("Input must be a number (int or float)")
    return n * n


def absolute_value(n: Union[int, float]) -> Union[int, float]:
    """
    Get the absolute value of a number.

    Args:
        n: Number (int or float)

    Returns:
        Union[int, float]: Absolute value of n

    Raises:
        ValueError: If input is not numeric

    Example:
        >>> absolute_value(-5)
        5
        >>> absolute_value(-2.5)
        2.5
    """
    if not isinstance(n, (int, float)) or isinstance(n, bool):
        raise ValueError("Input must be a number (int or float)")
    return abs(n)


# ============= STRING OPERATIONS =============

def is_palindrome(text: str) -> bool:
    """
    Check if a string is a palindrome.
    Example: "madam" -> True
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    clean_text = ''.join(c.lower() for c in text if c.isalnum())
    return clean_text == clean_text[::-1]

def reverse_string(text: str) -> str:
    """
    Reverse a string.
    Example: "hello" -> "olleh"
    """
    if not isinstance(text, str):
        raise ValueError("Input must be a string")
    return text[::-1]

# ============= LIST OPERATIONS =============

def sort_list(numbers: list, reverse: bool = False) -> list:
    """
    Sort a list of numbers.
    """
    if not isinstance(numbers, list):
        raise ValueError("Input must be a list")
    # specific check for non-numeric elements handled by Python's sort, 
    # but we can be explicit
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise ValueError("List must contain only numbers")
    return sorted(numbers, reverse=reverse)