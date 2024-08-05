from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scripts_scrapping.logs import *
from functools import wraps
from typing import Callable, Any
import re


def decorator_try_open_main_page(count: int = 10) -> Callable[[Callable], Callable]:
    """Функция декоратор. Дополняет функцию (func), если в ней произошла любая ошибка,
     то попытается вызвать её ещё столько раз, сколько указано в параметр count,
     count - количество раз вызова функции (int)
     Возвращает функцию base_decorator"""

    def base_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)  # Для сохранения атрибутов функции func
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
                raise Service('Ошибка с загрузкой главной страницы со списком вакансий')
            return result_func

        return wrapper

    return base_decorator


class ScrappingHH:
    """Класс, позволяющий подключиться к HH и отбирать вакансии с определёнными параметрами
    при создании экземпляра класса происходит установка и настройка движка для браузера Chrome.
    Для работы класса должен быть скачан браузер Chrome."""

    def __init__(self, main_url, show_search=True) -> None:  # Подключение к движку
        """Инициализатор. Подключается к движку и настраивает его
        Ничего не принимает, возвращает None"""

        self.path = ChromeDriverManager().install()                         # Установка и получение пути движка
        self.browser_service = Service(executable_path=self.path)           # Загрузка движка в браузер по пути path
        self.options = ChromeOptions()                                      # Экземпляр класса настройки движка
        self.options.add_experimental_option("detach", True)    # Не закрывать браузер во время работы
        if not show_search:
            self.options.add_argument('--headless')                         # Отображение браузера
        self.main_url = main_url

    def replace_main_url(self, new_url: str) -> str:
        """Функция для изменения главной ссылки с вакансиями
        new-url - новая ссылка (str).
        Функция вернёт новую ссылку (str)"""

        self.main_url = new_url
        return self.main_url

    def main_url_add_next_page(self, number_page: int, url: str) -> None:
        """Функция для изменения/добавления номера страницы ссылке
        number_page - номер страницы (int), url - ссылка, к которой добавится изменение.
        Функция вернёт None"""

        # Если page нет в ссылке, то добавляет
        if not re.findall(r'&page=\d+', url):  self.replace_main_url(url + f'page={number_page}')
        # Если page есть в ссылке, то изменяется
        else:  self.replace_main_url(re.sub(r'&page=\d+', f'&page={number_page}', url))

    @decorator_try_open_main_page()  # За счет декоратора главная страница в браузере будет пытаться открыться 10 раз
    def get_url(self) -> list[str]:
        """Функция достаёт все ссылки вакансий на странице
        main_url - URL-ссылка, с которой возьмутся ссылки на вакансии
        Функция вернёт список из строк URL-адресов вакансий"""

        driver = Chrome(service=self.browser_service, options=self.options)  # Создание браузера
        driver.get(self.main_url)                                   # Переход на страницу для поиска URL вакансий
        urls = []                                                   # Список полученных URL-адресов
        path_HTML = '//h2[@class="bloko-header-section-2"]/span/a'  # Путь HTML к ссылке вакансии
        url_vacancy = driver.find_elements(By.XPATH, path_HTML)     # Получение объектов
        for el in url_vacancy:                                      # Итерация по полученным объектам
            urls.append(el.get_attribute('href'))                   # Изъятие ссылки из свойства href тега <a>
        driver.quit()                                               # Закрытие браузера
        return urls

    @staticmethod
    def vacations_data(driver: object) -> tuple[Any, str | Any, Any, Any, Any]:
        """Функция предназначена для работы внутри класса. Достает необходимые параметры с вакансии
        driver - объект браузера, через который происходит поиск,
        возвращает кортеж строк с найденными параметров вакансий"""

        # HTML пути до собираемых данных с Вакансий
        path_html_title = '//div[@class="vacancy-title"]/h1'
        path_html_company = '//div[@class="vacancy-company-details"]'
        path_html_area = '//div[@class="vacancy-company-redesigned"]/div[last()]'
        path_html_experience = '//p[@class="vacancy-description-list-item"]'
        path_html_salary = '//div[@data-qa="vacancy-salary"]'

        # Получение информации о вакансии
        vacancy_title = driver.find_element(By.XPATH, path_html_title)              # Название вакансий
        vacancy_company = driver.find_element(By.XPATH, path_html_company)          # Название компании
        vacancy_area = driver.find_element(By.XPATH, path_html_area)                # Регион (город) вакансии
        vacancy_experience = driver.find_element(By.XPATH, path_html_experience)    # Требуемый опыт
        try: vacancy_salary = driver.find_element(By.XPATH, path_html_salary).text  # ЗП вакансии
        except NoSuchElementException:  vacancy_salary = 'Зарплата не указана'

        return (vacancy_title.text, vacancy_salary, vacancy_company.text,
                vacancy_area.text.split(', ')[0], vacancy_experience.text)

    def get_vacations(self, quantity: int) -> list[Any] | list[list[dict[str, str | Any]] | int]:
        """Функция проходится по полученным ссылкам и отбирает нужные вакансии (get_url(main_urls),
        в которых присутствуют ключевые слова
        quantity - количество отбираемых вакансий (num)
        key_words - список ключевых слов (список со строчками)
        Возвращает пустой список, если ничего не найдётся или кортеж,
        состоящий из кортежа найденных вакансий и параметров поиска"""

        log_start(quantity)
        urls = self.get_url()   # Получение ссылок вакансий со страницы по ссылке main_url
        if not urls:            # Если ничего нашлось на первой странице, то выход из функции
            log_non_url()
            return []

        result_info_vacations = []  # Информация о найденных вакансиях (Ссылка, название, компания и т.д.)
        count_check_vacations = 0   # Счетчик для количества всех просмотренных вакансий
        count = 0                   # Счетчик для отслеживания количество найденных подходящих под условия вакансий
        number_page = 0             # Номер страницы (со второго цикла for)

        while count != quantity:    # Цикл ищет указанное количество вакансий = quantity
            if number_page >= 1:    # Переход на следующую страницу по новой ссылке и получение ссылок
                self.main_url_add_next_page(number_page, self.main_url)  # Следующая страница
                try: urls = self.get_url()
                except: break
                if not urls: break

            number_page += 1  # Увеличение номера страницы для следующего шага while
            driver = Chrome(service=self.browser_service, options=self.options)  # Создание браузера

            for url in urls:                    # Итерация по ссылкам с вакансиями
                try:                            # Если случится любая ошибка при поиске информации, то пропуск итерации
                    driver.get(url)                            # Переход браузера по ссылке (url) с вакансией
                    count_check_vacations += 1                 # Просмотр вакансии увеличивается на 1
                    result_info = self.vacations_data(driver)  # Получение информации о вакансии
                except BaseException as error:
                    log_error_url_search(url, error)
                    driver = Chrome(service=self.browser_service, options=self.options)  # Создание браузера
                    continue

                result_info_vacations.append({'url_address': url, 'title': result_info[0],
                                              'salary': result_info[1], 'name_company': result_info[2],
                                              'city': result_info[3], 'experience': result_info[4]})
                count += 1                      # Увеличение счетчика найденных вакансий
                log_current_vacations(count)
                if count == quantity: break     # Если нашлось нужное кол-во вакансии, то поиск прекращается
            driver.quit()                       # Закрытие браузера

        log_end_search(count, count_check_vacations)
        return [result_info_vacations, count, count_check_vacations, quantity]


