from datetime import datetime
from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    """
    сохранение информации о совершённой
    в рублях трате за какой-то день

    Args:
        date (str): дата в формате YYYYMMDD.
        number (int): сумма в рублях.
    """
    # try:
    its_date = datetime.strptime(date, '%Y%m%d').date()
    year = its_date.year
    month = its_date.month
    day = its_date.day

    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += number

    storage[year][month].setdefault('month_total', 0)
    storage[year].setdefault('year_total', 0)

    # сумма месячных трат:
    storage[year][month]['month_total'] += number
    # сумма годовых трат:
    storage[year]['year_total'] += number
    print(storage)

    return f"траты за {its_date}: {number} руб."
    # except ValueError:
    #     return 'Введите корректную дату!'


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    """ получение суммарных трат за указанный год.

    Args:
        year (int): год.
    """
    try:
        year_expenses = storage[year]['year_total']
        print(year_expenses)
        return f'затраты за год {year}: {year_expenses} руб.'
    except KeyError:
        return 'В эту дату нет трат!'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    """
    получение суммарных трат за указанные год и месяц.

    Args:
        year (int): год.
        month (int): месяц.
    """
    # try:
    month_expenses = storage[year][month]['month_total']
    print(month_expenses)
    return f'затраты за год {year} месяц {month}: {month_expenses} руб.'
    # except KeyError:
    #     return 'В эту дату нет трат!'


if __name__ == "__main__":
    app.run(debug=True)