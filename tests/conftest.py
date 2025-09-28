from typing import Any, Dict, List

import pytest


@pytest.fixture
def sample_card_numbers() -> Dict[str, str]:
    """
    Фикстура предоставляет тестовые данные номеров карт для тестирования.

    Returns:
        Словарь с различными типами номеров карт:
        - standard: стандартный 16-значный номер
        - visa: номер карты Visa
        - mastercard: номер карты Mastercard
        - short: короткий номер (менее 16 цифр)
        - empty: пустая строка
        - with_spaces: номер с пробелами
        - with_dashes: номер с дефисами
    """
    return {
        "standard": "7000792289606361",
        "visa": "4111111111111111",
        "mastercard": "5555555555554444",
        "short": "1234567890",
        "empty": "",
        "with_spaces": "7000 7922 8960 6361",
        "with_dashes": "7000-7922-8960-6361",
    }


@pytest.fixture
def sample_account_numbers() -> Dict[str, str]:
    """
    Фикстура предоставляет тестовые данные номеров счетов для тестирования.

    Returns:
        Словарь с различными типами номеров счетов:
        - standard: стандартный длинный номер счета
        - short: короткий номер (менее 4 цифр)
        - empty: пустая строка
        - min_length: номер минимальной длины для маскировки
        - with_spaces: номер с пробелами
    """
    return {
        "standard": "73654108430135874305",
        "short": "1234",
        "empty": "",
        "min_length": "123456",  # 6 символов
        "with_spaces": "7365 4108 4301 3587 4305",
    }


@pytest.fixture
def sample_data() -> Dict[str, str]:
    """
    Фикстура предоставляет тестовые данные для универсальной функции маскировки.

    Returns:
        Словарь с данными для тестирования mask_account_card:
        - card_visa: строка с картой Visa
        - card_mastercard: строка с картой Mastercard
        - account: строка со счетом на русском
        - account_english: строка со счетом на английском
        - invalid: некорректная строка
        - empty: пустая строка
    """
    return {
        "card_visa": "Visa Platinum 7000792289606361",
        "card_mastercard": "Maestro 7000792289606361",
        "account": "Счет 73654108430135874305",
        "account_english": "Account 73654108430135874305",
        "invalid": "Invalid String",
        "empty": "",
    }


@pytest.fixture
def sample_dates() -> Dict[str, str]:
    """
    Фикстура предоставляет тестовые данные дат для тестирования.

    Returns:
        Словарь с различными форматами дат:
        - standard: полный ISO формат с миллисекундами
        - short_time: ISO формат без миллисекунд
        - no_time: только дата без времени
        - invalid: невалидный формат даты
        - empty: пустая строка
    """
    return {
        "standard": "2024-03-11T02:26:18.671407",
        "short_time": "2024-03-11T02:26:18",
        "no_time": "2024-03-11",
        "invalid": "invalid-date",
        "empty": "",
    }


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """
    Фикстура предоставляет тестовые данные операций для тестирования фильтрации и сортировки.

    Returns:
        Список словарей с операциями, содержащими:
        - Операции с разными статусами (EXECUTED, PENDING, CANCELED)
        - Операции с разными датами в хронологическом порядке
        - Операцию без ключа state (для тестирования обработки отсутствующих полей)
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "PENDING", "date": "2024-02-10T01:25:17.570306"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T00:24:16.469205"},
        {"id": 4, "state": "CANCELED", "date": "2023-12-08T23:23:15.368104"},
        {"id": 5, "state": "EXECUTED", "date": "2023-11-07T22:22:14.267003"},
        {"id": 6, "date": "2023-10-06T21:21:13.165902"},  # без state
    ]


@pytest.fixture
def operations_with_same_dates() -> List[Dict[str, Any]]:
    """
    Фикстура предоставляет операции с одинаковыми датами для тестирования сортировки.

    Returns:
        Список словарей с операциями, содержащими:
        - Операции с идентичными датами (проверка стабильности сортировки)
        - Операции с разными статусами для проверки сохранения порядка
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "PENDING", "date": "2024-03-11T02:26:18.671407"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T00:24:16.469205"},
    ]


@pytest.fixture
def operations_invalid_dates() -> List[Dict[str, Any]]:
    """
    Фикстура предоставляет операции с невалидными датами для тестирования обработки ошибок.

    Returns:
        Список словарей с операциями, содержащими:
        - Невалидный формат даты
        - Корректный формат даты для сравнения
        - Пустую строку вместо даты
    """
    return [
        {"id": 1, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 2, "state": "PENDING", "date": "2024-02-10T01:25:17.570306"},
        {"id": 3, "state": "EXECUTED", "date": ""},
    ]
