import json
import os


def save_json(name: str, data: dict[dict[str:str]]) -> None:
    """Функция для записи словаря data в json файл.
    name - путь записи (срока)
    data - словарь с информацией
    Функция возвращает None"""

    name = check_files(name)
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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
    print(f'|| Содержимое будет записано в файл ---> {name}')
    return name