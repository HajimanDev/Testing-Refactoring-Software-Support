"""
Модуль с функцией деления двух чисел.
"""

def divide(a: float, b: float) -> float:
    """
    Делит число a на число b.

    Args:
        a (float): Делимое.
        b (float): Делитель.

    Returns:
        float: Результат деления.

    Raises:
        ZeroDivisionError: Если b равен 0.
    """
    if b == 0:
        raise ZeroDivisionError("Деление на ноль недопустимо.")
    return a / b


def main() -> None:
    """Основная функция для ввода чисел и вывода результата."""
    print("Введите два числа:")
    try:
        x = float(input("Первое число: "))
        y = float(input("Второе число: "))
        result = divide(x, y)
        print(f"Результат деления: {result}")
    except ValueError:
        print("Ошибка: введите корректные числа.")
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

