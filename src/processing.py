import re
from typing import List, Dict, Any


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED').
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Функция sort_by_date, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращает новый список, отсортированный по дате (date).
    """

    def get_sort_key(operation: Dict) -> str:
        date = operation.get("date")
        # Если дата None или пустая, используем пустую строку для сортировки
        return date if date else ""

    return sorted(
        operations,
        key=get_sort_key,
        reverse=reverse,
    )


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


def count_operations_by_category(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь, где ключи - названия категорий,
                       значения - количество операций в каждой категории
    """
    if not data or not categories:
        return {}

    # Инициализируем словарь с нулевыми значениями для всех категорий
    category_counts = {category: 0 for category in categories}

    for operation in data:
        description = operation.get("description")

        # Пропускаем операции без описания или с None описанием
        if not description:
            continue

        description = description.lower()

        # Проверяем каждую категорию на наличие в описании операции
        for category in categories:
            # Регистронезависимый поиск категории в описании
            if category.lower() in description:
                category_counts[category] += 1

    return category_counts