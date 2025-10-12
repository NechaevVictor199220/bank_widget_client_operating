import json
import os
import tempfile
import unittest
from typing import Any
from unittest.mock import patch

from src.utils import load_transactions


class TestLoadTransactions(unittest.TestCase):

    def test_load_existing_file(self) -> None:
        """Тест загрузки существующего файла"""
        transactions = load_transactions("data/operations.json")
        self.assertIsInstance(transactions, list)
        self.assertGreater(len(transactions), 0)

    def test_file_not_found(self) -> None:
        """Тест загрузки несуществующего файла"""
        transactions = load_transactions("data/nonexistent.json")
        self.assertEqual(transactions, [])

    def test_invalid_json(self) -> None:
        """Тест загрузки файла с некорректным JSON"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_empty_file(self) -> None:
        """Тест загрузки пустого файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            # просто создаем пустой файл
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    def test_not_list_content(self) -> None:
        """Тест загрузки файла с содержимым не списком"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)  # словарь вместо списка
            temp_path = f.name

        try:
            transactions = load_transactions(temp_path)
            self.assertEqual(transactions, [])
        finally:
            os.unlink(temp_path)

    @patch("src.utils.json.load")
    @patch("builtins.open")
    def test_load_transactions_general_exception(self, mock_open: Any, mock_json_load: Any) -> None:
        """Тест обработки общего исключения в load_transactions"""
        mock_open.side_effect = Exception("Unexpected error")

        result = load_transactions("any_file.json")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
