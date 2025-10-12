import os
from typing import Dict, Union

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Предупреждение: библиотека requests не установлена. Установите её для работы с API.")


def convert_to_rubles(amount: float, currency_code: str) -> float:
    """
    Конвертирует сумму в рубли, обращаясь к внешнему API для получения курса валют.

    Args:
        amount (float): Сумма для конвертации
        currency_code (str): Код валюты (USD, EUR, RUB и т.д.)

    Returns:
        float: Сумма в рублях
    """
    # Если валюта уже рубли, возвращаем как есть
    if currency_code.upper() == "RUB":
        return amount

    # Проверяем доступность библиотеки requests
    if not REQUESTS_AVAILABLE:
        print("Ошибка: Библиотека requests не установлена")
        return _get_amount_with_fixed_rate(amount, currency_code)

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        print("Ошибка: Не установлен API ключ. Установите переменную окружения EXCHANGE_RATE_API_KEY")
        return _get_amount_with_fixed_rate(amount, currency_code)

    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {"apikey": api_key}

    params: Dict[str, Union[str, int, float]] = {
        "from": currency_code.upper(),
        "to": "RUB",
        "amount": amount,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success", False):
            result = data.get("result")
            if isinstance(result, (int, float)):
                return float(result)
            else:
                print(f"Неверный формат результата: {result}")
                return _get_amount_with_fixed_rate(amount, currency_code)
        else:
            print(f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")
            return _get_amount_with_fixed_rate(amount, currency_code)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return _get_amount_with_fixed_rate(amount, currency_code)
    except (KeyError, ValueError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return _get_amount_with_fixed_rate(amount, currency_code)


def _get_amount_with_fixed_rate(amount: float, currency_code: str) -> float:
    """
    Вспомогательная функция для получения суммы с фиксированным курсом при ошибках API.

    Args:
        amount (float): Сумма для конвертации
        currency_code (str): Код валюты

    Returns:
        float: Сумма в рублях по фиксированному курсу
    """
    fixed_rates = {"USD": 90.0, "EUR": 100.0}
    rate = fixed_rates.get(currency_code.upper(), 1.0)
    print(f"Используется фиксированный курс для {currency_code}: {rate}")
    return amount * rate
