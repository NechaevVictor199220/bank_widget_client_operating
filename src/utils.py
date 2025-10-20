import json
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
from .external_api import convert_to_rubles
import os
import pandas as pd


utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)
utils_logger.handlers.clear()
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
utils_logger.addHandler(file_handler)
utils_logger.propagate = False


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON, CSV или XLSX файла.

    Args:
        file_path (str): Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, не найден или содержит не список - возвращает пустой список.
    """
    if not os.path.exists(file_path):
        utils_logger.error(f"Файл не найден: {file_path}")
        return []

    # Определяем тип файла по расширению
    file_extension = Path(file_path).suffix.lower()

    try:
        if file_extension == '.json':
            return _load_json_transactions(file_path)
        elif file_extension == '.csv':
            return _load_csv_transactions(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            return _load_excel_transactions(file_path)
        else:
            utils_logger.error(f"Неподдерживаемый формат файла: {file_extension}")
            return []

    except Exception as e:
        utils_logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {str(e)}")
        return []


def _load_json_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON файла.

    Args:
        file_path (str): Путь к JSON файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций
    """
    utils_logger.info(f"Загрузка JSON файла: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

        if isinstance(data, list):
            utils_logger.info(f"Успешно загружено {len(data)} транзакций из JSON файла")
            return data
        else:
            utils_logger.warning(f"JSON файл {file_path} не содержит список. Загружено: {type(data)}")
            return []


def _load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из CSV файла.

    Args:
        file_path (str): Путь к CSV файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций
    """
    try:

        utils_logger.info(f"Загрузка CSV файла: {file_path}")

        # Читаем CSV файл
        df = pd.read_csv(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        utils_logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV файла")
        return transactions

    except ImportError:
        utils_logger.error("Библиотека pandas не установлена. Установите её для работы с CSV файлами.")
        return []
    except Exception as e:
        utils_logger.error(f"Ошибка при загрузке CSV файла {file_path}: {str(e)}")
        return []


def _load_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из Excel файла.

    Args:
        file_path (str): Путь к Excel файлу

    Returns:
        List[Dict[str, Any]]: Список транзакций
    """
    try:
        import pandas as pd

        utils_logger.info(f"Загрузка Excel файла: {file_path}")

        # Читаем Excel файл (первый лист по умолчанию)
        df = pd.read_excel(file_path)

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        utils_logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel файла")
        return transactions

    except ImportError:
        utils_logger.error("Библиотека pandas не установлена. Установите её для работы с Excel файлами.")
        return []
    except Exception as e:
        utils_logger.error(f"Ошибка при загрузке Excel файла {file_path}: {str(e)}")
        return []


def get_transaction_amount_in_rubles(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Возвращает сумму транзакции в рублях.

    Args:
        transaction (Dict[str, Any]): Словарь с данными транзакции

    Returns:
        Optional[float]: Сумма в рублях или None если не удалось получить сумму
    """
    utils_logger.info("Начало получения суммы транзакции в рублях")

    try:
        # Проверяем наличие необходимых ключей
        if not transaction or "operationAmount" not in transaction:
            utils_logger.warning("Транзакция не содержит operationAmount")
            return None

        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount")
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code", "RUB")

        # Проверяем что amount существует и не пустой
        if amount_str is None or amount_str == "":
            utils_logger.warning("Сумма транзакции пустая или отсутствует")
            return None

        # Преобразуем строку в float
        amount = float(amount_str)

        utils_logger.info(f"Сумма транзакции: {amount} {currency_code}")

        # Конвертируем в рубли если нужно
        if currency_code != "RUB":
            utils_logger.info(f"Конвертация из {currency_code} в RUB")
            amount = convert_to_rubles(amount, currency_code)
            utils_logger.info(f"Сумма после конвертации: {amount} RUB")
        else:
            utils_logger.info("Транзакция уже в RUB, конвертация не требуется")

        return amount

    except (KeyError, ValueError, TypeError) as e:
        utils_logger.error(f"Ошибка при получении суммы транзакции: {str(e)}")
        return None