from flask import Flask
import os

app = Flask(__name__)


@app.route('/preview/<int:size>/<path:relative_path>')
def preview(size: int, relative_path: str):
    """
    Возвращает первые size символов файла по относительному пути relative_path.
    """
    try:
        # Абсолютный путь к файлу
        abs_path = os.path.abspath(relative_path)

        # Читаем не более size символов (файл не загружается целиком)
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read(size)

        result_size = len(content)

        # Формируем ответ: жирный путь, размер и содержимое
        return f"<b>{abs_path}</b> {result_size}<br>{content}"

    except FileNotFoundError:
        return "Файл не найден"
    except PermissionError:
        return "Нет прав на чтение файла"
    except Exception as e:
        return f"Ошибка: {e}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777, debug=True)