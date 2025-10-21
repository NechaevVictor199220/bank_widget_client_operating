from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date, filter_by_description


@pytest.fixture
def sample_operations() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми операциями"""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-01-01T00:00:00.000000",
            "description": "Перевод организации"
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-02T00:00:00.000000",
            "description": "Перевод со счета на счет"
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-03T00:00:00.000000",
            "description": "Оплата услуг"
        },
        {
            "id": 4,
            "state": "EXECUTED",
            "date": "2024-01-04T00:00:00.000000",
            "description": "Перевод денег"
        },
        {
            "id": 5,
            "state": "PENDING",
            "date": "2024-01-05T00:00:00.000000",
            "description": "Оплата товаров"
        }
    ]


@pytest.fixture
def operations_with_same_dates() -> List[Dict[str, Any]]:
    """Фикстура с операциями с одинаковыми датами"""
    return [
        {"id": 1, "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "date": "2024-01-01T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]


@pytest.fixture
def operations_invalid_dates() -> List[Dict[str, Any]]:
    """Фикстура с операциями с невалидными датами"""
    return [
        {"id": 1, "date": "invalid-date"},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "another-invalid-date"},
    ]


# Тесты для filter_by_state
@pytest.mark.parametrize(
    "state,expected_count",
    [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("NONEXISTENT", 0),
    ],
)
def test_filter_by_state_parametrized(
        sample_operations: List[Dict[str, Any]], state: str, expected_count: int
) -> None:
    """Параметризованный тест фильтрации по разным состояниям"""
    result = filter_by_state(sample_operations, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(op.get("state") == state for op in result)


def test_filter_by_state_default(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест фильтрации со значением по умолчанию"""
    result = filter_by_state(sample_operations)
    assert len(result) == 3
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_empty_list() -> None:
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_operations_without_state() -> None:
    """Тестирование операций без ключа state"""
    operations = [
        {"id": 1, "date": "2024-01-01"},  # нет state
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
        {"id": 3, "description": "test"},  # нет state и date
    ]
    result = filter_by_state(operations, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_none_values() -> None:
    """Тестирование с None значениями"""
    operations: List[Dict[str, Any]] = [
        {"id": 1, "state": None, "date": "2024-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
    ]
    result = filter_by_state(operations, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


# Тесты для sort_by_date
def test_sort_by_date_descending(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест сортировки по убыванию"""
    result = sort_by_date(sample_operations, reverse=True)
    dates = [op["date"] for op in result if "date" in op]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in result if "date" in op]
    assert dates == sorted(dates)


def test_sort_by_date_same_dates(operations_with_same_dates: List[Dict[str, Any]]) -> None:
    """Тест сортировки с одинаковыми датами"""
    result = sort_by_date(operations_with_same_dates, reverse=True)
    assert len(result) == 3


def test_sort_by_date_invalid_dates(operations_invalid_dates: List[Dict[str, Any]]) -> None:
    """Тест сортировки с невалидными датами"""
    result = sort_by_date(operations_invalid_dates, reverse=True)
    assert len(result) == 3


def test_sort_by_date_empty_list() -> None:
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []
    assert sort_by_date([], reverse=False) == []


def test_sort_by_date_mixed_valid_invalid() -> None:
    """Тестирование сортировки с смешанными валидными и невалидными датами"""
    operations: List[Dict[str, Any]] = [
        {"id": 1, "date": "invalid-date"},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
        {"id": 4},  # нет даты
    ]
    result = sort_by_date(operations, reverse=True)
    assert len(result) == 4


def test_sort_by_date_empty_strings() -> None:
    """Тестирование сортировки с пустыми строками дат"""
    operations = [
        {"id": 1, "date": ""},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations, reverse=False)
    assert len(result) == 3


def test_sort_by_date_none_values() -> None:
    """Тестирование сортировки с None значениями дат"""
    operations: List[Dict[str, Any]] = [
        {"id": 1, "date": None},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations)
    assert len(result) == 3


def test_sort_by_date_single_operation() -> None:
    """Тестирование сортировки одного элемента"""
    operations = [{"id": 1, "date": "2024-01-01T00:00:00.000000"}]
    result = sort_by_date(operations)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_by_date_identical_dates() -> None:
    """Тестирование сортировки с одинаковыми датами"""
    operations = [
        {"id": 1, "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "date": "2024-01-01T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations)
    assert len(result) == 3
    assert {op["id"] for op in result} == {1, 2, 3}


# Тесты для filter_by_description
def test_filter_by_description_basic(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест базовой фильтрации по описанию"""
    result = filter_by_description(sample_operations, "Перевод")
    assert len(result) == 3
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    assert result[2]["id"] == 4


def test_filter_by_description_case_insensitive(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест регистронезависимого поиска"""
    result = filter_by_description(sample_operations, "ПЕРЕВОД")
    assert len(result) == 3

    result = filter_by_description(sample_operations, "перевод")
    assert len(result) == 3


def test_filter_by_description_partial_match(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест поиска по части строки"""
    result = filter_by_description(sample_operations, "организации")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_description_no_match(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест поиска без совпадений"""
    result = filter_by_description(sample_operations, "Кредит")
    assert len(result) == 0


def test_filter_by_description_empty_search(sample_operations: List[Dict[str, Any]]) -> None:
    """Тест поиска с пустой строкой"""
    result = filter_by_description(sample_operations, "")
    assert len(result) == 0


def test_filter_by_description_empty_data() -> None:
    """Тест поиска с пустыми данными"""
    result = filter_by_description([], "Перевод")
    assert len(result) == 0


def test_filter_by_description_special_characters() -> None:
    """Тест поиска с специальными символами"""
    operations_with_special_chars = [
        {
            "id": 1,
            "description": "Payment (USD) to vendor"
        },
        {
            "id": 2,
            "description": "Transfer $100.00"
        }
    ]
    result = filter_by_description(operations_with_special_chars, "(USD)")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_filter_by_description_missing_description() -> None:
    """Тест с операциями без описания"""
    operations_with_missing_desc = [
        {
            "id": 1,
            "description": "Перевод"
        },
        {
            "id": 2,
            # Нет описания
        },
        {
            "id": 3,
            "description": None
        }
    ]
    result = filter_by_description(operations_with_missing_desc, "Перевод")
    assert len(result) == 1
    assert result[0]["id"] == 1


@pytest.mark.parametrize(
    "search_string,expected_ids",
    [
        ("Перевод", [1, 2, 4]),
        ("Оплата", [3, 5]),
        ("организации", [1]),
        ("денег", [4]),
        ("Кредит", []),
        ("", []),
    ],
)
def test_filter_by_description_parametrized(
        sample_operations: List[Dict[str, Any]], search_string: str, expected_ids: List[int]
) -> None:
    """Параметризованный тест фильтрации по описанию"""
    result = filter_by_description(sample_operations, search_string)
    result_ids = [op["id"] for op in result]
    assert result_ids == expected_ids


def test_filter_by_description_regex_special_chars() -> None:
    """Тест поиска с символами, имеющими специальное значение в regex"""
    operations = [
        {"id": 1, "description": "Payment .* regex test"},
        {"id": 2, "description": "Transfer + plus test"},
        {"id": 3, "description": "Normal payment"}
    ]

    # Должен искать буквально ".", а не как regex wildcard
    result = filter_by_description(operations, ".*")
    assert len(result) == 1
    assert result[0]["id"] == 1

    # Должен искать буквально "+", а не как regex quantifier
    result = filter_by_description(operations, "+")
    assert len(result) == 1
    assert result[0]["id"] == 2