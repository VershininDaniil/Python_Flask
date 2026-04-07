from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    """
    Контекстный менеджер, который игнорирует переданные типы исключений.
    Если возникает неожидаемый тип исключения, он прокидывается выше.
    """
    def __init__(self, errors: Collection) -> None:
        # Для issubclass нужен кортеж:
        self.errors = tuple(errors)

    def __enter__(self) -> None:
        """
        Метод __enter__ ничего не делает, но он необходим для корректного
        использования контекстного менеджера.
        """

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        """
        Если тип исключения находится в списке игнорируемых (self.errors),
        метод возвращает True, что указывает на успешную обработку
        исключения и его игнорирование. Если исключение
        не из списка игнорируемых, метод возвращает None,
        и исключение прокидывается выше по стеку вызовов.
        """
        if issubclass(exc_type, self.errors):
            # игнорируем исключение:
            return True
        # прокидываем выше:
        return None