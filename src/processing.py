import re
from collections import Counter
from typing import Dict, List


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
            operation
            for operation in data
            if operation.get("description") and pattern.search(operation["description"])
        ]

        return filtered_operations

    except re.error:
        # В случае ошибки в регулярном выражении возвращаем пустой список
        return []


def count_operations_by_category(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям с использованием Counter.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь, где ключи - названия категорий,
                       значения - количество операций в каждой категории
    """
    if not data or not categories:
        return {}

    # Создаем счетчик для категорий
    category_counter = Counter()

    # Инициализируем счетчик нулевыми значениями для всех категорий
    for category in categories:
        category_counter[category] = 0

    # Проходим по всем операциям
    for operation in data:
        description = operation.get("description")

        # Пропускаем операции без описания или с пустым описанием
        if not description:
            continue

        description_lower = description.lower()

        # Для каждой категории проверяем наличие в описании
        for category in categories:
            if category.lower() in description_lower:
                category_counter[category] += 1

    return dict(category_counter)


def count_operations_by_type_advanced(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Альтернативная реализация с более эффективным использованием Counter.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь с количеством операций по категориям
    """
    if not data or not categories:
        return {}

    # Используем Counter для подсчета
    counter = Counter()

    for operation in data:
        description = operation.get("description", "").lower()

        if not description:
            continue

        # Находим все категории, которые присутствуют в описании
        matching_categories = {cat for cat in categories if cat.lower() in description}

        # Увеличиваем счетчик для каждой найденной категории
        for category in matching_categories:
            counter[category] += 1

    # Гарантируем, что все категории присутствуют в результате (даже с нулем)
    result = {category: 0 for category in categories}
    result.update(counter)

    return result


def get_most_common_categories(data: List[Dict], top_n: int = 5) -> List[tuple]:
    """
    Находит наиболее часто встречающиеся категории в операциях.

    Args:
        data: Список операций
        top_n: Количество самых частых категорий для возврата

    Returns:
        List[tuple]: Список кортежей (категория, количество)
    """
    if not data:
        return []

    # Извлекаем все описания
    descriptions = [op.get("description", "").lower() for op in data if op.get("description")]

    if not descriptions:
        return []

    # Разбиваем описания на слова и подсчитываем частоту
    all_words = []
    for desc in descriptions:
        # Разбиваем на слова, убираем пунктуацию
        words = re.findall(r"\b\w+\b", desc)
        all_words.extend(words)

    # Используем Counter для подсчета частоты слов
    word_counter = Counter(all_words)

    # Исключаем стоп-слова (можно расширить список)
    stop_words = {"в", "на", "с", "и", "или", "для", "по", "из", "от", "до"}
    for word in stop_words:
        word_counter.pop(word, None)

    # Возвращаем top_n самых частых слов
    return word_counter.most_common(top_n)
