from typing import Dict

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_str,expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 700079******6361"),
        ("Maestro 7000792289606361", "Maestro 700079******6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Account 73654108430135874305", "Account **4305"),
        ("Invalid String", "Invalid String"),
        ("", ""),
    ],
)
def test_mask_account_card_parametrized(input_str: str, expected: str) -> None:
    """
    Параметризованный тест универсальной функции маскировки.
    """
    assert mask_account_card(input_str) == expected


def test_mask_account_card_with_fixture(sample_data: Dict[str, str]) -> None:
    """
    Тестирование универсальной маскировки с использованием фикстур.
    """
    assert mask_account_card(sample_data["card_visa"]) == "Visa Platinum 700079******6361"
    assert mask_account_card(sample_data["account"]) == "Счет **4305"


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("invalid-date", "Дата не указана"),  # Исправлено
        ("", "Дата не указана"),  # Исправлено
        (None, "Дата не указана"),  # Исправлено
    ],
)
def test_get_date_parametrized(date_str: str, expected: str) -> None:
    """
    Параметризованный тест форматирования дат.
    """
    assert get_date(date_str) == expected


def test_get_date_with_fixture(sample_dates: Dict[str, str]) -> None:
    """
    Тестирование форматирования дат с использованием фикстур.
    """
    assert get_date(sample_dates["standard"]) == "11.03.2024"
    assert get_date(sample_dates["invalid"]) == "Дата не указана"  # Исправлено


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
    ],
)
def test_get_date_valid(input_date: str, expected: str) -> None:
    """Тест валидных дат"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "invalid-date",
        "2024-13-01",  # несуществующий месяц
        "2024-01-32",  # несуществующий день
        "not-a-date",
        "",
        None,
    ],
)
def test_get_date_invalid(invalid_date: str) -> None:
    """Тест невалидных дат"""
    assert get_date(invalid_date) == "Дата не указана"


def test_get_date_none() -> None:
    """Тест с None"""
    assert get_date(None) == "Дата не указана"
