from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Функция принимает строку, содержащую тип и номер карты или счета.
    Возвращает строку с замаскированным номером
    """
    if not account_info:
        return account_info

    parts = account_info.split()
    if "счет" in account_info.lower() or "account" in account_info.lower():
        account_number = parts[-1]
        masked_number = get_mask_account(account_number)
        return " ".join(parts[:-1] + [masked_number])
    else:
        card_number = parts[-1]
        masked_number = get_mask_card_number(card_number)
        return " ".join(parts[:-1] + [masked_number])


def get_date(date_str: str) -> str:
    """
       Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%d.%m.%Y")

    except (ValueError, TypeError):
        return date_str


# if __name__ == "__main__":
#     print(mask_account_card("Maestro 1596837868705199"))
#     print(mask_account_card("Счет 64686473678894779589"))
#     print(mask_account_card("MasterCard 7158300734726758"))
#     print(mask_account_card("Счет 35383033474447895560"))
#     print(mask_account_card("Visa Classic 6831982476737658"))
#     print(mask_account_card("Visa Platinum 8990922113665229"))
#     print(mask_account_card("Visa Gold 5999414228426353"))
#     print(mask_account_card("Счет 73654108430135874305"))
#
# if __name__ == "__main__":
#     print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
#     print(get_date("2023-12-31T23:59:59.999999"))  # 31.12.2023
#     print(get_date("2024-01-01T00:00:00.000000"))  # 01.01.2024
