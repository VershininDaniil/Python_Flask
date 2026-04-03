from flask import Flask

app = Flask(__name__)

# Структура хранения: {год: {месяц: сумма_за_месяц}}
storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    """
    Сохраняет трату в рублях за указанный день.
    Дата в формате YYYYMMDD (год, месяц, день).
    """
    year = int(date[:4])
    month = int(date[4:6])
    # day = int(date[6:])  # день не используется в агрегированном хранении

    # Добавляем сумму к месячной статистике
    storage.setdefault(year, {}).setdefault(month, 0)
    storage[year][month] += number

    return "OK"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    """
    Возвращает суммарные траты за указанный год.
    """
    if year not in storage:
        return "0"
    total = sum(storage[year].values())
    return str(total)


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    """
    Возвращает суммарные траты за указанный месяц.
    """
    if year not in storage or month not in storage[year]:
        return "0"
    return str(storage[year][month])


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777, debug=True)