from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency"""

    def test_filter_usd_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации USD транзакций"""
        usd_gen = filter_by_currency(sample_transactions, "USD")
        usd_list = list(usd_gen)

        assert len(usd_list) == 3
        assert usd_list[0]["id"] == 939719570
        assert usd_list[1]["id"] == 142264268
        assert usd_list[2]["id"] == 895315941
        assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in usd_list)

    def test_filter_rub_transactions(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации RUB транзакций"""
        rub_gen = filter_by_currency(sample_transactions, "RUB")
        rub_list = list(rub_gen)

        assert len(rub_list) == 2
        assert rub_list[0]["id"] == 873106923
        assert rub_list[1]["id"] == 594226727
        assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in rub_list)

    def test_filter_nonexistent_currency(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест фильтрации несуществующей валюты"""
        eur_gen = filter_by_currency(sample_transactions, "EUR")
        eur_list = list(eur_gen)

        assert len(eur_list) == 0

    def test_empty_transactions_list(self) -> None:
        """Тест с пустым списком транзакций"""
        empty_gen = filter_by_currency([], "USD")
        empty_list = list(empty_gen)

        assert len(empty_list) == 0

    def test_generator_behavior(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест поведения генератора (поштучная выдача)"""
        usd_gen = filter_by_currency(sample_transactions, "USD")

        # Проверяем поштучную выдачу
        first = next(usd_gen)
        assert first["id"] == 939719570
        assert first["operationAmount"]["currency"]["code"] == "USD"

        second = next(usd_gen)
        assert second["id"] == 142264268
        assert second["operationAmount"]["currency"]["code"] == "USD"

        third = next(usd_gen)
        assert third["id"] == 895315941
        assert third["operationAmount"]["currency"]["code"] == "USD"

        # Дальше StopIteration
        with pytest.raises(StopIteration):
            next(usd_gen)

    @pytest.mark.parametrize(
        "currency_code,expected_count,expected_ids",
        [
            ("USD", 3, [939719570, 142264268, 895315941]),
            ("RUB", 2, [873106923, 594226727]),
            ("EUR", 0, []),
            ("GBP", 0, []),
        ],
    )
    def test_parametrized_currency_filter(
        self,
        sample_transactions: List[Dict[str, Any]],
        currency_code: str,
        expected_count: int,
        expected_ids: List[int],
    ) -> None:
        """Параметризованный тест фильтрации по разным валютам"""
        result = list(filter_by_currency(sample_transactions, currency_code))
        assert len(result) == expected_count
        assert [t["id"] for t in result] == expected_ids


class TestTransactionDescriptions:
    """Тесты для генератора transaction_descriptions"""

    def test_descriptions_generator(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест генератора описаний"""
        desc_gen = transaction_descriptions(sample_transactions)
        descriptions = list(desc_gen)

        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]

        assert descriptions == expected

    def test_empty_transactions(self) -> None:
        """Тест с пустым списком транзакций"""
        desc_gen = transaction_descriptions([])
        assert list(desc_gen) == []

    def test_generator_next_behavior(self, sample_transactions: List[Dict[str, Any]]) -> None:
        """Тест поштучного получения описаний"""
        desc_gen = transaction_descriptions(sample_transactions)

        assert next(desc_gen) == "Перевод организации"
        assert next(desc_gen) == "Перевод со счета на счет"
        assert next(desc_gen) == "Перевод со счета на счет"
        assert next(desc_gen) == "Перевод с карты на карту"
        assert next(desc_gen) == "Перевод организации"

        # Дальше StopIteration
        with pytest.raises(StopIteration):
            next(desc_gen)

    @pytest.mark.parametrize(
        "count,expected_descriptions",
        [
            (1, ["Перевод организации"]),
            (2, ["Перевод организации", "Перевод со счета на счет"]),
            (3, ["Перевод организации", "Перевод со счета на счет", "Перевод со счета на счет"]),
        ],
    )
    def test_parametrized_descriptions_count(
        self, sample_transactions: List[Dict[str, Any]], count: int, expected_descriptions: List[str]
    ) -> None:
        """Параметризованный тест получения определенного количества описаний"""
        desc_gen = transaction_descriptions(sample_transactions)
        result = [next(desc_gen) for _ in range(count)]
        assert result == expected_descriptions


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator"""

    def test_basic_range(self) -> None:
        """Тест базового диапазона"""
        gen = card_number_generator(1, 5)
        numbers = list(gen)

        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]

        assert numbers == expected

    def test_single_number(self) -> None:
        """Тест генерации одного номера"""
        gen = card_number_generator(123, 123)
        numbers = list(gen)

        assert numbers == ["0000 0000 0000 0123"]
        assert len(numbers) == 1

    def test_large_numbers_formatting(self) -> None:
        """Тест форматирования больших номеров"""
        gen = card_number_generator(9999999999999999, 9999999999999999)
        numbers = list(gen)

        assert numbers == ["9999 9999 9999 9999"]

    def test_range_with_leading_zeros(self) -> None:
        """Тест диапазона с ведущими нулями"""
        gen = card_number_generator(9998, 10001)
        numbers = list(gen)

        expected = ["0000 0000 0000 9998", "0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"]

        assert numbers == expected

    def test_generator_next_behavior(self) -> None:
        """Тест поштучного получения номеров карт"""
        gen = card_number_generator(10, 12)

        assert next(gen) == "0000 0000 0000 0010"
        assert next(gen) == "0000 0000 0000 0011"
        assert next(gen) == "0000 0000 0000 0012"

        with pytest.raises(StopIteration):
            next(gen)

    @pytest.mark.parametrize(
        "start,end,expected_first,expected_last,expected_count",
        [
            (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001", 1),
            (999, 1001, "0000 0000 0000 0999", "0000 0000 0000 1001", 3),
            (123456789, 123456789, "0000 0001 2345 6789"[:19], "0000 0001 2345 6789"[:19], 1),
        ],
    )
    def test_parametrized_ranges(
        self, start: int, end: int, expected_first: str, expected_last: str, expected_count: int
    ) -> None:
        """Параметризованный тест различных диапазонов"""
        gen = card_number_generator(start, end)
        numbers = list(gen)

        assert len(numbers) == expected_count
        if expected_count > 0:
            assert numbers[0] == expected_first
            assert numbers[-1] == expected_last

    def test_formatting_consistency(self) -> None:
        """Тест согласованности форматирования"""
        gen = card_number_generator(1234567890123456, 1234567890123456)
        number = next(gen)

        # Проверяем формат: XXXX XXXX XXXX XXXX
        assert len(number) == 19  # 16 цифр + 3 пробела
        assert number.count(" ") == 3
        parts = number.split(" ")
        assert len(parts) == 4
        assert all(len(part) == 4 for part in parts)
        assert all(part.isdigit() for part in parts)

    def test_invalid_range_errors(self) -> None:
        """Тест ошибок при некорректных диапазонах"""
        with pytest.raises(ValueError):
            list(card_number_generator(0, 5))  # start < 1

        with pytest.raises(ValueError):
            list(card_number_generator(5, 1))  # start > end


# Интеграционные тесты
class TestIntegration:
    """Интеграционные тесты для совместной работы функций"""

    def test_filter_then_descriptions(self, real_transactions: List[Dict[str, Any]]) -> None:
        """Тест цепочки: фильтрация -> получение описаний"""
        # Фильтруем USD транзакции
        usd_transactions = list(filter_by_currency(real_transactions, "USD"))

        # Получаем описания отфильтрованных транзакций
        descriptions = list(transaction_descriptions(usd_transactions))

        assert len(usd_transactions) == 1
        assert len(descriptions) == 1
        assert descriptions[0] == "Перевод организации"
        assert usd_transactions[0]["operationAmount"]["currency"]["code"] == "USD"

    def test_empty_filter_then_descriptions(self, real_transactions: List[Dict[str, Any]]) -> None:
        """Тест цепочки с пустым результатом фильтрации"""
        # Фильтруем несуществующую валюту
        eur_transactions = list(filter_by_currency(real_transactions, "EUR"))

        # Получаем описания (должен быть пустой список)
        descriptions = list(transaction_descriptions(eur_transactions))

        assert len(eur_transactions) == 0
        assert len(descriptions) == 0
