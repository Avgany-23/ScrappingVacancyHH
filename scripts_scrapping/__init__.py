from datetime import datetime, timedelta
from time import sleep
from typing import Callable, Any
from functools import wraps


def time_decorator(func: Callable) -> Callable[[], Any]:
    """"Функция декоратор для подсчета пройденного времени работы функции
    Принимает func - ссылка на функцию
    Возвращает функцию wrapper"""

    @wraps(func)    # Для сохранение атрибутов функции func
    def wrapper(*args: Any, **kwargs: Any) -> func:
        """Функция обертка. Возвращает значение функции func
        Принимает *args - позиционные аргументов, **kwargs - именнованные"""
        print(f'Начало работы функции.\n'
              f"🕐Текущее время и дата: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
        start = datetime.now()
        result_func = func(*args, **kwargs)
        end = datetime.now() - start

        # Подсчет количества часов, минут и секунд
        hours = end.seconds // 60 // 60
        minutes = end.seconds // 60 - hours * 60
        seconds = end.seconds - hours * 60 ** 2 - minutes * 60

        # Кортежи для правильного склонения времени
        name_hours = ('час', 'часа', 'часов')
        name_minutes = ('минута', 'минуты', 'минут')
        name_seconds = ('секунда', 'секунды', 'секунд')

        # Вывод информации о количестве работы функции
        print(f'Время обработки составило: {choose_plural(hours, name_hours)} '
                                         f'{choose_plural(minutes, name_minutes)} и '
                                         f'{choose_plural(seconds, name_seconds)}\n')
        return result_func
    return wrapper


def choose_plural(amount: int, declensions: tuple[str]) -> str:
    """Функция для склонения слов. Принимает число и 3 варианта его склонения,
    Например, 91 ('день', 'дня', 'дней')
    Принимает amount - количество (int), declensions - список склонений (кортеж строк)
    Возвращает строку, содержащую в себе число и правильное склонение"""

    selector = {
        amount % 10 == 1: 0,
        amount % 10 in [2, 3, 4]: 1,
        amount % 10 in [0, 5, 6, 7, 8, 9]: 2,
        amount % 100 in range(11, 21) : 2
    }
    return f'{amount} {declensions[selector[True]]}'