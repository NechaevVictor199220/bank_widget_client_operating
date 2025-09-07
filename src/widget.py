from masks import get_mask_card_number, get_mask_account


def mask_account_card(account_info: str) -> str:
         """
     Маскирует номер счета или карты в переданной строке.

     Args:
         account_info: строка с типом и номером карты/счета
         Примеры:
         - "Visa Platinum 7000792289606361"
         - "Счет 73654108430135874305"

     Returns:
         Строка с замаскированным номером
     """
         # Разделяем строку на части
         parts = account_info.split()

         # Определяем тип (последнее слово может быть номером)
         if "счет" in account_info.lower() or "account" in account_info.lower():
             # Это счет - используем маскировку счета
             account_number = parts[-1]
             masked_number = get_mask_account(account_number)
             return " ".join(parts[:-1] + [masked_number])
         else:
             # Это карта - используем маскировку карты
             card_number = parts[-1]
             masked_number = get_mask_card_number(card_number)
             return " ".join(parts[:-1] + [masked_number])

if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 700079******6361
    print(mask_account_card("Maestro 7000792289606361"))  # Maestro 700079******6361
    print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305
    print(mask_account_card("Account 73654108430135874305"))  # Account **4305