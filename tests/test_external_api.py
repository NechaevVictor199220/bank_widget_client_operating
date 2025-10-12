import unittest
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import requests

from src.external_api import convert_to_rubles, get_exchange_rate
from src.utils import get_transaction_amount_in_rubles, load_transactions


class TestExternalAPI(unittest.TestCase):

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_success(self, mock_getenv: Any, mock_get: Any) -> None:
        """Тест успешного получения курса валют"""
        mock_getenv.return_value = "test_api_key"

        # Мокаем успешный ответ API
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "result": 90.5}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("USD", "RUB")
        self.assertEqual(rate, 90.5)

    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_no_api_key(self, mock_getenv: Any) -> None:
        """Тест отсутствия API ключа"""
        mock_getenv.return_value = None

        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_api_error(self, mock_getenv: Any, mock_get: Any) -> None:
        """Тест ошибки API"""
        mock_getenv.return_value = "test_api_key"

        # Мокаем ответ с ошибкой API
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_request_exception(self, mock_getenv: Any, mock_get: Any) -> None:
        """Тест исключения при запросе"""
        mock_getenv.return_value = "test_api_key"

        # Используем конкретное исключение requests
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_json_decode_error(self, mock_getenv: Any, mock_get: Any) -> None:
        """Тест ошибки декодирования JSON"""
        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)

    @patch("src.external_api.requests.get")
    @patch("src.external_api.os.getenv")
    def test_get_exchange_rate_key_error(self, mock_getenv: Any, mock_get: Any) -> None:
        """Тест ошибки ключа в ответе"""
        mock_getenv.return_value = "test_api_key"

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True
            # Нет ключа "result"
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)

    def test_convert_to_rubles_rub(self) -> None:
        """Тест конвертации рублей в рубли"""
        result = convert_to_rubles(100.0, "RUB")
        self.assertEqual(result, 100.0)

    def test_convert_to_rubles_usd_with_fixed_rate(self) -> None:
        """Тест конвертации USD в рубли с фиксированным курсом"""
        result = convert_to_rubles(100.0, "USD")
        # Должен использовать фиксированный курс 90.0
        self.assertEqual(result, 9000.0)

    def test_convert_to_rubles_eur_with_fixed_rate(self) -> None:
        """Тест конвертации EUR в рубли с фиксированным курсом"""
        result = convert_to_rubles(50.0, "EUR")
        # Должен использовать фиксированный курс 100.0
        self.assertEqual(result, 5000.0)

    def test_convert_to_rubles_unknown_currency(self) -> None:
        """Тест конвертации неизвестной валюты"""
        result = convert_to_rubles(100.0, "UNKNOWN")
        # Должен использовать курс по умолчанию 1.0
        self.assertEqual(result, 100.0)

    def test_convert_to_rubles_cache(self) -> None:
        """Тест кэширования курсов валют"""
        # Очищаем кэш
        from src.external_api import _exchange_rates_cache

        _exchange_rates_cache.clear()

        # Первый вызов - должен вычислить
        result1 = convert_to_rubles(100.0, "USD")

        # Второй вызов - должен использовать кэш
        result2 = convert_to_rubles(200.0, "USD")

        self.assertEqual(result1, 9000.0)  # 100 * 90
        self.assertEqual(result2, 18000.0)  # 200 * 90

    @patch("src.external_api.REQUESTS_AVAILABLE", False)
    def test_get_exchange_rate_requests_not_available(self) -> None:
        """Тест когда requests не установлен"""
        rate = get_exchange_rate("USD", "RUB")
        self.assertIsNone(rate)


class TestUtils(unittest.TestCase):

    def test_get_transaction_amount_in_rubles_rub(self) -> None:
        """Тест получения суммы в рублях для RUB транзакции"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertEqual(amount, 1000.50)

    def test_get_transaction_amount_in_rubles_usd(self) -> None:
        """Тест получения суммы в рублях для USD транзакции"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsInstance(amount, float)
        self.assertEqual(amount, 9000.0)  # 100 * 90.0

    def test_get_transaction_amount_in_rubles_invalid_data(self) -> None:
        """Тест обработки невалидных данных транзакции"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_missing_data(self) -> None:
        """Тест обработки отсутствующих данных"""
        transaction: Dict[str, Any] = {}  # Добавляем аннотацию типа

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_empty_amount(self) -> None:
        """Тест обработки пустой суммы"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": "", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_none_amount(self) -> None:
        """Тест обработки None суммы"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": None, "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_missing_currency(self) -> None:
        """Тест обработки отсутствующей валюты"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {
                "amount": "100.00"
                # Нет информации о валюте
            }
        }

        amount = get_transaction_amount_in_rubles(transaction)
        # Должен использовать RUB по умолчанию
        self.assertEqual(amount, 100.0)

    def test_get_transaction_amount_in_rubles_missing_operation_amount(self) -> None:
        """Тест обработки отсутствующего operationAmount"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "other_field": "value"
            # Нет operationAmount
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_invalid_amount_format(self) -> None:
        """Тест обработки неверного формата суммы"""
        transaction: Dict[str, Any] = {  # Добавляем аннотацию типа
            "operationAmount": {"amount": "not_a_number", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    @patch("src.utils.json.load")
    @patch("builtins.open")
    def test_load_transactions_general_exception(self, mock_open: Any, mock_json_load: Any) -> None:
        """Тест обработки общего исключения в load_transactions"""
        mock_open.side_effect = Exception("Unexpected error")

        result = load_transactions("any_file.json")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
