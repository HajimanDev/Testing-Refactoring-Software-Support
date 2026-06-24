"""
Модуль с тестами для функции divide.
"""

import pytest
from app import divide


def test_divide_positive_numbers():
    """Тест деления положительных чисел."""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3
    assert divide(7, 2) == 3.5


def test_divide_negative_numbers():
    """Тест деления с отрицательными числами."""
    assert divide(-10, 2) == -5
    assert divide(10, -2) == -5
    assert divide(-10, -2) == 5


def test_divide_by_zero():
    """Тест: деление на ноль вызывает ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError, match="Деление на ноль недопустимо."):
        divide(10, 0)


def test_divide_float_precision():
    """Тест точности деления с плавающей точкой."""
    assert divide(1, 3) == pytest.approx(0.33333333, rel=1e-6)