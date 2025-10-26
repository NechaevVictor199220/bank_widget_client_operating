import os
import sys
from typing import Any, Dict, List, Optional

from src.processing import count_operations_by_category, filter_by_description, filter_by_state, sort_by_date
from src.utils import get_transaction_amount_in_rubles, load_transactions
from src.widget import get_date, mask_account_card

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


def clear_screen() -> None:
    """Очищает экран консоли"""
    os.system("cls" if os.name == "nt" else "clear")


def print_welcome() -> None:
    """Выводит приветственное сообщение"""
    print("=" * 60)
    print("Привет! Добро пожаловать в программу работы")
    print("с банковскими транзакциями.")
    print("=" * 60)


def get_file_choice() -> str:
    """Получает выбор файла от пользователя"""
    print("\nВыберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    print("4. Выйти из программы")

    while True:
        choice = input("\nВаш выбор (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("❌ Неверный выбор. Пожалуйста, введите 1, 2, 3 или 4.")


def get_file_path(choice: str) -> Optional[str]:
    """Возвращает путь к файлу на основе выбора пользователя"""
    if choice == "4":
        return None

    file_map = {"1": "data/operations.json", "2": "data/transactions.csv", "3": "data/transactions_excel.xlsx"}

    file_names = {"1": "JSON-файл", "2": "CSV-файл", "3": "XLSX-файл"}

    file_path = file_map.get(choice)
    file_name = file_names.get(choice, "файл")

    print(f"\n✅ Для обработки выбран {file_name}.")
    return file_path


def get_status_filter() -> str:
    """Получает статус для фильтрации от пользователя"""
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(available_statuses)}")
        print("Или введите 'назад' для возврата к выбору файла")

        status = input("Статус: ").strip()

        if status.lower() == "назад":
            return "назад"

        status_upper = status.upper()
        if status_upper in available_statuses:
            print(f"✅ Операции отфильтрованы по статусу '{status_upper}'")
            return status_upper
        else:
            print(f"❌ Статус операции '{status}' недоступен.")


def get_yes_no_input(question: str) -> bool:
    """Получает ответ Да/Нет от пользователя"""
    while True:
        answer = input(f"\n{question} (Да/Нет): ").strip().lower()
        if answer in ["да", "д", "yes", "y", ""]:
            return True
        elif answer in ["нет", "н", "no", "n"]:
            return False
        else:
            print("❌ Пожалуйста, введите 'Да' или 'Нет'")


def get_sort_direction() -> bool:
    """Получает направление сортировки от пользователя"""
    while True:
        direction = input("\nОтсортировать по возрастанию или по убыванию? ").strip().lower()
        if direction in ["по возрастанию", "возрастанию", "asc", "ascending", ""]:
            return False  # по возрастанию
        elif direction in ["по убыванию", "убыванию", "desc", "descending"]:
            return True  # по убыванию
        else:
            print("❌ Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def get_search_word() -> Optional[str]:
    """Получает слово для поиска в описании"""
    while True:
        answer = input("\nВведите слово для поиска в описании (или Enter для пропуска): ").strip()
        if not answer:
            return None
        elif len(answer) < 2:
            print("❌ Слишком короткое слово для поиска. Минимум 2 символа.")
        else:
            return answer


def format_amount(transaction: Dict[str, Any]) -> str:
    """Форматирует сумму для отображения"""
    amount_info = transaction.get("operationAmount", {})
    amount = amount_info.get("amount", "0")
    currency_info = amount_info.get("currency", {})
    currency_name = currency_info.get("name", "")

    # Пытаемся конвертировать в рубли для единообразия
    try:
        amount_rub = get_transaction_amount_in_rubles(transaction)
        if amount_rub is not None:
            return f"{amount_rub:.2f} руб. (оригинал: {amount} {currency_name})"
    except (ValueError, KeyError, TypeError):
        pass

    return f"{amount} {currency_name}"


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для красивого вывода"""
    # Дата
    date_str = get_date(transaction.get("date", "")) if transaction.get("date") else "Дата не указана"

    # Описание
    description = transaction.get("description", "Описание отсутствует")

    # От кого
    from_str = ""
    if "from" in transaction:
        from_str = mask_account_card(transaction["from"])

    # Кому
    to_str = ""
    if "to" in transaction:
        to_str = mask_account_card(transaction["to"])

    # Сумма
    amount_str = format_amount(transaction)

    # Формируем вывод
    lines = []
    lines.append(f"📅 {date_str} | {description}")

    if from_str and to_str:
        lines.append(f"   📤 {from_str}")
        lines.append(f"   📥 {to_str}")
    elif from_str:
        lines.append(f"   📤 {from_str}")
    elif to_str:
        lines.append(f"   📥 {to_str}")

    lines.append(f"   💰 Сумма: {amount_str}")
    lines.append("")  # пустая строка для разделения

    return "\n".join(lines)


def show_transaction_statistics(transactions: List[Dict[str, Any]]) -> None:
    """Показывает статистику по транзакциям"""
    if not transactions:
        return

    print("\n📊 Статистика выборки:")
    print("-" * 40)

    # Подсчет по категориям
    common_categories = ["Перевод", "Оплата", "Пополнение", "Снятие", "Карта"]
    category_stats = count_operations_by_category(transactions, common_categories)

    print("Операции по типам:")
    for category, count in category_stats.items():
        if count > 0:
            percentage = (count / len(transactions)) * 100
            print(f"  {category}: {count} ({percentage:.1f}%)")

    # Суммарная информация
    total_amount = 0
    for transaction in transactions:
        amount_rub = get_transaction_amount_in_rubles(transaction)
        if amount_rub:
            total_amount += amount_rub

    print(f"\n💰 Общая сумма: {total_amount:.2f} руб.")
    print(f"📈 Средняя сумма: {total_amount / len(transactions):.2f} руб.")


def process_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Основной процесс обработки транзакций"""
    if not transactions:
        print("\n❌ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\n{'=' * 60}")
    print("📋 Распечатываю итоговый список транзакций...")
    print(f"{'=' * 60}")
    print(f"📊 Всего банковских операций в выборке: {len(transactions)}\n")

    for i, transaction in enumerate(transactions, 1):
        print(f"--- Операция {i} ---")
        print(format_transaction(transaction))

    # Показываем статистику
    show_transaction_statistics(transactions)


def process_file_selection() -> Optional[List[Dict[str, Any]]]:
    """Обрабатывает выбор файла и загрузку данных"""
    file_choice = get_file_choice()

    if file_choice == "4":
        return None

    file_path = get_file_path(file_choice)

    if not file_path:
        return None

    # Проверяем существование файла
    if not os.path.exists(file_path):
        print(f"❌ Файл '{file_path}' не найден.")
        print("Убедитесь, что файл существует в папке data/")
        return None

    # Загрузка транзакций
    print("\n🔄 Загружаю транзакции...")
    all_transactions = load_transactions(file_path)

    if not all_transactions:
        print("❌ Не удалось загрузить транзакции из файла.")
        print("Возможные причины:")
        print("  - Файл пустой")
        print("  - Неправильный формат файла")
        print("  - Ошибка чтения файла")
        return None

    print(f"✅ Загружено {len(all_transactions)} транзакций")
    return all_transactions


def apply_filters(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Применяет фильтры к транзакциям на основе выбора пользователя"""
    current_transactions = transactions

    # Фильтрация по статусу
    while True:
        status = get_status_filter()
        if status == "назад":
            return None  # Сигнал для возврата

        filtered_transactions = filter_by_state(current_transactions, status)

        if not filtered_transactions:
            print(f"\n❌ Не найдено операций с статусом '{status}'.")
            print("Попробуйте выбрать другой статус.")
            continue
        else:
            print(f"✅ Найдено {len(filtered_transactions)} операций с статусом '{status}'")
            current_transactions = filtered_transactions
            break

    # Сортировка по дате
    if get_yes_no_input("Отсортировать операции по дате?"):
        reverse = get_sort_direction()
        current_transactions = sort_by_date(current_transactions, reverse=reverse)
        direction = "убыванию" if reverse else "возрастанию"
        print(f"✅ Операции отсортированы по {direction}")

    # Фильтрация по валюте
    if get_yes_no_input("Выводить только рублевые транзакции?"):
        ruble_transactions = []
        for transaction in current_transactions:
            operation_amount = transaction.get("operationAmount", {})
            currency_code = operation_amount.get("currency", {}).get("code", "")
            if currency_code == "RUB":
                ruble_transactions.append(transaction)

        if ruble_transactions:
            current_transactions = ruble_transactions
            print(f"✅ Оставлены только рублевые транзакции: {len(current_transactions)} операций")
        else:
            print("ℹ️  Рублевых транзакций не найдено, показываю все")

    # Фильтрация по описанию
    if get_yes_no_input("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = get_search_word()
        if search_word:
            searched_transactions = filter_by_description(current_transactions, search_word)
            if searched_transactions:
                current_transactions = searched_transactions
                print(f"✅ Отфильтровано по слову '{search_word}': {len(current_transactions)} операций")
            else:
                print(f"ℹ️  Операций со словом '{search_word}' не найдено")

    return current_transactions


def main() -> None:
    """Основная функция программы"""
    clear_screen()
    print_welcome()

    try:
        while True:
            # Выбор и загрузка файла
            all_transactions = process_file_selection()
            if all_transactions is None:
                break

            # Применение фильтров
            filtered_transactions = apply_filters(all_transactions)
            if filtered_transactions is None:
                continue  # Вернуться к выбору файла

            # Вывод результатов
            process_transactions(filtered_transactions)

            # Предложение продолжить
            if not get_yes_no_input("\nХотите выполнить еще один запрос?"):
                break

            clear_screen()
            print_welcome()

    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем.")
    except Exception as e:
        print(f"\n❌ Произошла неожиданная ошибка: {e}")
        print("Пожалуйста, сообщите об этой ошибке разработчику.")
    finally:
        print("\n" + "=" * 60)
        print("Спасибо за использование программы! До свидания!")
        print("=" * 60)


if __name__ == "__main__":
    main()
