import os
import json
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import pandas as pd

from src.utils import load_transactions, get_transaction_amount_in_rubles


class TestLoadTransactions(unittest.TestCase):

    def test_load_existing_json_file(self) -> None:
        """Тест загрузки существующего JSON файла"""
        transactions = load_transactions('data/operations.json')
        self.assertIsInstance(transactions, list)
        self.assertGreater(len(transactions), 0)

    def test_file_not_found(self) -> None:
        """Тест загрузки несуществующего файла"""
        transactions = load_transactions('data/nonexistent.json')
        self.assertEqual(transactions, [])

    def test_invalid_json(self) -> None:
        """Тест загрузки файла с некорректным JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_empty_file(self) -> None:
        """Тест загрузки пустого файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            # просто создаем пустой файл
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_not_list_content(self) -> None:
        """Тест загрузки файла с содержимым не списком"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"key": "value"}, f)  # словарь вместо списка
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    @patch('src.utils.json.load')
    @patch('builtins.open')
    def test_load_transactions_general_exception(self, mock_open: Any, mock_json_load: Any) -> None:
        """Тест обработки общего исключения в load_transactions"""
        mock_open.side_effect = Exception("Unexpected error")

        result = load_transactions('any_file.json')
        self.assertEqual(result, [])

    @patch('src.utils.pd.read_csv')
    def test_load_csv_success(self, mock_read_csv: Any) -> None:
        """Тест успешной загрузки CSV файла"""
        # Создаем мок DataFrame с транзакциями
        mock_df = MagicMock()
        mock_data = [
            {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01', 'amount': '100.0'},
            {'id': 2, 'state': 'PENDING', 'date': '2024-01-02', 'amount': '200.0'}
        ]
        mock_df.to_dict.return_value = mock_data
        mock_read_csv.return_value = mock_df

        # Создаем временный CSV файл для теста
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('id,state,date,amount\n1,EXECUTED,2024-01-01,100.0\n2,PENDING,2024-01-02,200.0')
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(len(transactions), 2)
            self.assertEqual(transactions[0]['id'], 1)
            self.assertEqual(transactions[1]['state'], 'PENDING')
        finally:
            os.unlink(temp_path)

    @patch('src.utils.pd.read_excel')
    def test_load_excel_success(self, mock_read_excel: Any) -> None:
        """Тест успешной загрузки Excel файла"""
        # Создаем мок DataFrame с транзакциями
        mock_df = MagicMock()
        mock_data = [
            {'id': 1, 'description': 'Payment 1', 'amount': '150.0', 'currency': 'RUB'},
            {'id': 2, 'description': 'Payment 2', 'amount': '250.0', 'currency': 'USD'}
        ]
        mock_df.to_dict.return_value = mock_data
        mock_read_excel.return_value = mock_df

        # Создаем временный Excel файл для теста
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as f:
            # Просто создаем пустой файл, так как мы мокаем pandas
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(len(transactions), 2)
            self.assertEqual(transactions[0]['description'], 'Payment 1')
            self.assertEqual(transactions[1]['currency'], 'USD')
        finally:
            os.unlink(temp_path)

    @patch('src.utils.pd.read_csv')
    def test_load_csv_exception(self, mock_read_csv: Any) -> None:
        """Тест обработки исключения при загрузке CSV"""
        mock_read_csv.side_effect = Exception("CSV read error")

        # Создаем временный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    @patch('src.utils.pd.read_excel')
    def test_load_excel_exception(self, mock_read_excel: Any) -> None:
        """Тест обработки исключения при загрузке Excel"""
        mock_read_excel.side_effect = Exception("Excel read error")

        # Создаем временный Excel файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as f:
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_unsupported_file_format(self) -> None:
        """Тест загрузки файла с неподдерживаемым форматом"""
        # Создаем временный файл с неподдерживаемым форматом
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('some text content')
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_file_extension_case_insensitive(self) -> None:
        """Тест что расширения файлов обрабатываются без учета регистра"""
        # Создаем временные файлы с разными регистрами расширений
        test_cases = [
            ('.json', True),
            ('.JSON', True),
            ('.csv', True),
            ('.CSV', True),
            ('.xlsx', True),
            ('.XLSX', True),
            ('.txt', False),  # неподдерживаемый формат
        ]

        for extension, should_support in test_cases:
            with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as f:
                # Записываем минимальный валидный контент для JSON
                if extension.lower() == '.json':
                    f.write('[]')
                else:
                    f.write('test content')
                temp_path = f.name

            try:
                transactions = load_transactions(temp_path)
                if should_support:
                    # Для поддерживаемых форматов ожидаем либо список, либо ошибку
                    self.assertIsInstance(transactions, list)
                else:
                    # Для неподдерживаемых форматов ожидаем пустой список
                    self.assertEqual(transactions, [])
            finally:
                os.unlink(temp_path)

    @patch('src.utils._load_csv_transactions')
    @patch('src.utils._load_excel_transactions')
    @patch('src.utils._load_json_transactions')
    def test_correct_loader_called(
            self,
            mock_json_loader: Any,
            mock_excel_loader: Any,
            mock_csv_loader: Any
    ) -> None:
        """Тест что для каждого формата вызывается правильный загрузчик"""
        # Настраиваем моки чтобы возвращали пустые списки
        mock_json_loader.return_value = []
        mock_csv_loader.return_value = []
        mock_excel_loader.return_value = []

        # Создаем временные файлы для каждого формата
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as json_file:
            json_file.write('[]')
            json_path = json_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as csv_file:
            csv_file.write('id,amount\n1,100')
            csv_path = csv_file.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as excel_file:
            # Просто создаем пустой файл
            excel_path = excel_file.name

        try:
            # Тестируем JSON
            load_transactions(json_path)
            mock_json_loader.assert_called_once_with(json_path)

            # Сбрасываем мок для следующего теста
            mock_json_loader.reset_mock()

            # Тестируем CSV
            load_transactions(csv_path)
            mock_csv_loader.assert_called_once_with(csv_path)

            # Сбрасываем мок для следующего теста
            mock_csv_loader.reset_mock()

            # Тестируем Excel
            load_transactions(excel_path)
            mock_excel_loader.assert_called_once_with(excel_path)

        finally:
            # Удаляем временные файлы
            os.unlink(json_path)
            os.unlink(csv_path)
            os.unlink(excel_path)

    def test_pandas_not_installed_csv(self) -> None:
        """Тест поведения когда pandas не установлен для CSV"""
        # Создаем временный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write('id,amount\n1,100')
            temp_path = f.name

        try:
            with patch('src.utils.pd', None):  # Эмулируем отсутствие pandas
                transactions = load_transactions(temp_path)
                self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_pandas_not_installed_excel(self) -> None:
        """Тест поведения когда pandas не установлен для Excel"""
        # Создаем временный Excel файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xlsx', delete=False) as f:
            temp_path = f.name

        try:
            with patch('src.utils.pd', None):  # Эмулируем отсутствие pandas
                transactions = load_transactions(temp_path)
                self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)


class TestTransactionAmountInRubles(unittest.TestCase):

    def test_get_transaction_amount_in_rubles_rub(self) -> None:
        """Тест получения суммы в рублях для RUB транзакции"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertEqual(amount, 1000.50)

    def test_get_transaction_amount_in_rubles_usd(self) -> None:
        """Тест получения суммы в рублях для USD транзакции"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsInstance(amount, float)
        # Должен использовать фиксированный курс 90.0
        self.assertEqual(amount, 9000.0)

    def test_get_transaction_amount_in_rubles_invalid_data(self) -> None:
        """Тест обработки невалидных данных транзакции"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "invalid", "currency": {"code": "USD"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_missing_data(self) -> None:
        """Тест обработки отсутствующих данных"""
        transaction: Dict[str, Any] = {}

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_empty_amount(self) -> None:
        """Тест обработки пустой суммы"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_none_amount(self) -> None:
        """Тест обработки None суммы"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": None, "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_missing_currency(self) -> None:
        """Тест обработки отсутствующей валюты"""
        transaction: Dict[str, Any] = {
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
        transaction: Dict[str, Any] = {
            "other_field": "value"
            # Нет operationAmount
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)

    def test_get_transaction_amount_in_rubles_invalid_amount_format(self) -> None:
        """Тест обработки неверного формата суммы"""
        transaction: Dict[str, Any] = {
            "operationAmount": {"amount": "not_a_number", "currency": {"code": "RUB"}}
        }

        amount = get_transaction_amount_in_rubles(transaction)
        self.assertIsNone(amount)


if __name__ == '__main__':
    unittest.main()