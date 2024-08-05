from scripts_scrapping.scrap import ScrappingHH, HHurl
from scripts_scrapping.save_data import save_json
from scripts_scrapping import *
import os


if __name__ == '__main__':
    '''
    Параметр language_prog - можно указать любой язык поиска. 
    Для параметра cities доступны:  '' - все регионы, Moscow - Москва, St.Petersburg - СПБ, 
                                    Ekaterinburg - Екатеренбург, Novosibirsk - Новосибирск
    '''

    # ------ Параметры для поиска - ЗАПОЛНЯТЬ ЗДЕСЬ ------
    search = ['python', 'django', 'drf', 'backend', 'fastapi', 'flask']  # Имя поиска (обязательно ввести хотя бы 1)
    descriptions = ['django', 'drf', 'fastapi', 'flask']                 # Ключевые слова (необязательно)
    regions = ['Moscow', 'St.Petersburg', 'Ekaterinburg']                # Регионы (необязательно)
    del_words = ['Педагог', 'Devops', 'Java']                            # Исключаемые из вакансии слова (необязательно)
    experience = '1-3'                                                   # Опыт (необязательно)
    salary = '52000'                                                     # Зарплата ОТ (необязательно)
    # ------------------------------------------------------

    class_url = HHurl()
    main_url = class_url.get_result_main_url(name_search=search, description=descriptions, regions=regions,
                                             exp=experience, salary=salary, exclude_words=del_words)

    # Создание класса для поиска вакансий и их получения
    vacations = ScrappingHH(main_url, show_search=True)
    result_info_vacations = time_decorator(vacations.get_vacations)(quantity=10)

    if result_info_vacations[0]:
        # Преобразование полученных данных в формат для json-файла
        res_dict = {'Указанное количество на получение вакансий': result_info_vacations[0][3],
                    'Итоговое количество просмотренных вакансий': result_info_vacations[0][2],
                    'Итоговое количество вакансий в json файле': result_info_vacations[0][1],
                    'Время поиска вакансий': result_info_vacations[1][:-1],
                    'Вакансии': {}}

        for vacancy in result_info_vacations[0][0]:
            res_dict['Вакансии'][vacancy['url_address']] = {'Название вакансии': vacancy['title'],
                                                            'Зарплата': vacancy['salary'],
                                                            'Компания': vacancy['name_company'],
                                                            'Требуемый опыт работы': vacancy['experience'].split(': ')[1],
                                                            'Регион': vacancy['city']}

        # Получение пути для записи и запись вакансий в файл
        path_file = os.path.join(os.getcwd(), r'result_scrapping\vacations.json')
        save_json(path_file, res_dict)
