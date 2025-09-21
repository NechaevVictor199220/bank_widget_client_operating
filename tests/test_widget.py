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

    Проверяет корректное определение типа данных (карта/счет) и применение
    соответствующей маскировки на основе анализа строки:
    - Карты различных платежных систем
    - Счета на русском и английском языках
    - Некорректные входные данные
    - Пустые строки
    """
    assert mask_account_card(input_str) == expected


def test_mask_account_card_with_fixture(sample_data: Dict[str, str]) -> None:
    """
    Тестирование универсальной маскировки с использованием фикстур.

    Проверяет работу функции с предопределенными тестовыми данными:
    - Корректное распознавание и маскировка карт
    - Корректное распознавание и маскировка счетов
    """
    assert mask_account_card(sample_data["card_visa"]) == "Visa Platinum 700079******6361"
    assert mask_account_card(sample_data["account"]) == "Счет **4305"


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-01-01T00:00:00.000000", "01.01.2024"),
        ("invalid-date", "invalid-date"),
        ("", ""),
        (None, None),
    ],
)
def test_get_date_parametrized(date_str: str, expected: str) -> None:
    """
    Параметризованный тест форматирования дат.

    Проверяет преобразование дат из ISO формата в формат ДД.ММ.ГГГГ:
    - Корректные даты с миллисекундами
    - Разные временные зоны и форматы времени
    - Обработка некорректных форматов дат
    - Обработка пустых строк и None значений
    """
    assert get_date(date_str) == expected


def test_get_date_with_fixture(sample_dates: Dict[str, str]) -> None:
    """
    Тестирование форматирования дат с использованием фикстур.

    Проверяет работу функции с предопределенными тестовыми данными:
    - Корректное форматирование валидных дат
    - Корректная обработка невалидных форматов дат
    """
    assert get_date(sample_dates["standard"]) == "11.03.2024"
    assert get_date(sample_dates["invalid"]) == "invalid-date"
