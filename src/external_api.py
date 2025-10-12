import os
from typing import Dict, Optional, Union

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Предупреждение: библиотека requests не установлена. Установите её для работы с API.")


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает текущий курс валюты к рублю через внешнее API.

    Args:
        from_currency (str): Код исходной валюты (например, "USD", "EUR")
        to_currency (str): Код целевой валюты (по умолчанию "RUB")

    Returns:
        Optional[float]: Курс обмена или None в случае ошибки
    """
    if not REQUESTS_AVAILABLE:
        print("Ошибка: Библиотека requests не установлена")
        return None

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        print("Ошибка: Не установлен API ключ. Установите переменную окружения EXCHANGE_RATE_API_KEY")
        return None

    url = "https://api.apilayer.com/exchangerates_data/convert"

    headers = {"apikey": api_key}

    # Исправляем тип params - используем Union для совместимости
    params: Dict[str, Union[str, int]] = {
        "from": from_currency,
        "to": to_currency,
        "amount": 1,  # Получаем курс для 1 единицы валюты
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
                return None
        else:
            print(f"Ошибка API: {data.get('error', {}).get('info', 'Неизвестная ошибка')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Ошибка при обработке ответа API: {e}")
        return None


# Кэш курсов валют чтобы не делать лишние запросы
_exchange_rates_cache: Dict[str, float] = {}


def convert_to_rubles(amount: float, currency_code: str) -> float:
    """
    Конвертирует сумму в рубли.

    Args:
        amount (float): Сумма для конвертации
        currency_code (str): Код валюты (USD, EUR, RUB и т.д.)

    Returns:
        float: Сумма в рублях
    """
    # Если валюта уже рубли, возвращаем как есть
    if currency_code.upper() == "RUB":
        return amount

    cache_key = f"{currency_code.upper()}_RUB"

    # Проверяем кэш
    if cache_key not in _exchange_rates_cache:
        rate = get_exchange_rate(currency_code.upper(), "RUB")
        if rate is None:
            # Если не удалось получить курс, используем фиксированные значения
            fixed_rates = {"USD": 90.0, "EUR": 100.0}
            rate = fixed_rates.get(currency_code.upper(), 1.0)
            print(f"Используется фиксированный курс для {currency_code}: {rate}")

        _exchange_rates_cache[cache_key] = rate

    return amount * _exchange_rates_cache[cache_key]
