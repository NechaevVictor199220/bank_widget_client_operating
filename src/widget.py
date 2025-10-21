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
    if date_str is None or date_str == "":
        return "Дата не указана"

    try:
        # Пытаемся распарсить дату
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        return "Дата не указана"
