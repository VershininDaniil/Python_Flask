result = 0
for n in range(1, 11):
    result += n ** 2


# Secret magic code
import sys


with open(sys.argv[0], 'r') as py_file:
    py_file_content = py_file.read()
    # sys.argv - список, содержащий аргументы командной строки
    # sys.argv[0] - первый элемент списка - имя скрипта
    # таким образом мы открываем наш скрипт и читаем его

print(py_file_content)