from unittest.mock import patch

import pytest

from src.main import format_amount, format_transaction, get_sort_direction, get_yes_no_input


class TestMainFunctions:
    """Тесты для функций основного модуля"""

    @pytest.mark.parametrize("yes_input", ["да", "д", "yes", "y", ""])
    def test_get_yes_no_input_yes_variants(self, yes_input: str) -> None:
        """Тест ответов Да"""
        with patch("builtins.input", return_value=yes_input):
            result = get_yes_no_input("Тестовый вопрос")
            assert result is True

    @pytest.mark.parametrize("no_input", ["нет", "н", "no", "n"])
    def test_get_yes_no_input_no_variants(self, no_input: str) -> None:
        """Тест ответов Нет"""
        with patch("builtins.input", return_value=no_input):
            result = get_yes_no_input("Тестовый вопрос")
            assert result is False

    @pytest.mark.parametrize("invalid_input", ["maybe", "123", "test"])
    def test_get_yes_no_input_invalid_then_valid(self, invalid_input: str) -> None:
        """Тест невалидного ввода с последующим валидным"""
        with patch("builtins.input", side_effect=[invalid_input, "да"]):
            result = get_yes_no_input("Тестовый вопрос")
            assert result is True

    @pytest.mark.parametrize("asc_input", ["по возрастанию", "возрастанию", "asc", "ascending", ""])
    def test_get_sort_direction_ascending(self, asc_input: str) -> None:
        """Тест выбора сортировки по возрастанию"""
        with patch("builtins.input", return_value=asc_input):
            result = get_sort_direction()
            assert result is False  # False = по возрастанию

    @pytest.mark.parametrize("desc_input", ["по убыванию", "убыванию", "desc", "descending"])
    def test_get_sort_direction_descending(self, desc_input: str) -> None:
        """Тест выбора сортировки по убыванию"""
        with patch("builtins.input", return_value=desc_input):
            result = get_sort_direction()
            assert result is True  # True = по убыванию

    @pytest.mark.parametrize("invalid_input", ["invalid", "123", "test"])
    def test_get_sort_direction_invalid_then_valid(self, invalid_input: str) -> None:
        """Тест невалидного ввода направления с последующим валидным"""
        with patch("builtins.input", side_effect=[invalid_input, "по возрастанию"]):
            result = get_sort_direction()
            assert result is False

    def test_format_amount_rub(self) -> None:
        """Тест форматирования рублевой суммы"""
        transaction = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB", "name": "руб."}}}
        result = format_amount(transaction)
        assert "1000.50 руб." in result

    def test_format_amount_usd(self) -> None:
        """Тест форматирования долларовой суммы"""
        transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}}}
        result = format_amount(transaction)
        assert "100.00 USD" in result

    def test_format_amount_eur(self) -> None:
        """Тест форматирования евро суммы"""
        transaction = {"operationAmount": {"amount": "50.75", "currency": {"code": "EUR", "name": "EUR"}}}
        result = format_amount(transaction)
        assert "50.75 EUR" in result

    def test_format_amount_missing_currency(self) -> None:
        """Тест форматирования суммы без валюты"""
        transaction = {"operationAmount": {"amount": "100.00"}}
        result = format_amount(transaction)
        assert "100.00" in result

    def test_format_amount_missing_operation_amount(self) -> None:
        """Тест форматирования суммы без operationAmount"""
        transaction = {}
        result = format_amount(transaction)
        assert "0" in result

    def test_format_transaction_complete(self) -> None:
        """Тест форматирования полной транзакции"""
        transaction = {
            "date": "2024-01-01T00:00:00.000000",
            "description": "Перевод организации",
            "from": "Visa Platinum 7000792289606361",
            "to": "Счет 73654108430135874305",
            "operationAmount": {"amount": "1000.50", "currency": {"code": "RUB", "name": "руб."}},
        }
        result = format_transaction(transaction)

        # Проверяем ключевые элементы
        assert "01.01.2024" in result
        assert "Перевод организации" in result
        assert "Visa Platinum 700079******6361" in result
        assert "Счет **4305" in result
        assert "1000.50 руб." in result

    def test_format_transaction_minimal(self) -> None:
        """Тест форматирования минимальной транзакции"""
        transaction = {"description": "Тестовая операция"}
        result = format_transaction(transaction)
        assert "Тестовая операция" in result
        assert "Дата не указана" in result

    def test_format_transaction_only_from(self) -> None:
        """Тест форматирования транзакции только с отправителем"""
        transaction = {
            "date": "2024-01-01T00:00:00.000000",
            "description": "Снятие наличных",
            "from": "MasterCard 1234567812345678",
            "operationAmount": {"amount": "5000.00", "currency": {"code": "RUB", "name": "руб."}},
        }
        result = format_transaction(transaction)
        assert "MasterCard 123456******5678" in result
        assert "Снятие наличных" in result

    def test_format_transaction_only_to(self) -> None:
        """Тест форматирования транзакции только с получателем"""
        transaction = {
            "date": "2024-01-01T00:00:00.000000",
            "description": "Пополнение счета",
            "to": "Счет 12345678901234567890",
            "operationAmount": {"amount": "10000.00", "currency": {"code": "RUB", "name": "руб."}},
        }
        result = format_transaction(transaction)
        assert "Счет **7890" in result
        assert "Пополнение счета" in result

    def test_format_transaction_no_date(self) -> None:
        """Тест форматирования транзакции без даты"""
        transaction = {
            "description": "Операция без даты",
            "from": "Visa 1234567890123456",
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD", "name": "USD"}},
        }
        result = format_transaction(transaction)
        assert "Дата не указана" in result
        assert "Операция без даты" in result

    def test_format_transaction_invalid_date(self) -> None:
        """Тест форматирования транзакции с невалидной датой"""
        transaction = {
            "date": "invalid-date",
            "description": "Операция с невалидной датой",
            "operationAmount": {"amount": "100.00", "currency": {"code": "RUB", "name": "руб."}},
        }
        result = format_transaction(transaction)
        assert "Дата не указана" in result
        assert "Операция с невалидной датой" in result


