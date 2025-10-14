import json
import logging
from typing import Any, Dict, List, Optional
from .external_api import convert_to_rubles


utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.INFO)
utils_logger.handlers.clear()
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
utils_logger.addHandler(file_handler)
utils_logger.propagate = False


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает данные о финансовых транзакциях из JSON-файла.

    Args:
        file_path (str): Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
                              Если файл пустой, не найден или содержит не список - возвращает пустой список.
    """
    utils_logger.info(f"Начало загрузки транзакций из файла: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Проверяем, что данные являются списком
            if isinstance(data, list):
                utils_logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
                return data
            else:
                utils_logger.warning(f"Файл {file_path} не содержит список. Загружено: {type(data)}")
                return []

    except FileNotFoundError:
        # Файл не найден
        utils_logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        # ошибка декодирования JSON
        utils_logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except Exception as e:
        # Любая другая ошибка
        utils_logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {str(e)}")
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
        print(f"Ошибка при получении суммы транзакции: {e}")
        return None
