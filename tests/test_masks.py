import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_standard(sample_card_numbers):
    assert get_mask_card_number(sample_card_numbers["standard"]) == "700079******6361"


def test_get_mask_card_number_visa(sample_card_numbers):
    assert get_mask_card_number(sample_card_numbers["visa"]) == "411111******1111"


@pytest.mark.parametrize("card_number,expected", [
    ("1234567890123456", "123456******3456"),  # 16 цифр
    ("123456789012345", "123456789012345"),    # 15 цифр
    ("12345678901234567", "123456******4567"), # 17 цифр
    ("", ""),  # пустая строка
    (None, None),  # None
    (1234567812345678, 1234567812345678),  # число
])


def test_get_mask_card_number_parametrized(card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_account_number_standard(sample_account_numbers):
    assert get_mask_account(sample_account_numbers["standard"]) == "**4305"


def test_get_mask_account_number_short(sample_account_numbers):
    assert get_mask_account(sample_account_numbers["short"]) == "1234"


@pytest.mark.parametrize("account_number,expected", [
    ("73654108430135874305", "**4305"),  # стандартный
    ("12345678901234567890", "**7890"),  # 20 цифр
    ("1234", "1234"),  # меньше 4 цифр
    ("123", "123"),  # 3 цифры
    ("", ""),  # пустая строка
    (None, None),  # None
])
def test_get_mask_account_number_parametrized(account_number, expected):
    assert get_mask_account(account_number) == expected