from typing import Any, Dict, Generator, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте операции.

    Args:
        transactions: список словарей с транзакциями
        currency_code: код валюты для фильтрации (например, "USD", "EUR", "RUB")

    Returns:
        Итератор, который выдает транзакции с заданной валютой
    """
    for transaction in transactions:
        # Проверяем наличие валюты в операции
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})

        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой транзакции по очереди.

    Args:
        transactions: список словарей с транзакциями

    Returns:
        Итератор, который выдает описание каждой транзакции
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        yield description


# # Пример использования с предоставленными данными
# if __name__ == "__main__":
#     # Пример данных транзакций
#     transactions = [
#         {
#             "id": 939719570,
#             "state": "EXECUTED",
#             "date": "2018-06-30T02:08:58.425572",
#             "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод организации",
#             "from": "Счет 75106830613657916952",
#             "to": "Счет 11776614605963066702",
#         },
#         {
#             "id": 142264268,
#             "state": "EXECUTED",
#             "date": "2019-04-04T23:20:05.206878",
#             "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 19708645243227258542",
#             "to": "Счет 75651667383060284188",
#         },
#         {
#             "id": 873106923,
#             "state": "EXECUTED",
#             "date": "2019-03-23T01:09:46.296404",
#             "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод со счета на счет",
#             "from": "Счет 44812258784861134719",
#             "to": "Счет 74489636417521191160",
#         },
#         {
#             "id": 895315941,
#             "state": "EXECUTED",
#             "date": "2018-08-19T04:27:37.904916",
#             "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
#             "description": "Перевод с карты на карту",
#             "from": "Visa Classic 6831982476737658",
#             "to": "Visa Platinum 8990922113665229",
#         },
#         {
#             "id": 594226727,
#             "state": "CANCELED",
#             "date": "2018-09-12T21:27:25.241689",
#             "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
#             "description": "Перевод организации",
#             "from": "Visa Platinum 1246377376343588",
#             "to": "Счет 14211924144426031657",
#         },
#     ]
#
#     usd_transactions = filter_by_currency(transactions, "USD")
#     eru_transactions = filter_by_currency(transactions, "EUR")
#     rub_transactions = filter_by_currency(transactions, "RUB")
#
#     print("Первые 2 USD транзакции:")
#     for _ in range(2):
#         try:
#             transaction = next(usd_transactions)
#             print(transaction)
#             print("-" * 50)
#         except StopIteration:
#             print("Больше нет USD транзакций")
#             break
#
#     descriptions = transaction_descriptions(transactions)
#
#     print("Описания первых 5 транзакций:")
#     for i in range(5):
#         try:
#             description = next(descriptions)
#             print(f"{i + 1}. {description}")
#         except StopIteration:
#             print("Больше нет транзакций")
#             break


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start: начальный номер (от 1)
        end: конечный номер (до 9999999999999999)

    Yields:
        Номер карты в формате XXXX XXXX XXXX XXXX
    """
    # Проверка валидности диапазона
    if start < 1:
        raise ValueError("Начальный номер должен быть не менее 1")
    if end > 9999999999999999:
        raise ValueError("Конечный номер не может превышать 9999999999999999")
    if start > end:
        raise ValueError("Начальный номер не может быть больше конечного")

    for number in range(start, end + 1):
        # Форматируем число в 16-значную строку с ведущими нулями
        card_num_str = str(number).zfill(16)

        # Разбиваем на группы по 4 цифры
        formatted_card = " ".join([card_num_str[i : i + 4] for i in range(0, 16, 4)])

        yield formatted_card


# print("Пример из задания (1-5):")
# for card_number in card_number_generator(1, 5):
#     print(card_number)
#
# print("\n" + "=" * 50)
