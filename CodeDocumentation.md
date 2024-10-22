# Техническое описание проекта
## **Стек: Python 3.11 + selenium (version 4.23.1)**
----
## 1. Общее (файл main.py):

Перед работой скрипта необходимо установить (обновить) библиотеки, находящиеся в текстовом файле requierements.txt:

**_В консоли текущего окружения прописывается команда_**: pip install -r requierements.txt

Далее указать желаемые параметра поиска (или оставить параметры по умолчанию). Так же можно указать свой путь сохранения данных (строка 47 path_file).


## 2. Директория result_scrapping:

Директорая предназначена для хранения найденных вакансий (путь сохранения в неё указан по умолчанию). Изначально содержит 1 примерочный json файль с результатом поиска 10 вакансий.

## 3. scripts_scrapping/__init__.py:

Модуль предназначен для определения директории scripts_scrapping как "пакета". Так же содержит в себе дополнительные для работы скрипта функции:

**-3.1. Функция-декоратор time_decorator(func: Callable) -> Callable[[], Any]** - Функция декоратор для подсчета пройденного времени работы функции. В данном коде используется для подсчета времени поиска вакансий (время в формате %H:%M:%S). Принимает в себя func - ссылка на функцию. Возвращает функцию wrapper;

**-3.2. Функция choose_plural(amount: int, declensions: tuple[str]) -> str** - функция для склонения слов. Принимает число и 3 варианта его склонения, например, 91 ('день', 'дня', 'дней'). Принимает amount - количество (int), declensions - список склонений (кортеж строк). Возвращает строку, содержащую в себе число и правильное склонение.


## 4. scripts_scrapping/save_data.py:

Модуль, предназначенный для сохранения информации в json файл. В данной программе сохраняет найденные вакансии.

**-4.1. Функция save_json(name: str, data: dict[dict[str:str]]) -> None** - функция записывает словарь data в json файл по пути name. Если файл name уже существует по этому пути, то немного переделает название файла, чтобы сохранить его по указанному пути. Принимает в себя name - путь записи (срока), data - словарь с информацией. Функция возвращает None;

**-4.1. Функция check_files(name: str) -> str** - функция проверяет, существует ли файл по пути name. Если существует, то добавит к нему уникальную цифру. Принимает в себя name - путь (string). Вернёт строку с исходным путём или переделанным.


## 5. scripts_scrapping/scrap.py:

Модуль предназначен для скрапинга вакансий на HH, данные функции (методы) содержатся в классе ScrappingHH. Так же представлен один декоратор в начале скрипта.

__Логика работы модуля:__

--> При создании экземпляра класса происходит создание движка (в инициализаторе).

--> Далее функция create_main_url по принятым параметрам создаёт ссылку на главную страницу с вакансиями

--> Далее функция get_url принимает созданную ссылку, переходит по ней и сохраняет все ссылки вакансий

--> В конце функция get_vacations проходится по ссылкам с функции get_url и собирает информацию с каждой вакансии. В процессе работы данной функции вызывается другая функция check_key_words, которая проверяет, есть ли ключевые слова в описании вакансии. Если такие есть, то вызывается функция vacations_data и сохраняет нужные параметры (название вакансии, регион, зп и т.д.) 

--> На выходе получается словарь с вакансиями

**-5.1. Функция-декоратор decorator_try_open_main_page(count: int = 10) -> Callable[[Callable], Callable]** - функция декоратор. Дополняет функцию (func), если в ней произошла любая ошибка, то попыается вызвать её ещё столько раз, сколько указано в параметр count. Принимает в себя count - количество раз вызова функции (int). Возвращает функцию base_decorator -> wrapper -> Any;


Класс ScrappingHH - асс, позвляющий подключиться к HH и отбирать вакансии с определёнными параметрами при создании экземпляра класса происходит установка и настройка движка для браузера Chrome. Для работы класса должен быть скачан браузер Chrom

**-5.2. Магический метод класса __init__(self) -> None** - инициализатор класса. Подключается к движку и настраивает его. Ничего не принимает, возвращает None;

**-5.3. Метод класса create_main_url(self, language_prog:str, cities:list[str]=['AllRegions']) -> str** - функция составляет URL адресс для поиска вакансий. Принимает в себя language_prog - строка, указывающая, по какому языку искать вакансии, cities - список городов, по которым производить поиск. Возвращает ссылку (string);

**-5.4. Метод класса get_url(self, main_url) -> list[str]** - функция достаёт все ссылки вакансий на странице. Принимает в себя main_url - URL-ссылка, с которой возьмутся ссылки на вакансии. Функция вернёт список URL-адрессов. Функция оборачивается ранее указанным декоратором decorator_try_open_main_page. Если при попытке взять ссылки произойдёт ошибка, то она вызовится ещё раз. По умолчанию будет пытаться вызваться 10 раз;

**-5.5. Статический метод класса check_key_words(driver: object, keywords: list[str]) -> bool** - функция предназначена для работы внутри класса проверяет (@staticmethod), есть ли ключевые слова (keywords) в описании вакансии, если ключевые слова есть в описании, вернёт True, в ином случае False. Принимает в себя driver - объект браузера, через который происходит поиск, cities - список плючевых строк;

**-5.6. Статический метод vacations_data(driver: object) -> tuple[str]** - функция предназначена для работы внутри класса (@staticmethod). Выцепляет необходимые параметры с вакансии. Принимает в себя driver - объект браузера, через который происходит поиск. Возвращает кортеж строк с  найденными параметров вакансий;

**-5.7. Метод класса get_vacations(self, main_urls: str, quantity: int, keywords: list[str]) -> tuple[tuple[str], ...] | list[None]** - функция проходится по полученным ссылкам (из get_url(main_urls)) и отбирает нужные вакансии, в которых присутствуют ключевые слова. Принимает в себя main_urls - ссылка (string), quantity - количество отбираемых вакансий (num), key_words - список ключевых слов (список со строчками). Возвращает gустой список, если ничего не найдётся или кортеж, состящий из кортежа найденных вакансий и параметров поиска.


## 6. scripts_scrapping/logs.py:
Скрипт содержит функции с отображением результатов работы скрипта в консоли. Все функции используются в в модуле scripts_scrapping/scrap.py 
