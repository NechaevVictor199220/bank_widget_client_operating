# Bank Widget Client Operating

Проект для обработки банковских операций, включая маскировку номеров карт и счетов, фильтрацию и сортировку операций.

## Цель проекта

Создание набора утилит для работы с банковскими данными:
- Маскировка конфиденциальной информации (номера карт и счетов)
- Фильтрация операций по статусу
- Сортировка операций по дате
- Форматирование дат

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
### Импорт модулей
#### python
```
from src.masks import get_mask_account_number, get_mask_card_number

from src.widget import mask_account_card, get_date

from src.processing import filter_by_state, sort_by_date
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
# Тестирование
## Запуск тестов и проверка качества кода:

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
# Форматирование кода
### Проект использует следующие инструменты для поддержания качества кода:

Black - форматирование кода

isort - сортировка импортов

flake8 - проверка стиля

mypy - проверка типов

Конфигурация инструментов находится в файле pyproject.toml.

# Лицензия
Проект распространяется под лицензией MIT.