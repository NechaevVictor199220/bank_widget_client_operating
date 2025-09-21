import pytest


@pytest.fixture
def sample_card_numbers():
    return {
        "standard": "7000792289606361",
        "visa": "4111111111111111",
        "mastercard": "5555555555554444",
        "short": "1234567890",
        "empty": "",
        "with_spaces": "7000 7922 8960 6361",
        "with_dashes": "7000-7922-8960-6361",
    }


@pytest.fixture
def sample_account_numbers():
    return {
        "standard": "73654108430135874305",
        "short": "1234",
        "empty": "",
        "min_length": "123456",  # 6 символов
        "with_spaces": "7365 4108 4301 3587 4305",
    }


@pytest.fixture
def sample_data():
    return {
        "card_visa": "Visa Platinum 7000792289606361",
        "card_mastercard": "Maestro 7000792289606361",
        "account": "Счет 73654108430135874305",
        "account_english": "Account 73654108430135874305",
        "invalid": "Invalid String",
        "empty": "",
    }


@pytest.fixture
def sample_dates():
    return {
        "standard": "2024-03-11T02:26:18.671407",
        "short_time": "2024-03-11T02:26:18",
        "no_time": "2024-03-11",
        "invalid": "invalid-date",
        "empty": "",
    }


@pytest.fixture
def sample_operations():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "PENDING", "date": "2024-02-10T01:25:17.570306"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T00:24:16.469205"},
        {"id": 4, "state": "CANCELED", "date": "2023-12-08T23:23:15.368104"},
        {"id": 5, "state": "EXECUTED", "date": "2023-11-07T22:22:14.267003"},
        {"id": 6, "date": "2023-10-06T21:21:13.165902"},  # без state
    ]


@pytest.fixture
def operations_with_same_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        {"id": 2, "state": "PENDING", "date": "2024-03-11T02:26:18.671407"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-09T00:24:16.469205"},
    ]


@pytest.fixture
def operations_invalid_dates():
    return [
        {"id": 1, "state": "EXECUTED", "date": "invalid-date"},
        {"id": 2, "state": "PENDING", "date": "2024-02-10T01:25:17.570306"},
        {"id": 3, "state": "EXECUTED", "date": ""},
    ]
