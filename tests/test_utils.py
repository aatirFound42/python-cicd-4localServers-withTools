"""
Unit tests for utility functions.
Comprehensive tests including edge cases and error conditions.
"""

import pytest

from app.utils import (
    absolute_value,
    add_numbers,
    divide_numbers,
    even_parity,
    get_current_time,
    is_even,
    is_odd,
    multiply_numbers,
    square,
    subtract_numbers,
)


class TestGetCurrentTime:
    """Tests for get_current_time function."""

    def test_returns_string(self):
        """Test that function returns string."""
        result = get_current_time()
        assert isinstance(result, str)

    def test_returns_iso_format(self):
        """Test that timestamp is in ISO format."""
        result = get_current_time()
        assert "T" in result  # ISO format has T separator
        assert len(result) > 0

    def test_contains_digits(self):
        """Test that timestamp contains digits."""
        result = get_current_time()
        assert any(c.isdigit() for c in result)


class TestAddNumbers:
    """Tests for add_numbers function."""

    def test_add_positive_integers(self):
        """Test adding positive integers."""
        assert add_numbers(5, 3) == 8

    def test_add_negative_integers(self):
        """Test adding negative integers."""
        assert add_numbers(-5, -3) == -8

    def test_add_mixed_signs(self):
        """Test adding numbers with different signs."""
        assert add_numbers(10, -7) == 3

    def test_add_with_zero(self):
        """Test adding with zero."""
        assert add_numbers(5, 0) == 5

    def test_add_floats(self):
        """Test adding float numbers."""
        assert add_numbers(2.5, 1.5) == 4.0

    def test_add_large_numbers(self):
        """Test adding large numbers."""
        assert add_numbers(999999, 1) == 1000000

    def test_add_raises_error_for_none(self):
        """Test error when adding None."""
        with pytest.raises(ValueError):
            add_numbers(None, 5)

    def test_add_raises_error_for_string(self):
        """Test error when adding string."""
        with pytest.raises(ValueError):
            add_numbers("5", 3)

    def test_add_raises_error_for_bool(self):
        """Test error when using boolean."""
        with pytest.raises(ValueError):
            add_numbers(True, 5)


class TestSubtractNumbers:
    """Tests for subtract_numbers function."""

    def test_subtract_positive_integers(self):
        """Test subtracting positive integers."""
        assert subtract_numbers(10, 3) == 7

    def test_subtract_negative_integers(self):
        """Test subtracting negative integers."""
        assert subtract_numbers(-10, -3) == -7

    def test_subtract_results_negative(self):
        """Test subtraction resulting in negative."""
        assert subtract_numbers(3, 10) == -7

    def test_subtract_floats(self):
        """Test subtracting floats."""
        assert subtract_numbers(5.5, 2.5) == 3.0


