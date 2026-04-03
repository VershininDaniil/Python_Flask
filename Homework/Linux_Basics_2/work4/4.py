from flask import Flask
from datetime import datetime

app = Flask(__name__)

# Кортеж с фразами для каждого дня недели в родительном падеже
# Индексы: 0 – понедельник, 1 – вторник, 2 – среда, 3 – четверг,
# 4 – пятница, 5 – суббота, 6 – воскресенье
weekday_phrases = (
    "хорошего понедельника",
    "хорошего вторника",
    "хорошей среды",
    "хорошего четверга",
    "хорошей пятницы",
    "хорошей субботы",
    "хорошего воскресенья"
)


@app.route('/hello-world/<name>')
def hello_world(name: str) -> str:
    """
    Возвращает приветствие с пожеланием хорошего дня недели.

    Параметры:
        name (str): имя пользователя из URL.

    Возвращает:
        str: приветствие с именем и пожеланием.
    """
    # Получаем текущий день недели (0 = понедельник, 6 = воскресенье)
    weekday_index = datetime.today().weekday()
    phrase = weekday_phrases[weekday_index]
    return f"Привет, {name}. {phrase.capitalize()}!"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)