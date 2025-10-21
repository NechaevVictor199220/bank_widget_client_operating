import re
from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operation: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Функция sort_by_date, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращает новый список, отсортированный по дате (date).
    """

    def get_date_key(operation: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для получения даты из операции"""
        date_str = operation.get("date", "")
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            # Если дата некорректна, возвращаем минимальную дату
            return datetime.min

    return sorted(operation, key=get_date_key, reverse=reverse)


def filter_by_description(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует операции по строке поиска в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операции

    Returns:
        List[Dict]: Список операций, у которых в описании есть данная строка
    """
    if not data or not search:
        return []

    try:
        # Создаем регулярное выражение для поиска (регистронезависимое)
        pattern = re.compile(re.escape(search), re.IGNORECASE)

        # Фильтруем операции, где описание соответствует регулярному выражению
        filtered_operations = [
            operation for operation in data
            if operation.get("description") and pattern.search(operation["description"])
        ]

        return filtered_operations

    except re.error:
        # В случае ошибки в регулярном выражении возвращаем пустой список
        return []
