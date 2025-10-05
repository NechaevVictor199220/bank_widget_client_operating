import functools
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Подготовка информации о вызове
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                log_message = f"{timestamp} - {func_name} ok\n"

            except Exception as e:
                # Логируем ошибку
                log_message = f"{timestamp} - {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                raise  # Пробрасываем ошибку дальше

            finally:
                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message)
                else:
                    print(log_message, end='')

            return result

        return wrapper

    return decorator