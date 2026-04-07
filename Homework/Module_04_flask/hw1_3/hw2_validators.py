from typing import Optional
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Функция-валидатор, возвращающая валидирующую функцию.
    """
    def _number_length(form: FlaskForm, field: Field):
        # Получаем значение поля
        value = field.data
        if value is None:
            return
        # Преобразуем число в строку
        str_value = str(value)
        length = len(str_value)
        if length < min or length > max:
            msg = message or f"Длина числа должна быть от {min} до {max} цифр"
            raise ValidationError(msg)
    return _number_length


class NumberLength:
    """
    Класс-валидатор.
    """
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        value = field.data
        if value is None:
            return
        str_value = str(value)
        length = len(str_value)
        if length < self.min or length > self.max:
            msg = self.message or f"Длина числа должна быть от {self.min} до {self.max} цифр"
            raise ValidationError(msg)