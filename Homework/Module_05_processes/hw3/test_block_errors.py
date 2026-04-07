import logging, unittest

from block_errors import BlockErrors


# Настройка конфигурации логгирования
logging.basicConfig(level=logging.DEBUG)


class TestBlockErrors(unittest.TestCase):

    def test_ignor_error(self):
        """Ошибка игнорируется."""
        ignor_errors = {ZeroDivisionError, TypeError}
        with BlockErrors(ignor_errors):
            a = 1 / 0
        logging.debug(
            f'1. Выполнено без ошибок (ошибка игнорируется)!'
        )

    def test_above_error(self):
        """Ошибка прокидывается выше."""
        ignor_errors = {ZeroDivisionError}
        with self.assertRaises(TypeError) as exc:
            with BlockErrors(ignor_errors):
                a = 1 / '0'
                # вызывается TypeError, которого нет в игноре,
                # поэтому TypeError переходит выше где его ловит assertRaises
        logging.debug(
            f'2. Ошибка прокидывается выше: {type(exc.exception).__name__}'
        )

    def test_external_error(self):
        """
        Ошибка прокидывается выше во внутреннем блоке и
        игнорируется во внешнем.
        """
        external_ignor = {TypeError}
        with BlockErrors(external_ignor):
            internal_ignor = {ZeroDivisionError}
            with BlockErrors(internal_ignor):
                a = 1 / '0'
        logging.debug('3. Внешний блок: выполнено без ошибок.')

    def test_exc_error(self):
        """Дочерние ошибки игнорируются."""
        ignor_errors = {Exception}
        try:
            with BlockErrors(ignor_errors):
                a = 1 / '0'
        except Exception as exc:
            self.fail(f'4. Ошибка не игнорируется: {type(exc).__name__}')
        logging.debug(
            f'4. Игнорируется дочерняя ошибка Exception!'
        )


if __name__ == '__main__':
    unittest.main()