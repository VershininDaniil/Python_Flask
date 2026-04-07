import shlex, subprocess

from flask import Flask, request
from typing import List


app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    # Получаем аргументы из запроса:
    args: List[str] = request.args.getlist('arg')
    print('1', args)

    # Применяем shlex.quote,
    # что важно для безопасного формирования командной строки,
    # и строим список из строки аргументов:
    quote_args = [''.join(shlex.quote(arg) for arg in args)]
    print('2', quote_args)

    # clean_quote_args = ''.join(quote_args)
    # print('3', clean_quote_args)

    # Строим команду ps с применением аргументов:
    command = ['ps'] + quote_args
    print('4', command)
    # clean_command = [shlex.quote(arg) for arg in command]

    # Вызываем команду:
    result = subprocess.run(command, capture_output=True, text=True)

    ps_info = result.stdout.strip()

    return f'<pre>{ps_info}</pre>'


if __name__ == "__main__":
    app.run(debug=True)