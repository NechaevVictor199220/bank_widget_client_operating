import json
from typing import Any, Dict, List, Optional

from .external_api import convert_to_rubles


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, не найден или содержит не список - возвращает пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except (FileNotFoundError, json.JSONDecodeError):
        # Файл не найден или ошибка декодирования JSON
        return []
    except Exception:
        # Любая другая ошибка
        return []


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции

    Returns:
        Optional[float]: Сумма в рублях или None если не удалось получить сумму
    """
    try:
        # Проверяем наличие необходимых ключей
        if not transaction or "operationAmount" not in transaction:
            return None

        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code", "RUB")

        # Проверяем что amount существует и не пустой
        if amount_str is None or amount_str == "":
            return None

        # Преобразуем строку в float
        amount = float(amount_str)

        # Конвертируем в рубли если нужно
        if currency_code != "RUB":
            amount = convert_to_rubles(amount, currency_code)

        return amount

    except (KeyError, ValueError, TypeError) as e:
        print(f"Ошибка при получении суммы транзакции: {e}")
        return None
