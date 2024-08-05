import json
import os


def save_json(name: str, data: dict[dict[str:str]]) -> None:
    """Функция для записи словаря data в json файл. Если путь (name) для заиси файла не найдется,
    то файл запишется в текущую директорию.
    name - путь записи (срока)
    data - словарь с информацией
    Функция возвращает None"""

    name = check_files(name)
    try:

        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except FileNotFoundError as e:  # Если путь на нашёлся, то файл запишется в текущую директорию вызова функции
        print(e)
        name = check_files(os.path.join(os.getcwd(), 'vacations.json'))
        with open(name, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"|| Содержимое записано в файл{' '*6}---> {name}")

def check_files(name: str) -> str:
    """Функция проверяет, существует ли файл по пути name. Если существует, то добавит к нему уникальную цифру
    name - путь (string)
    Вернёт исходный путь или переделанный"""

    if os.path.exists(name):
        print(f'❌❌Файл уже сушествует по пути    ---> {name}')
        count = 1
        while True:
            current_name = name[:name.rfind('.')] + f'({str(count)})' + name[name.rfind('.'):]
            if not os.path.exists(current_name):
                name = current_name
                break
            count += 1
    return name