class TestMultiplyNumbers:
    """Tests for multiply_numbers function."""

    def test_multiply_positive_integers(self):
        """Test multiplying positive integers."""
        assert multiply_numbers(5, 3) == 15

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert multiply_numbers(100, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert multiply_numbers(-5, -3) == 15

    def test_multiply_mixed_signs(self):
        """Test multiplying with different signs."""
        assert multiply_numbers(-5, 3) == -15


class TestDivideNumbers:
    """Tests for divide_numbers function."""

    def test_divide_positive_integers(self):
        """Test dividing positive integers."""
        assert divide_numbers(10, 2) == 5.0

    def test_divide_with_float_result(self):
        """Test division with float result."""
        result = divide_numbers(10, 3)
        assert abs(result - 3.333) < 0.01

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises error."""
        with pytest.raises(ZeroDivisionError):
            divide_numbers(10, 0)

    def test_divide_negative_numbers(self):
        """Test dividing negative numbers."""
        assert divide_numbers(-10, 2) == -5.0

    def test_divide_raises_error_for_string(self):
        """Test error when dividing by string."""
        with pytest.raises(ValueError):
            divide_numbers(10, "2")


class TestIsEven:
    """Tests for is_even function."""

    def test_even_numbers_return_true(self):
        """Test that even numbers return True."""
        assert is_even(4) is True
        assert is_even(0) is True
        assert is_even(-4) is True

    def test_odd_numbers_return_false(self):
        """Test that odd numbers return False."""
        assert is_even(3) is False
        assert is_even(1) is False
        assert is_even(-3) is False

    def test_raises_error_for_float(self):
        """Test error when checking float."""
        with pytest.raises(ValueError):
            is_even(4.5)

    def test_raises_error_for_string(self):
        """Test error when checking string."""
        with pytest.raises(ValueError):
            is_even("4")


class TestIsOdd:
    """Tests for is_odd function."""

    def test_odd_numbers_return_true(self):
        """Test that odd numbers return True."""
        assert is_odd(3) is True
        assert is_odd(1) is True
        assert is_odd(-3) is True

    def test_even_numbers_return_false(self):
        """Test that even numbers return False."""
        assert is_odd(4) is False
        assert is_odd(0) is False
        assert is_odd(-4) is False

    def test_raises_error_for_float(self):
        """Test error when checking float."""
        with pytest.raises(ValueError):
            is_odd(3.5)


class TestEvenParity:
    """Tests for even_parity function (binary parity check)."""

    def test_even_parity_return_true(self):
        """
        Test that numbers with even parity return True.
        Even parity = even count of 1-bits in binary representation.
        3 = 0b11 (two 1s) → even parity → True
        0 = 0b0 (zero 1s) → even parity → True
        """
        assert even_parity(3) is True  # 0b11 → 2 ones → even
        assert even_parity(0) is True  # 0b0 → 0 ones → even
        assert even_parity(5) is True  # 0b101 → 2 ones → even
        assert even_parity(6) is True  # 0b110 → 2 ones → even

    def test_even_parity_return_false(self):
        """
        Test that numbers with odd parity return False.
        Odd parity = odd count of 1-bits in binary representation.
        4 = 0b100 (one 1) → odd parity → False
        2 = 0b10 (one 1) → odd parity → False
        """
        assert even_parity(4) is False  # 0b100 → 1 one → odd
        assert even_parity(2) is False  # 0b10 → 1 one → odd
        assert even_parity(1) is False  # 0b1 → 1 one → odd
        assert even_parity(7) is False  # 0b111 → 3 ones → odd

    def test_raises_error_for_float(self):
        """Test error when checking float."""
        with pytest.raises(ValueError):
            even_parity(2.5)

    def test_raises_error_for_string(self):
        """Test error when checking string."""
        with pytest.raises(ValueError):
            even_parity("2")


class TestSquare:
    """Tests for square function."""

    def test_square_positive_number(self):
        """Test squaring positive number."""
        assert square(5) == 25

    def test_square_negative_number(self):
        """Test squaring negative number."""
        assert square(-5) == 25

    def test_square_zero(self):
        """Test squaring zero."""
        assert square(0) == 0

    def test_square_float(self):
        """Test squaring float."""
        assert square(2.5) == 6.25


class TestAbsoluteValue:
    """Tests for absolute_value function."""

    def test_absolute_positive_number(self):
        """Test absolute value of positive number."""
        assert absolute_value(5) == 5

    def test_absolute_negative_number(self):
        """Test absolute value of negative number."""
        assert absolute_value(-5) == 5

    def test_absolute_zero(self):
        """Test absolute value of zero."""
        assert absolute_value(0) == 0

    def test_absolute_float(self):
        """Test absolute value of float."""
        assert absolute_value(-2.5) == 2.5


class TestIntegrationScenarios:
    """Integration tests combining multiple functions."""

    def test_add_and_square(self):
        """Test chaining add and square operations."""
        result = add_numbers(2, 3)  # 5
        squared = square(result)  # 25
        assert squared == 25

    def test_divide_and_absolute(self):
        """Test chaining divide and absolute value."""
        result = divide_numbers(-10, 2)  # -5.0
        absolute = absolute_value(result)  # 5.0
        assert absolute == 5.0

    def test_odd_even_checks(self):
        """Test odd-even checking logic."""
        for n in range(10):
            is_n_even = is_even(n)
            is_n_odd = is_odd(n)
            assert is_n_even != is_n_odd  # Cannot be both even and odd

    def test_multiply_and_square(self):
        """Test chaining multiply and square."""
        result = multiply_numbers(2, 3)  # 6
        squared = square(result)  # 36
        assert squared == 36

    def test_subtract_and_absolute(self):
        """Test chaining subtract and absolute value."""
        result = subtract_numbers(5, 10)  # -5
        absolute = absolute_value(result)  # 5
        assert absolute == 5
