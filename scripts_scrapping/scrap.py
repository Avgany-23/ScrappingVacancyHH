from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from functools import wraps
from typing import Callable, Any
import re


def decorator_try_open_main_page(count: int = 10) -> Callable[[Callable], Callable]:
    """Функция декоратор. Дополняет функцию (func), если в ней произошла любая ошибка,
     то попыается вызвать её ещё столько раз, сколько указано в параметр count.
     count - количество раз вызова функции (int)
     Возвращает функцию base_decorator"""

    def base_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func) # Для сохранение атрибутов функции func
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            counter = 1
            # Попытка вызвать функцию (func) count раз
            while counter <= count:

                try:
                    result_func = func(*args, **kwargs)
                    break
                except:
                    counter += 1

            # Если ошибка произошла count раз, то вызов исключения
            if counter - 1 == count:
                raise Service('Ошибка с загрузкой главной страницы со списком вакасий')

            return result_func
        return wrapper
    return base_decorator


class ScrappingHH():
    """Класс, позвляющий подключиться к HH и отбирать вакансии с определёнными параметрами
    при создании экземпляра класса происходит установка и настройка движка для браузера Chrome.
    Для работы класса должен быть скачан браузер Chrome."""

    def __init__(self) -> None: # Подключение к движку
        """Инициализатор. Подключается к движку и настраивает его
        Ничего не принимает, возвращает None"""

        self.path = ChromeDriverManager().install()                     # Установка и получение пути движка
        self.browser_service = Service(executable_path=self.path)       # Загрузка движка в браузер по пути path
        self.options = ChromeOptions()                                  # Экземпляр класса настройки движка
        self.options.add_experimental_option("detach", True)            # Не закрывать браузер во время работы
        # self.options.add_argument('--headless')                       # Для ускорения парсинга


    def create_main_url(self, language_prog:str, cities:list[str]=['AllRegions']) -> str:
        """Функция предназначена для работы внутри класса. Составляет URL адресс для поиска
        language_prog - строка, указывающая, по какому языку искать вакансии
        cities - список городов, по которым производить поиск
        Возвращает ссылку (string)"""

        area = {'AllRegions': 'true', 'Moscow': 1, 'St.Petersburg': 2, 'Ekaterinburg': 3, 'Novosibirsk': 4}
        headers_city = '&area=' + '&area='.join(str(area[city]) for city in cities)

        # Сохранение данных экземпляру класса для дальнейшего использования
        self.language_prog = language_prog.lower()
        self.cities = cities
        self.main_url = f'https://spb.hh.ru/search/vacancy?text={language_prog.lower()}{headers_city}'
        return self.main_url

    @decorator_try_open_main_page()  # За счет декоратора главная страница в браузере будет пытаться открыться 10 раз
    def get_url(self, main_url) -> list[str]:
        """Функция достаёт все ссылки вакансий на странице
        main_url - URL-ссылка, с которой возьмутся ссылки на вакансии
        Функция вернёт список URL-адрессов"""

        driver = Chrome(service=self.browser_service,
                        options=self.options)                               # Создание браузера
        driver.get(main_url)                                                # Переход на страницу для поиска URL вакансий
        urls = []                                                           # Список полученных URL-адресов
        path_HTML = '//h2[@class="bloko-header-section-2"]/span/a'          # Путь HTML к ссылке вакансии
        url_vacancy = driver.find_elements(By.XPATH, path_HTML)             # Получение объектов
        for el in url_vacancy:                                              # Итерация по полученным объектам
            urls.append(el.get_attribute('href'))                           # Изъятие ссылки из свойства href тега <a>
        driver.quit()                                                       # Закрытие браузера
        return urls


    @staticmethod
    def check_key_words(driver: object, keywords: list[str]) -> bool:
        """Функция предназначена для работы внутри класса, проверяет, есть ли ключевые слова (keywords) в описании вакансии
        Если ключевые слова есть в описании, вернёт True, в ином случае False
        driver - объект браузера, через который происходит поиск
        cities - список плючевых строк"""

        # HTML пути до собираемых данных с Вакансий
        path_html_disription1 = '//div[@class="vacancy-section"]/div[@class="g-user-content"]'
        path_html_disription2 = '//div[@class="vacancy-branded-user-content"]'
        path_html_disription3 = '//div[@class="vacancy-body-block-module_vacancy-body-block__Iv3qP"]/div[@class="g-user-content"]'

        # Первый вариант оформления описания вакансии
        try: vacancy_discription = driver.find_element(By.XPATH, path_html_disription1)
        except NoSuchElementException:
            # Второй вариант оформления описания вакансии
            try: vacancy_discription = driver.find_element(By.XPATH, path_html_disription2)
            # Третий вариант оформления описания вакансии
            except NoSuchElementException: vacancy_discription = driver.find_element(By.XPATH, path_html_disription3)

        # Проверка на содержание ключевых слов в вакансии
        if not re.findall('|'.join(keywords), vacancy_discription.text, re.I):
            return False
        return True


    @staticmethod
    def vacations_data(driver: object) -> tuple[str]:
        """Функция предназначена для работы внутри класса. Выцепляет необходимые параметры с вакансии
        driver - объект браузера, через который происходит поиск
        Возвращает кортеж строк с  найденными параметров вакансий"""

        # HTML пути до собираемых данных с Вакансий
        path_html_title = '//div[@class="vacancy-title"]/h1'
        path_html_company = '//span[@class="vacancy-company-name"]'
        path_html_area = '//div[@class="vacancy-company-redesigned"]/div[last()]'
        path_html_experience = '//p[@class="vacancy-description-list-item"]'

        # Получение информации о вакансии
        vacancy_title = driver.find_element(By.XPATH, path_html_title)                                 # Название вакансий
        vacancy_company = driver.find_element(By.XPATH, path_html_company)                             # Название компании
        vacancy_area = driver.find_element(By.XPATH, path_html_area)                                   # Регион (город) вакансии
        vacancy_experience = driver.find_element(By.XPATH, path_html_experience)                       # Требуемый опыт
        try: vacancy_salary = driver.find_element(By.XPATH, '//div[@data-qa="vacancy-salary"]').text   # ЗП вакансии
        except NoSuchElementException: vacancy_salary = 'Зарплата не указана'

        return (vacancy_title.text, vacancy_salary, vacancy_company.text,
                vacancy_area.text.split(', ')[0], vacancy_experience.text)


    def get_vacations(self, main_urls: str, quantity: int, keywords: list[str]) -> tuple[tuple[str], ...] | list[None]:
        '''Функция проходится по полученным ссылкам (из get_url(main_urls)) и отбирает нужные вакансии,
        в которых присутствуют ключевые слова
        main_urls - ссылка (string)
        quantity - количество отбираемых вакансий (num)
        key_words - список ключевых слов (список со строчками)
        Возвращает gустой список, если ничего не найдётся или кортеж,
        состящий из кортежа найденных вакансий и параметров поиска
        '''

        print(f'>> Поиск вакансий начался. Количество поиска вакансий - {quantity}')
        urls = self.get_url(main_urls)              # Получение ссылок вакансий со страницы по ссылке main_url
        if not urls:                                # Если ничего нашлось на первой странице, то выход из функции
            print('Ничего не нашлось.')
            return []

        result_info_vacations = []                  # Информация о найденных вакансиях (Ссылка, название, компания и т.д.)
        count_check_vacations = 0                   # Счетчик для количества всех просмотренных вакансий
        count = 0                                   # Счетчик для отслеживания количество найденных подходящих под условия вакансий
        number_page = 0                             # Номер страницы (со второго цикла for)

        try:    # Если произойдёт какая-либо ошибка, то текущие данные сохранятся, а программа остановит скраппинг
            # Пока не найдется указанное (quantity) кол-во вакансий, будет работать while
            while count != quantity:
                # Если первый цикл for дошёл до конца и нужного кол-во вакансий не набралось,
                # значит переход на следующую страницу поиска
                if number_page >= 1:
                    urls = self.get_url(main_urls + f'&page={number_page}')
                    if not urls:
                        break

                number_page += 1                                                      # Увеличение номера страницы для следующего шага while
                driver = Chrome(service=self.browser_service, options=self.options)   # Создание браузера

                # Итерация по ссылкам с вакансиями
                for url in urls:
                    driver.get(url)                     # Переход браузера по ссылке (url) с вакансией
                    count_check_vacations += 1          # Просмотр вакансии увеличивается на 1

                    # Если ключевых слов в вакансии нет, то пропускаем скраппинг по ней
                    if not self.check_key_words(driver, keywords):
                        continue

                    # Получение информации о вакансии и запись в result_info_vacations
                    try: result_info = self.vacations_data(driver)
                    except: continue    # Если произошла любая ошибка, то пропуск итерации
                    result_info_vacations.append({'url_adress': url, 'title': result_info[0],
                                                  'salary': result_info[1], 'name_company': result_info[2],
                                                  'city': result_info[3], 'experience': result_info[4]})
                    count += 1                    # Увеличение счетчика найденных вакансий
                    print(f'\r---> Текущее количество найденных вакансий ➙ {count}', end='', flush=True)
                    if count == quantity: break   # Если введённое пользователем количество вакансий нашлось, прекращаем искать

                driver.quit()                     # Закрытие браузера
        except: pass
        print(f'\nПроцесс закончен ✅✅\n'
              f'-количество найденных вакансий с содержанием указанных ключевых слов: {count}\n'
              f'-количество просмотренных вакансий с фильтром языка программирования и указанных регионов: {count_check_vacations}')
        return result_info_vacations, count, count_check_vacations, keywords, self.cities, self.language_prog