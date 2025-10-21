# Проект для обработки банковских операций
Проект для обработки банковских операций,
включая маскировку номеров карт и счетов, фильтрацию и сортировку операций.
## Цель проекта

Создание набора утилит для работы с банковскими данными:
- Маскировка конфиденциальной информации (номера карт и счетов)
- Фильтрация операций по статусу
- Сортировка операций по дате
- Форматирование дат
- Логирование вызовов функций
- Автоматическая конвертация через внешнее API
- Поиск операций по описанию с использованием регулярных выражений
- Статистика операций по категориям
## Поддержка форматов файлов

Проект поддерживает загрузку транзакций из различных форматов:

```python
from src.utils import load_transactions

# JSON формат
transactions_json = load_transactions('data/operations.json')

# CSV формат  
transactions_csv = load_transactions('data/transactions.csv')

# Excel формат
transactions_excel = load_transactions('data/transactions.xlsx')
```
## Установка

### Требования
- Python 3.13+
- Poetry (для управления зависимостями)

# Установка зависимостей


### Клонирование репозитория
```
git clone <url-репозитория>
cd bank_widget_client_operating
```
### Установка зависимостей через Poetry
```
poetry install
```
### Активация виртуального окружения
```
poetry shell
```
## Структура проекта
```
src/
├── masks.py          # Функции маскировки карт и счетов
├── widget.py         # Основные функции обработки данных
├── processing.py     # Функции фильтрации и сортировки
├── decorators.py # Декораторы для логирования
├── utils.py # Утилиты для работы с файлами и транзакциями
├── external_api.py # Функции для работы с внешними API
├── main.py           # Основная логика приложения
└── logger_config.py # Конфигурация логирования

tests/
├── test_masks.py     # Тесты для модуля masks
├── test_widget.py # Тесты для модуля widget
├── test_processing.py # Тесты для модуля processing
├── test_decorators.py # Тесты для модуля decorators
├── test_utils.py # Тесты для модуля utils
├── test_main.py       #Тесты основной логики приложения
└── test_external_api.py # Тесты для модуля external_api

data/
├── operations.json # Пример данных в JSON формате
├── transactions.csv # Пример данных в CSV формате
└── transactions_excel.xlsx # Пример данных в Excel формате
logs/ # Папка для файлов логов (создается автоматически)
```
## Использование
### Импорт модулей
```
from src.masks import get_mask_account_number, get_mask_card_number

from src.widget import mask_account_card, get_date

from src.processing import filter_by_state, sort_by_date

from src.decorators import log
```
# Примеры работы
## Маскировка номеров карт и счетов
### python
#### Маскировка номера карты

```
masked_card = get_mask_card_number("7000792289606361")
print(masked_card)  # 700079******6361
```

#### Маскировка номера счета
```
masked_account = get_mask_account_number("73654108430135874305")
print(masked_account)  # **4305
```
#### Универсальная маскировка
```
result = mask_account_card("Visa Platinum 7000792289606361")
print(result)  # Visa Platinum 700079******6361

result = mask_account_card("Счет 73654108430135874305")
print(result)  # Счет **4305
```
### Форматирование дат
#### python
```
formatted_date = get_date("2024-03-11T02:26:18.671407")
print(formatted_date)  # 11.03.2024
```

### Фильтрация операций
#### python
```
operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T00:00:00.000000'},
    {'id': 2, 'state': 'CANCELED', 'date': '2024-01-02T00:00:00.000000'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-03T00:00:00.000000'}
]
```
### Фильтрация по выполненным операциям
```
executed_ops = filter_by_state(operations)
print(executed_ops)  # [{'id': 1, ...}, {'id': 3, ...}]
```
### Фильтрация по отмененным операциям
```
canceled_ops = filter_by_state(operations, 'CANCELED')
print(canceled_ops)  # [{'id': 2, ...}]
```
### Сортировка операций
#### python
### Сортировка по убыванию (новые сначала)
```sorted_desc = sort_by_date(operations)
for op in sorted_desc:
    print(f"{op['date']} - {op['id']}")
```
### Сортировка по возрастанию (старые сначала)
```
sorted_asc = sort_by_date(operations, reverse=False)
for op in sorted_asc:
    print(f"{op['date']} - {op['id']}")
```
## Логирование функций с декоратором @log
### Базовое использование (вывод в консоль)
```
@log
def process_transaction(amount: float, account: str) -> str:
    return f"Processed {amount} to {account}"

result = process_transaction(1000.0, "1234567890")
# Вывод: [2024-03-11 10:30:45] Вызов функции: process_transaction
#         [2024-03-11 10:30:45] Функция process_transaction выполнена успешно
```
### Логирование в файл

