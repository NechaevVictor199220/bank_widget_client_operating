from typing import Dict

import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_standard(sample_card_numbers: Dict[str, str]) -> None:
    """Тестирование маскировки стандартного номера карты."""
    assert get_mask_card_number(sample_card_numbers["standard"]) == "700079******6361"


def test_get_mask_card_number_visa(sample_card_numbers: Dict[str, str]) -> None:
    """Тестирование маскировки номера Visa карты."""
    assert get_mask_card_number(sample_card_numbers["visa"]) == "411111******1111"


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("1234567890123456", "123456******3456"),  # 16 цифр
        ("123456789012345", "123456789012345"),  # 15 цифр
        ("12345678901234567", "123456******4567"),  # 17 цифр
        ("", ""),  # пустая строка
        (None, None),  # None
        (1234567812345678, 1234567812345678),  # число
    ],
)
def test_get_mask_card_number_parametrized(card_number: str, expected: str) -> None:
    """
    Параметризованный тест маскировки номеров карт.

    Проверяет различные граничные случаи:
    - Карты разной длины (15, 16, 17 цифр)
    - Пустые строки и None значения
    - Числовые входные данные
    """
    assert get_mask_card_number(card_number) == expected


def test_get_mask_account_number_standard(sample_account_numbers: Dict[str, str]) -> None:
    """Тестирование маскировки стандартного номера счета."""
    assert get_mask_account(sample_account_numbers["standard"]) == "**4305"


def test_get_mask_account_number_short(sample_account_numbers: Dict[str, str]) -> None:
    """
    Тестирование маскировки короткого номера счета.

    Проверяет, что счета короче 4 цифр не маскируются.
    """
    assert get_mask_account(sample_account_numbers["short"]) == "1234"


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("73654108430135874305", "**4305"),  # стандартный
        ("12345678901234567890", "**7890"),  # 20 цифр
        ("1234", "1234"),  # меньше 4 цифр
        ("123", "123"),  # 3 цифры
        ("", ""),  # пустая строка
        (None, None),  # None
    ],
)
def test_get_mask_account_number_parametrized(account_number: str, expected: str) -> None:
    """
    Параметризованный тест маскировки номеров счетов.

    Проверяет различные граничные случаи:
    - Стандартные номера счетов (20 цифр)
    - Короткие номера (менее 4 цифр) - не должны маскироваться
    - Пустые строки и None значения
    - Граничное условие: ровно 4 цифры (должны маскироваться)
    """
    assert get_mask_account(account_number) == expected
