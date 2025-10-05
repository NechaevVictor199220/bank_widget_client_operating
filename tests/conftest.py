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


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def real_transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
    ]