```
@log(filename="operations.log")
def transfer_funds(source: str, target: str, amount: float) -> bool:
    # логика перевода
    return True

transfer_funds("1234", "5678", 500.0)
# Запись в файл operations.log
```
### Логирование с кастомным сообщением

```@log(msg="Важная банковская операция")
def critical_operation() -> None:
    # важная логика
    pass

critical_operation()
# Вывод: [2024-03-11 10:30:45] Вызов функции: Важная банковская операция
```

# Логирование ошибок

```
@log
def risky_operation() -> None:
    raise ValueError("Недостаточно средств")

try:
    risky_operation()
except ValueError:
    pass
# Вывод: [2024-03-11 10:30:45] Ошибка в функции risky_operation: Недостаточно средств
```

## Конвертация валют

```python
from src.utils import get_transaction_amount_in_rubles

transaction = {
    "operationAmount": {
        "amount": "100.00", 
        "currency": {"code": "USD"}
    }
}

amount_in_rubles = get_transaction_amount_in_rubles(transaction)
# Автоматическая конвертация через внешнее API
```

# Тестирование
## Запуск тестов и проверка качества кода:
### Запуск всех тестов
```poetry run pytest ```
### Запуск тестов с покрытием
```poetry run pytest --cov```
### Запуск тестов для конкретного модуля
```
# Тесты для масок
poetry run pytest tests/test_masks.py -v

# Тесты для виджета
poetry run pytest tests/test_widget.py -v

# Тесты для обработки
poetry run pytest tests/test_processing.py -v

# Тесты для декораторов
poetry run pytest tests/test_decorators.py -v

# Тесты для конвертаций
poetry run pytest tests/test_external_api.py -v

# Тесты для генераторов
poetry run pytest tests/test_generators.py -v

# Тесты для обработки данных
poetry run pytest tests/test_utils.py -v
```
### Запуск flake8 для проверки стиля
```
poetry run flake8 src/
```
### Запуск mypy для проверки типов
```
poetry run mypy src/
```
### Запуск black для форматирования кода
```
poetry run black src/
```
### Запуск isort для сортировки импортов
```
poetry run isort src/
```
## Описание тестов
### Модуль test_masks.py
* Тестирование маскировки карт: проверка корректности маскирования для карт разной длины

* Тестирование маскировки счетов: проверка обработки счетов различной длины

* Граничные случаи: пустые строки, None значения, некорректные данные

### Модуль widget.py
* Универсальная маскировка: проверка автоматического определения типа данных (карта/счет)

* Форматирование дат: конвертация из ISO формата в "ДД.ММ.ГГГГ"

* Обработка ошибок: некорректные входные данные, пустые строки

### Модуль processing.py
* Фильтрация операций: фильтрация по статусу (EXECUTED, PENDING, CANCELED)

* Сортировка по дате: сортировка по возрастанию/убыванию с обработкой невалидных дат

* Граничные случаи: операции без ключей, пустые списки, одинаковые даты

* Поиск по описанию: тестирование работы с регулярными выражениями

* Статистика по категориям: проверка подсчета операций
### Модуль test_decorators.py
* Логирование в консоль: проверка вывода успешных операций и ошибок

* Логирование в файл: проверка записи в файл и режима дополнения

* Сохранение метаданных: проверка сохранения имени, документации и аннотаций функций

* Использование без скобок: проверка работы декоратора как @log и @log()

### Модуль test_utils.py
* Загрузка данных из разных форматов: JSON, CSV, Excel

* Конвертация сумм транзакций в рубли

* Обработка ошибок при работе с файлами

### Модуль test_external_api.py  
* Тестирование работы с внешним API курсов валют

* Обработка сетевых ошибок и невалидных ответов

* Кэширование курсов валют

# Форматирование кода
### Проект использует следующие инструменты для поддержания качества кода:

Black - форматирование кода

isort - сортировка импортов

flake8 - проверка стиля

mypy - проверка типов

Конфигурация инструментов находится в файле pyproject.toml.

# Лицензия
Проект распространяется под лицензией MIT.