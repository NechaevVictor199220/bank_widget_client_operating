import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state,expected_count",
    [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("NONEXISTENT", 0),
    ],
)
def test_filter_by_state_parametrized(sample_operations, state, expected_count):
    """Параметризованный тест фильтрации по разным состояниям"""
    result = filter_by_state(sample_operations, state)
    assert len(result) == expected_count
    if expected_count > 0:
        assert all(op.get("state") == state for op in result)


def test_filter_by_state_default(sample_operations):
    """Тест фильтрации со значением по умолчанию"""
    result = filter_by_state(sample_operations)
    assert len(result) == 3
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_empty_list():
    """Тест фильтрации пустого списка"""
    assert filter_by_state([]) == []
    assert filter_by_state([], "EXECUTED") == []


def test_filter_by_state_operations_without_state():
    """Тестирование операций без ключа state"""
    operations = [
        {"id": 1, "date": "2024-01-01"},  # нет state
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
        {"id": 3, "description": "test"},  # нет state и date
    ]
    result = filter_by_state(operations, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_none_values():
    """Тестирование с None значениями"""
    operations = [
        {"id": 1, "state": None, "date": "2024-01-01"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-02"},
    ]
    result = filter_by_state(operations, "EXECUTED")
    assert len(result) == 1
    assert result[0]["id"] == 2


# Тесты для sort_by_date
def test_sort_by_date_descending(sample_operations):
    """Тест сортировки по убыванию"""
    result = sort_by_date(sample_operations, reverse=True)
    dates = [op["date"] for op in result if "date" in op]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_operations, reverse=False)
    dates = [op["date"] for op in result if "date" in op]
    assert dates == sorted(dates)


def test_sort_by_date_same_dates(operations_with_same_dates):
    """Тест сортировки с одинаковыми датами"""
    result = sort_by_date(operations_with_same_dates, reverse=True)
    assert len(result) == 3


def test_sort_by_date_invalid_dates(operations_invalid_dates):
    """Тест сортировки с невалидными датами"""
    result = sort_by_date(operations_invalid_dates, reverse=True)
    assert len(result) == 3


def test_sort_by_date_empty_list():
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []
    assert sort_by_date([], reverse=False) == []


def test_sort_by_date_mixed_valid_invalid():
    """Тестирование сортировки с смешанными валидными и невалидными датами"""
    operations = [
        {"id": 1, "date": "invalid-date"},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
        {"id": 4},  # нет даты
    ]
    result = sort_by_date(operations, reverse=True)
    assert len(result) == 4


def test_sort_by_date_empty_strings():
    """Тестирование сортировки с пустыми строками дат"""
    operations = [
        {"id": 1, "date": ""},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations, reverse=False)
    assert len(result) == 3


def test_sort_by_date_none_values():
    """Тестирование сортировки с None значениями дат"""
    operations = [
        {"id": 1, "date": None},
        {"id": 2, "date": "2024-01-02T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations)
    assert len(result) == 3


def test_sort_by_date_single_operation():
    """Тестирование сортировки одного элемента"""
    operations = [{"id": 1, "date": "2024-01-01T00:00:00.000000"}]
    result = sort_by_date(operations)
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_sort_by_date_identical_dates():
    """Тестирование сортировки с одинаковыми датами"""
    operations = [
        {"id": 1, "date": "2024-01-01T00:00:00.000000"},
        {"id": 2, "date": "2024-01-01T00:00:00.000000"},
        {"id": 3, "date": "2024-01-01T00:00:00.000000"},
    ]
    result = sort_by_date(operations)
    assert len(result) == 3
    assert {op["id"] for op in result} == {1, 2, 3}
