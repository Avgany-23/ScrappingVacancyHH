from scripts_scrapping.scrap import ScrappingHH
from scripts_scrapping.save_data import save_json
from scripts_scrapping import *
import os


if __name__ == '__main__':
    '''
    Параметр language_prog - можно указать любой язык поиска. 
    Для параметра cities доступны:  AllRegions - все регионы, Moscow - Москва, St.Petersburg - СПБ, 
                                    Ekaterinburg - Екатеренбург, Novosibirsk - Новосибирск
    '''

    # Параметры для поиска - ЗАПОЛНЯТЬ ЗДЕСЬ
    get_count_vacations = 10        # Указывается количество вакансий, которое необходимо получить с заданными фильтрами
    language_prog = 'python'        # Язык программирования
    cities = ['AllRegions']         # Список регионов поиска
    keywords = ['Django', 'Flask']  # Список ключевых слов, которые обязательно должны быть в вакансии

    vacations = ScrappingHH()       # Создание экземпляра класса для скраппинга

    # Создание ссылки с указанными параметрами (языка, города поиска). В список регионов можно добавить и другие
    main_url = vacations.create_main_url(language_prog=language_prog, cities=cities)

    # Получение вакансий по ссылке main_url, в которых содержатся ключевые слова keywords с декоратором time_decorator
    result_info_vacations = time_decorator(vacations.get_vacations)(main_url, get_count_vacations, keywords)

    # Преобразование полученных данных в формат для json-файла
    if result_info_vacations:
        res_dict = {'Общее количество просмотренных вакансий': result_info_vacations[2],
                    'Количество вакансий в json файле': result_info_vacations[1],
                    'Параметры поиска': {'Язык программирования': result_info_vacations[5],
                                         'Ключевые слова': result_info_vacations[3],
                                         'Регионы': result_info_vacations[4]},
                    'Вакансии': {}}
        for vacancy in result_info_vacations[0]:
            res_dict['Вакансии'][vacancy['url_adress']] = {'Название вакансии': vacancy['title'],
                                                           'Зарплата': vacancy['salary'],
                                                           'Компания': vacancy['name_company'],
                                                           'Требуемый опыт работы': vacancy['experience'].split(': ')[1],
                                                           'Регион': vacancy['city']}

        # Получение пути для записи и запись вакансий в файл
        path_file = os.path.join(os.getcwd(), r'result_scrapping\vacations.json')
        save_json(path_file, res_dict)
