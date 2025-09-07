def get_mask_card_number(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает его маску
    в формате ХХХХХХ******XXXX, где X - это цифры
    """
    if len(card_number) < 16:
        return card_number
    return card_number[:6] + "******" + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску в формате **XXXX,
    где X - это цифры
    """
    if len(account_number) < 20:
        return account_number
    return "**" + account_number[-4:]


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
