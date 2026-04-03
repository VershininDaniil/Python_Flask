import random
from datetime import datetime, timedelta
import os
import re
from flask import Flask

app = Flask(__name__)

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cat_breeds = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

def get_words_from_book():
    with open(BOOK_FILE, 'r', encoding='utf-8') as book:
        text = book.read()
        words = re.findall(r'\b[а-яА-Яa-zA-Z]+\b', text)
        return words

book_words = get_words_from_book()
counter_visits = 0

@app.route('/hello_world')
def hello_world():
    return 'Привет, мир!'

@app.route('/cars')
def cars():
    return ', '.join(cars_list)

@app.route('/cats')
def cats():
    return random.choice(cat_breeds)

@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now()
    return f'Точное время: {current_time.strftime("%Y-%m-%d %H:%M:%S")}'

@app.route('/get_time/future')
def get_time_future():
    future_time = datetime.now() + timedelta(hours=1)
    return f'Точное время через час будет {future_time.strftime("%Y-%m-%d %H:%M:%S")}'

@app.route('/get_random_word')
def get_random_word():
    return random.choice(book_words)

@app.route('/counter')
def counter():
    global counter_visits
    counter_visits += 1
    return str(counter_visits)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("СЕРВЕР ЗАПУЩЕН!")
    print("="*50)
    print("\nОткрой в браузере:\n")
    print("  http://127.0.0.1:5000/hello_world")
    print("  http://127.0.0.1:5000/cars")
    print("  http://127.0.0.1:5000/cats")
    print("  http://127.0.0.1:5000/get_time/now")
    print("  http://127.0.0.1:5000/get_time/future")
    print("  http://127.0.0.1:5000/get_random_word")
    print("  http://127.0.0.1:5000/counter")
    print("\n" + "="*50)
    app.run(debug=True)