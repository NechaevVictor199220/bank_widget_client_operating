import logging



masks_logger = logging.getLogger('masks')
masks_logger.setLevel(logging.INFO)
masks_logger.handlers.clear()
file_handler = logging.FileHandler('logs/masks.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
masks_logger.addHandler(file_handler)
masks_logger.propagate = False


def get_mask_card_number(card_number: str) -> str:
    """
    Функция принимает на вход номер карты и возвращает его маску
    в формате ХХХХХХ******XXXX, где X - это цифры
    """
    masks_logger.info(f"Начало маскировки номера карты: {card_number}")
    if not isinstance(card_number, str):
        masks_logger.error(f"Номер карты содержит недопустимые символы: {card_number}")
        return card_number
    if len(card_number) < 16:
        masks_logger.error(f"Некорректная длина номера карты: {len(card_number)}")
        return card_number
    masks_logger.info(f"Успешная маскировка номера карты: {card_number}")
    return card_number[:6] + "******" + card_number[-4:]


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску в формате **XXXX,
    где X - это цифры
    """
    masks_logger.info(f"Начало маскировки номера счета: {account_number}")
    if not account_number:
        masks_logger.error(f"Номер счета содержит недопустимые символы: {account_number}")
        return account_number
    if len(account_number) < 20:
        masks_logger.error(f"Номер счета слишком короткий: {len(account_number)}")
        return account_number
    masks_logger.info(f"Успешная маскировка номера счета: {account_number}")
    return "**" + account_number[-4:]


# if __name__ == "__main__":
#     print(get_mask_card_number("7000792289606361"))
#     print(get_mask_account("73654108430135874305"))
