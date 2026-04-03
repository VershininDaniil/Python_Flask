from flask import Flask

app = Flask(__name__)


@app.route('/max_number/<path:numbers>')
def max_number(numbers):
    # Разделяем строку по слешу
    parts = numbers.split('/')
    valid_numbers = []

    for part in parts:
        # Пропускаем пустые части (например, если был двойной слеш)
        if part == '':
            continue
        try:
            num = int(part)
            valid_numbers.append(num)
        except ValueError:
            # Если элемент не является целым числом, просто игнорируем его
            # Можно также вернуть ошибку, но по условию просто пропускаем
            continue

    if not valid_numbers:
        return "Не передано ни одного корректного числа"

    max_num = max(valid_numbers)
    # Используем HTML-тег <i> для курсива
    return f"Максимальное переданное число <i>{max_num}</i>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)