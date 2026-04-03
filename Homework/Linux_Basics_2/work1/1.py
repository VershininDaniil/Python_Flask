import os
import subprocess


def get_process_list_windows():
    """
    Получает список процессов в Windows в отформатированном виде
    """
    try:
        # Используем PowerShell Get-Process с форматированием в таблицу
        ps_script = """
        Get-Process | 
        Select-Object -Property @{Name='PID'; Expression={$_.Id}},
                                        @{Name='Name'; Expression={$_.ProcessName}},
                                        @{Name='CPU(s)'; Expression={[math]::Round($_.CPU, 2)}},
                                        @{Name='Memory(KB)'; Expression={[math]::Round($_.WorkingSet64/1KB, 0)}},
                                        @{Name='Threads'; Expression={$_.Threads.Count}},
                                        @{Name='StartTime'; Expression={$_.StartTime}} |
        Sort-Object -Property 'Memory(KB)' -Descending |
        Format-Table -AutoSize -Wrap
        """

        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='cp866'
        )

        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            return None

    except Exception as e:
        print(f"Ошибка при получении списка процессов: {e}")
        return None


def get_process_list_tasklist():
    """
    Альтернативный способ - используем tasklist с форматированием
    """
    try:
        # tasklist в табличном формате
        result = subprocess.run(
            ['tasklist', '/FO', 'TABLE', '/NH'],
            capture_output=True,
            text=True,
            encoding='cp866'
        )

        if result.returncode == 0:
            # Добавляем заголовки вручную для красоты
            header = "+" + "="*110 + "+\n"
            header += f"| {'Имя образа':<30} | {'PID':>8} | {'Сессия':<10} | {'Сессия №':>8} | {'Память (КБ)':>15} |\n"
            header += "+" + "="*110 + "+\n"

            lines = result.stdout.strip().split('\n')
            formatted_output = header

            for line in lines:
                if line.strip():
                    # Парсим строку tasklist
                    parts = line.split()
                    if len(parts) >= 5:
                        name = parts[0][:30]
                        pid = parts[1]
                        session = parts[2] if len(parts) > 2 else "Services"
                        session_num = parts[3] if len(parts) > 3 else "0"
                        memory = parts[4] if len(parts) > 4 else "0"

                        formatted_output += f"| {name:<30} | {pid:>8} | {session:<10} | {session_num:>8} | {memory:>15} |\n"

            formatted_output += "+" + "-"*110 + "+"
            return formatted_output

    except Exception as e:
        print(f"Ошибка при использовании tasklist: {e}")
        return None


def save_beautiful_process_list(file_path):
    """
    Сохраняет красивый отформатированный список процессов в файл
    """
    print("📊 Получение списка процессов...")

    # Пробуем получить красивый список
    processes = get_process_list_windows()

    if not processes:
        print("⚠️ Не удалось получить форматированный список, пробуем альтернативный способ...")
        processes = get_process_list_tasklist()

    if processes:
        # Добавляем информационный заголовок
        from datetime import datetime

        with open(file_path, 'w', encoding='utf-8') as f:
            # Записываем шапку с информацией
            f.write("="*120 + "\n")
            f.write(f"{"ОТЧЁТ О ПРОЦЕССАХ СИСТЕМЫ":^120}\n")
            f.write("="*120 + "\n")
            f.write(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Имя компьютера: {os.environ.get('COMPUTERNAME', 'Unknown')}\n")
            f.write(f"Пользователь: {os.environ.get('USERNAME', 'Unknown')}\n")
            f.write("-"*120 + "\n\n")

            # Записываем список процессов
            f.write(processes)

            # Добавляем статистику в конец файла
            f.write("\n\n" + "="*120 + "\n")
            f.write(f"{"СТАТИСТИКА":^120}\n")
            f.write("="*120 + "\n")

            # Получаем статистику по памяти
            stats = get_memory_statistics()
            if stats:
                f.write(stats)

        print(f"✅ Красивый отчёт сохранён в файл: {file_path}")
        return True
    else:
        print(f"❌ Не удалось получить список процессов")
        return False


def get_memory_statistics():
    """
    Получает статистику по использованию памяти
    """
    try:
        ps_script = """
        $processes = Get-Process
        $totalMemory = [math]::Round(($processes | Measure-Object -Property WorkingSet64 -Sum).Sum / 1KB, 0)
        $avgMemory = [math]::Round(($processes | Measure-Object -Property WorkingSet64 -Average).Average / 1KB, 0)
        $maxProcess = $processes | Sort-Object WorkingSet64 -Descending | Select-Object -First 1
        $maxMemory = [math]::Round($maxProcess.WorkingSet64 / 1KB, 0)
        
        Write-Output "Всего процессов: $($processes.Count)"
        Write-Output "Всего используется памяти: $($totalMemory.ToString('N0')) KB"
        Write-Output "Среднее использование памяти: $($avgMemory.ToString('N0')) KB"
        Write-Output "Процесс с максимальным использованием памяти: $($maxProcess.ProcessName) (PID: $($maxProcess.Id)) - $($maxMemory.ToString('N0')) KB"
        """

        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='cp866'
        )

        if result.returncode == 0:
            return result.stdout.strip()

    except Exception as e:
        print(f"Ошибка при получении статистики: {e}")

    return None


def display_file_content(file_path):
    """
    Отображает содержимое файла в консоли (первые 30 строк)
    """
    if os.path.exists(file_path):
        print(f"\n{'='*60}")
        print(f"ПРЕДПРОСМОТР ФАЙЛА {file_path}")
        print(f"{'='*60}")

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Показываем первые 30 строк или весь файл, если он меньше
            for i, line in enumerate(lines[:30], 1):
                print(f"{i:3}: {line.rstrip()}")

            if len(lines) > 30:
                print(f"\n... и ещё {len(lines) - 30} строк ...")
                print(f"Полный файл можно посмотреть здесь: {os.path.abspath(file_path)}")

        print(f"{'='*60}\n")


def main():
    # Путь к файлу вынесен в отдельную переменную
    file_path = "process_list.txt"



    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        print(f"📁 Файл '{file_path}' уже существует.")
        response = input("🔄 Перезаписать файл? (y/n): ").lower()
        if response != 'y':
            print("❌ Операция отменена.")
            return

    # Создаём красивый отчёт
    if save_beautiful_process_list(file_path):
        # Показываем превью файла
        display_file_content(file_path)

        # Показываем информацию о файле
        file_size = os.path.getsize(file_path)
        print(f"\n📊 Информация о файле:")
        print(f"   • Имя: {file_path}")
        print(f"   • Размер: {file_size:,} байт")
        print(f"   • Полный путь: {os.path.abspath(file_path)}")
    else:
        print("❌ Не удалось создать отчёт.")


if __name__ == "__main__":
    main()