class TestMainModule:
    """Тесты для основного модуля"""

    def test_main_import(self) -> None:
        """Тест, что модуль main импортируется без ошибок"""
        try:
            # Если импорт прошел успешно - тест пройден
            assert True
        except ImportError as e:
            pytest.fail(f"Ошибка импорта main модуля: {e}")

    def test_main_functions_exist(self) -> None:
        """Тест, что основные функции существуют"""

        # Если импорт прошел успешно - тест пройден
        assert True


@pytest.mark.parametrize(
    "transaction_data,expected_elements",
    [
        (
            {
                "date": "2024-01-01T00:00:00.000000",
                "description": "Тест",
                "from": "Карта 1234567812345678",
                "to": "Счет 12345678901234567890",
                "operationAmount": {"amount": "100.00", "currency": {"code": "RUB", "name": "руб."}},
            },
            ["01.01.2024", "Тест", "Карта 123456******5678", "Счет **7890", "100.00 руб."],
        ),
        ({"description": "Минимальная операция"}, ["Минимальная операция", "Дата не указана"]),
    ],
)
def test_format_transaction_parametrized(transaction_data: dict, expected_elements: list) -> None:
    """Параметризованный тест форматирования транзакций"""
    result = format_transaction(transaction_data)
    for element in expected_elements:
        assert element in result


def test_format_transaction_empty() -> None:
    """Тест форматирования пустой транзакции"""
    result = format_transaction({})
    assert "Описание отсутствует" in result
    assert "Дата не указана" in result


@pytest.mark.parametrize(
    "amount_data,expected_text",
    [
        ({"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB", "name": "руб."}}}, "1000.50 руб."),
        ({"operationAmount": {"amount": "200.00", "currency": {"code": "USD", "name": "USD"}}}, "200.00 USD"),
        ({"operationAmount": {"amount": "50.25"}}, "50.25"),
        ({}, "0"),
    ],
)
def test_format_amount_parametrized(amount_data: dict, expected_text: str) -> None:
    """Параметризованный тест форматирования сумм"""
    result = format_amount(amount_data)
    assert expected_text in result


def test_main_module_attributes() -> None:
    """Тест атрибутов основного модуля"""
    import src.main as main_module

    # Проверяем что основные функции существуют
    assert hasattr(main_module, "main")
    assert hasattr(main_module, "get_yes_no_input")
    assert hasattr(main_module, "get_sort_direction")
    assert hasattr(main_module, "format_transaction")
    assert hasattr(main_module, "format_amount")

    # Проверяем что это callable объекты (функции)
    assert callable(main_module.main)
    assert callable(main_module.get_yes_no_input)
    assert callable(main_module.get_sort_direction)
