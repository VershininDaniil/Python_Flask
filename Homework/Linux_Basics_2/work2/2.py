import sys


def get_mean_size(ls_output: str) -> float:
    """
    Вычисляет средний размер обычных файлов в выводе команды ls -l.
    """
    lines = ls_output.strip().splitlines()
    if not lines:
        return 0.0

    # Пропускаем строку "total ...", если она есть
    start_index = 0
    if lines and lines[0].startswith('total'):
        start_index = 1

    sizes = []
    for line in lines[start_index:]:
        if not line.strip():
            continue
        columns = line.split()
        # Проверяем, что это обычный файл (первый символ '-')
        if len(columns) >= 5 and columns[0].startswith('-'):
            try:
                size = int(columns[4])
                sizes.append(size)
            except ValueError:
                continue

    if not sizes:
        return 0.0

    return sum(sizes) / len(sizes)


def format_bytes(bytes_value: float) -> str:
    """
    Переводит байты в человекочитаемый формат (B, KiB, MiB, GiB).
    """
    if bytes_value < 1024:
        return f"{bytes_value:.2f} B"
    elif bytes_value < 1024 ** 2:
        return f"{bytes_value / 1024:.2f} KiB"
    elif bytes_value < 1024 ** 3:
        return f"{bytes_value / 1024 ** 2:.2f} MiB"
    else:
        return f"{bytes_value / 1024 ** 3:.2f} GiB"


if __name__ == '__main__':
    # ВРЕМЕННО для теста - читаем из файла
    with open('ls_output.txt', 'r', encoding='utf-8') as f:
        data = f.read()

    mean_size_bytes = get_mean_size(data)
    mean_size_readable = format_bytes(mean_size_bytes)

    print(f"{mean_size_bytes:.2f} байт = {mean_size_readable}")