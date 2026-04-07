import pytest
from typing import List, Tuple


def decrypt(encryption: str) -> str:
    result: list = []
    dots: int = 0
    for symbol in encryption:
        if symbol != '.':
            result.append(symbol)
            dots = 0
            continue

        dots += 1
        if dots == 2 and result:
            result.pop()
            dots = 0

    return ''.join(result)


# ===================== ТЕСТЫ =====================

class TestDecryptor:
    """Класс с тестами для дешифратора"""

    # Группа 1: Базовые случаи из задания
    def test_basic_cases_from_spec(self):
        """Тесты базовых случаев из спецификации"""
        test_cases: List[Tuple[str, str]] = [
            ("абра-кадабра.", "абра-кадабра"),
            ("абраа..-кадабра", "абра-кадабра"),
            (" абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
            ("абра........", ""),
            ("абр......a.", "a"),
            ("1..2.3", "23"),
            (".", ""),
            ("1.......................", ""),
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    # Группа 2: Тесты с разным количеством точек
    def test_single_dot_deletion(self):
        """Тесты с одной точкой (должна удалять 1 символ)"""
        test_cases: List[Tuple[str, str]] = [
            ("a.", ""),
            ("ab.", "a"),
            ("abc.", "ab"),
            ("hello.", "hello"),
            ("a.b", "b"),
            ("a.b.", ""),
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    def test_multiple_dots_deletion(self):
        """Тесты с двумя и более точками подряд"""
        test_cases: List[Tuple[str, str]] = [
            ("a..", ""),        # 2 точки удаляют 1 символ (по вашему алгоритму)
            ("ab..", ""),       # 2 точки удаляют 1 символ
            ("abc..", "a"),     # 2 точки удаляют 1 символ
            ("a...", ""),       # 3 точки: первые 2 удаляют символ, третья игнорируется
            ("ab...", ""),      # 4 точки: по 2 точки на каждый символ
            ("abcd....", ""),   # 4 точки удаляют 2 символа
            ("a.....", ""),     # 5 точек: 4 точки удаляют 2 символа, 1 точка игнор
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    def test_mixed_symbols_and_dots(self):
        """Тесты со смешанными символами и точками"""
        test_cases: List[Tuple[str, str]] = [
            ("a.b.c", "c"),
            ("1.2.3", "3"),
            ("hello..world", "helloorld"),
            ("test..123..", "te1"),
            ("a..b..c", "c"),
            ("123..45..6", "16"),
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    def test_edge_cases(self):
        """Тесты граничных случаев"""
        test_cases: List[Tuple[str, str]] = [
            ("", ""),                    # Пустая строка
            ("...", ""),                 # Только точки
            (".....", ""),               # Много точек
            (".a", "a"),                 # Точка в начале
            ("a.", ""),                  # Точка в конце
            ("..a", "a"),                # Две точки перед символом
            ("a..", ""),                 # Две точки после символа
            ("...a...", ""),             # Точки вокруг символа
            ("a...b...c", "c"),          # Символы между точками
            ("абв", "абв"),              # Кириллица без точек
            ("123", "123"),              # Цифры без точек
            ("!@#", "!@#"),              # Спецсимволы без точек
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    def test_complex_scenarios(self):
        """Тесты сложных сценариев"""
        test_cases: List[Tuple[str, str]] = [
            ("a..b..c..", ""),           # Четные пары точек удаляют все
            ("a...b...c", "c"),          # Нечетное количество точек
            ("programming..python", "programmingpython"),
            ("hello...world..!", "helloorl"),
            ("123..456..789", "12789"),
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{encrypted}' -> '{result}', ожидалось: '{expected}'"

    def test_whitespace_handling(self):
        """Тесты с пробелами и табуляцией"""
        test_cases: List[Tuple[str, str]] = [
            ("a b", "a b"),              # Пробел внутри
            ("a.. b", " b"),             # Пробел после точек
            (" a..", " "),               # Пробел перед точками
            ("hello  ..world", "hello world"),  # Пробелы и точки
            ("\t..a", "\ta"),            # Табуляция
            ("a\n..b", "ab"),            # Перенос строки
        ]

        for encrypted, expected in test_cases:
            result = decrypt(encrypted)
            assert result == expected, \
                f"Ошибка: '{repr(encrypted)}' -> '{repr(result)}', ожидалось: '{repr(expected)}'"

    def test_long_strings(self):
        """Тесты длинных строк"""
        # Длинная строка без изменений
        long_string = "a" * 1000
        assert decrypt(long_string) == long_string

        # Длинная строка с точками
        long_with_dots = "a" * 100 + ".." * 50
        assert decrypt(long_with_dots) == "a" * 50

        # Только точки
        only_dots = "." * 1000
        assert decrypt(only_dots) == ""


# ===================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ С ИСПОЛЬЗОВАНИЕМ subTest =====================

def test_all_spec_cases_with_subtest():
    """Использование subTest для группировки всех случаев из спецификации"""
    test_cases = [
        ("абра-кадабра.", "абра-кадабра"),
        ("абраа..-кадабра", "абра-кадабра"),
        (" абраа..-.кадабра", "абра-кадабра"),
        ("абра--..кадабра", "абра-кадабра"),
        ("абрау...-кадабра", "абра-кадабра"),
        ("абра........", ""),
        ("абр......a.", "a"),
        ("1..2.3", "23"),
        (".", ""),
        ("1.......................", ""),
    ]

    for encrypted, expected in test_cases:
        with pytest.subTest(encrypted=encrypted, expected=expected):
            result = decrypt(encrypted)
            assert result == expected, \
                f"Шифровка: '{encrypted}' -> Расшифровка: '{result}', ожидалось: '{expected}'"


# ===================== ПАРАМЕТРИЗОВАННЫЕ ТЕСТЫ (более современный подход) =====================

@pytest.mark.parametrize("encrypted, expected", [
    ("абра-кадабра.", "абра-кадабра"),
    ("абраа..-кадабра", "абра-кадабра"),
    (" абраа..-.кадабра", "абра-кадабра"),
    ("абра--..кадабра", "абра-кадабра"),
    ("абрау...-кадабра", "абра-кадабра"),
    ("абра........", ""),
    ("абр......a.", "a"),
    ("1..2.3", "23"),
    (".", ""),
    ("1.......................", ""),
])
def test_decrypt_parametrized(encrypted, expected):
    """Параметризованный тест для всех случаев из задания"""
    assert decrypt(encrypted) == expected


@pytest.mark.parametrize("encrypted, expected", [
    ("a.", ""),
    ("ab.", "a"),
    ("a..", ""),
    ("ab..", ""),
    ("abc..", "a"),
    ("a...", ""),
    ("a.b.c", "c"),
    ("1.2.3", "3"),
    ("", ""),
    ("...", ""),
])
def test_decrypt_additional_cases(encrypted, expected):
    """Дополнительные параметризованные тесты"""
    assert decrypt(encrypted) == expected


# ===================== ЗАПУСК ТЕСТОВ =====================

if __name__ == '__main__':
    # Запуск всех тестов
    pytest.main([__file__, '-v', '--tb=short'])

    # Или можно запустить конкретные тесты:
    # pytest.main([__file__, '-v', '-k', 'test_basic_cases'])