class HHurl:
    """Класс, предназначенный для составления ссылки расширенного поиска."""

    def __init__(self):
        """Инициализатор класса. Создает start_url (str) - ссылка на поиск HH вакансий без каких-либо фильтров."""

        self.start_url = ('https://hh.ru/search/vacancy?L_save_area=true&items_on_page=100&hhtmFrom'
                          '=vacancy_search_filter&search_field=name&search_field=company_name&search_field'
                          '=description&enable_snippets=true&text=&')

    def get_result_main_url(self, **kwargs) -> str:
        """Функция создаёт результирующую ссылку с определёнными фильтрами в переменной kwargs.
        Именованные аргументы key kwargs: name_search, description, regions, exp, salary, exclude_words.
        Возвращает итоговую ссылку (str)"""

        if 'name_search' not in kwargs.keys():
            raise KeyError('Для поиска вакансий указан обязательный параметр name_search')
        keys = kwargs.keys()

        # --- Получение параметров ссылки ---
        name_search = kwargs['name_search']
        description = kwargs['description'] if 'description' in keys else ''
        regions = kwargs['regions'] if 'regions' in keys else ''
        exp = kwargs['exp'] if 'exp' in keys else ''
        salary = kwargs['salary'] if 'salary' in keys else ''
        exclude_words = kwargs['exclude_words'] if 'exclude_words' in keys else ''

        # --- Составление параметров ссылки ---
        params_url = self.get_params(name_search, description)
        regions_url = self.get_region(regions)
        exp_url = self.get_experience(exp)
        salary_url = self.get_salary(salary)
        exclude_words_url = self.get_exclude_words(exclude_words)

        return self.start_url + params_url + regions_url + exp_url + salary_url + exclude_words_url

    @staticmethod
    def get_params(name_search: list[..., str], description: list[..., str] | str) -> str:
        """Статическая функция для составления заголовков имени поиска вакансия и ключевых слов.
        Принимает name_search - список имён поиска (список строк),
        description - список ключевых слов (список строк).
        Возвращает готовые заголовки (str)."""

        name = 'text=Name%3A%28' + '+or+'.join(name_search) + '%29' if name_search else ''
        descript = '+and+DESCRIPTION%3A%28' + '+or+'.join(description) + '%29&' if description else ''
        return name + (descript or '&')

    @staticmethod
    def get_region(regions: list[..., str] | str) -> str:
        """Статическая функция для составления заголовков регионов поиска вакансий.
        Принимает regions - список городов (список строк).
        Возвращает готовые заголовки (str)."""

        region = {'Moscow': '1', 'St.Petersburg': '2', 'Ekaterinburg': '3'}
        if regions:
            return 'area=' + 'area='.join(f'{region[key]}&' for key in regions)
        else:
            return ''

    @staticmethod
    def get_experience(exp: str) -> str:
        """Статическая функция для составления заголовков опыта для поиска вакансий.
        Принимает exp - опыт (строка).
        Возвращает готовые заголовки (str)."""

        if exp not in ('1-3', '6', '0', ''):
            raise KeyError('Неправильно указан опыт к вакансии')
        experience = {'0': 'noExperience&', '1-3': 'between1And3&', '6': 'moreThan6&'}
        if exp:
            return 'experience=' + experience[exp]
        return ''

    @staticmethod
    def get_salary(salary: str) -> str:
        """Статическая функция для составления заголовков заработной платы вакансий.
        Принимает salary - список заработной платы (строка).
        Возвращает готовые заголовки (str)."""

        if not salary:
            return ''
        if not salary.isdigit() or salary[0] == '0':
            raise KeyError('Неправильно указана зарплата')
        return f'salary={salary}&only_with_salary=true&'

    @staticmethod
    def get_exclude_words(exclude_words: list[str] | str) -> str:
        """Статическая функция для составления заголовков исключающих слов вакансий.
        Принимает exclude_words - список исключающих слов (список строк).
        Возвращает готовые заголовки (str)."""

        if not exclude_words:
            return ''

        ru_letters = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        eng_letters = 'abcdefghijklmnopqrstuvwxyz'
        words = [word.lower() for word in exclude_words]

        for word in words:
            if len(set(word) & set(ru_letters)) > 0 and len(set(word) & set(eng_letters)) > 0:
                raise KeyError(f'Слово {word} содержит сразу и английские буквы и русские. '
                               f'В одном слове должны быть буквы только одного языка')

        res_words = [word if word[0] in eng_letters
                     else str('педагог'.encode())[2:-1].replace(r'\x', '%').upper() for word in words]
        return 'excluded_text=' + '%2C+'.join(res_words) + '&'