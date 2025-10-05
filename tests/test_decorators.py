import pytest
import os
import tempfile
from typing import Any
from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log"""

    def test_log_to_console_success(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования успешной операции в консоль"""

        @log()
        def add_numbers(a: int, b: int) -> int:
            return a + b

        result = add_numbers(2, 3)

        # Проверяем результат функции
        assert result == 5

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out
        assert "add_numbers ok" in output
        assert "error" not in output

    def test_log_to_console_with_args_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования функции с аргументами и ключевыми словами"""

        @log()
        def complex_function(a: int, b: int, c: int = 10, d: int = 20) -> int:
            return a + b + c + d

        result = complex_function(1, 2, c=5, d=15)

        assert result == 23

        captured = capsys.readouterr()
        output = captured.out
        assert "complex_function ok" in output

    def test_log_to_console_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования ошибки в консоль"""

        @log()
        def failing_function(x: int) -> None:
            raise ValueError("Test error message")

        # Проверяем, что ошибка пробрасывается
        with pytest.raises(ValueError, match="Test error message"):
            failing_function(5)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        output = captured.out
        assert "failing_function error: ValueError" in output
        assert "Inputs: (5,), {}" in output

    def test_log_to_console_error_with_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест логирования ошибки с аргументами"""

        @log()
        def division(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            division(10, 0)

        captured = capsys.readouterr()
        output = captured.out
        assert "division error: ZeroDivisionError" in output
        assert "Inputs: (10, 0), {}" in output

    def test_log_to_file_success(self) -> None:
        """Тест логирования успешной операции в файл"""

        # Создаем временный файл и сразу закрываем его
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log")
        filename = temp_file.name
        temp_file.close()

        try:
            @log(filename=filename)
            def multiply(a: int, b: int) -> int:
                return a * b

            result = multiply(4, 5)

            # Проверяем результат
            assert result == 20

            # Проверяем запись в файл
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert "multiply ok" in content
                assert "error" not in content

        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_to_file_error(self) -> None:
        """Тест логирования ошибки в файл"""

        # Создаем временный файл и сразу закрываем его
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log")
        filename = temp_file.name
        temp_file.close()

        try:
            @log(filename=filename)
            def raise_custom_error(x: str) -> None:
                raise RuntimeError("Custom error occurred")

            with pytest.raises(RuntimeError):
                raise_custom_error("test_arg")

            # Проверяем запись в файл
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert "raise_custom_error error: RuntimeError" in content
                assert "Inputs: ('test_arg',), {}" in content

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_to_file_append_mode(self) -> None:
        """Тест что логи дописываются в файл, а не перезаписываются"""

        # Создаем временный файл и сразу закрываем его
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log")
        filename = temp_file.name
        temp_file.close()

        try:
            @log(filename=filename)
            def func1(x: int) -> int:
                return x + 1

            @log(filename=filename)
            def func2(x: int) -> int:
                return x * 2

            func1(5)
            func2(10)

            # Проверяем что оба вызова записаны в файл
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.strip().split("\n")
                assert len(lines) == 2
                assert "func1 ok" in lines[0]
                assert "func2 ok" in lines[1]

        finally:
            if os.path.exists(filename):
                os.unlink(filename)

    def test_function_metadata_preserved(self) -> None:
        """Тест сохранения метаданных функции"""

        @log()
        def original_function(x: int, y: int) -> int:
            """Оригинальная документация функции"""
            return x + y

        # Проверяем сохранение метаданных
        assert original_function.__name__ == "original_function"
        assert original_function.__doc__ == "Оригинальная документация функции"
        assert original_function.__annotations__ == {"x": int, "y": int, "return": int}

    def test_decorator_without_parentheses(self) -> None:
        """Тест использования декоратора без скобок"""

        @log
        def simple_function() -> str:
            return "success"

        result = simple_function()
        assert result == "success"

    def test_multiple_functions_same_log_file(self) -> None:
        """Тест нескольких функций с одним файлом логов"""

        # Создаем временный файл и сразу закрываем его
        temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".log")
        filename = temp_file.name
        temp_file.close()

        try:
            @log(filename=filename)
            def add(a: int, b: int) -> int:
                return a + b

            @log(filename=filename)
            def subtract(a: int, b: int) -> int:
                return a - b

            add(10, 5)
            subtract(10, 3)

            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert "add ok" in content
                assert "subtract ok" in content
                assert content.count("ok") == 2

        finally:
            if os.path.exists(filename):
                os.unlink(filename)