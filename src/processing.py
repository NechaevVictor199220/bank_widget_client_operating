from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Функция возвращает новый список словарей, содержащий только те словари,
    у которых ключ state соответствует указанному значению.
    """
    return [operation for operation in operations if operation.get("state") == state]


# Примеры использования с предоставленными данными
if __name__ == "__main__":
    # Входные данные из примера
    operations = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    # Тестирование со статусом по умолчанию 'EXECUTED'
    executed_ops = filter_by_state(operations)
    print("EXECUTED operations:")
    for op in executed_ops:
        print(op)

    print("\n" + "=" * 50 + "\n")

    # Тестирование с статусом 'CANCELED'
    canceled_ops = filter_by_state(operations, "CANCELED")
    print("CANCELED operations:")
    for op in canceled_ops:
        print(op)

    print("\n" + "=" * 50 + "\n")

    # Тестирование с несуществующим статусом
    pending_ops = filter_by_state(operations, "PENDING")
    print("PENDING operations:", pending_ops)  # Должен быть пустой список
