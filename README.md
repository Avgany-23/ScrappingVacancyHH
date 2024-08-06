# Скрипт для скрапинга вакансий на HeadHunter.

### _[Техническая документация находится в файле 'CodeDocumentation.md'.](./CodeDocumentation.md)_

----

Скрипт позволяет просматривать вакансии на HH и отбирать вакансии с указанными параметрами в файле main.py. Скрипт работает на основе браузера Chrome (он должен быть установлен на компьютере). 

**Для запуска нужно установить зависимости проекта, изменить (или оставить) параметры поиска и запустить модуль main.py.**

----

![image](https://github.com/user-attachments/assets/4506c953-97fc-4317-9ab5-f5929579811a)



По данными параметрам будет отобрано 10 вакансий, в названии которых содержатся слова python, django, drf, backend, fastapi, flask по регионам Москва, СПБ и Екатеренбург, в которых содержатся ключевые слова 'Django', 'drf', 'fastapi' или 'Flask', требуемый опыт при поиске будет указан 1-3 года, зарплата от 52 тысяч рублей. Так же будут игнорироваться вакансии, которые содержат в себе слова 'Педагог', 'Devops' или 'Java'.

### Перед запуском в файле main.py в переменной vacations (строка 28) параметр show_search можно установить на False, после чего при работе скрипта браузер открываться не будет и скорость поиска увеличиться примерно на 20%. В следующей переменной параметр quantity отвечает за количество вакансий, которое будет найдено. По умолчанию стоит 10.

__В выражении main_url = class_url.get_result_main_url(name_search=search, description=descriptions, regions=regions, exp=experience, salary=salary, exclude_words=del_words):__
1) name_search - обязательный параметр. Список должен содержать в себе как минимум одно слово для поиска;
2) description - дополнительный параметр, если не указывать, то применён не будет. Ключевые слова в вакансии указываются в списке;
3) regions - дополнительный параметр, если не указывать, то поиск будет совершаться по всем регионам. Регионы указываются в списке. При необходимости можно добавить дополнительные регионы поиска в модуле scripts_scrapping/scrap.py, в переменной region в методе get_region (строка218). Для этого нужно знать коды регионов HH. Например, 1 - это код Москвы на HH, 2 - СПБ и т.д;
4) exp - дополнительный параметр, если не указывать, то будет выдават вакансии с любым опытом. Указывается в строке в трех вариантах '1-3', '6' или '0';
5) salary - дополнительный параметр, если не указывать, то будет искать вакансии с любой ЗП. Указывается строка. Например, '100000' - значит от 100 тысяч рублей;
6) exclude_words - дополнительный параметр, позволяет указать список слов. Вакансии, содержащие указанные слова, в поиск попадать не будут.

__Для более расширенного поиска можно добавить новые методы в класс HHurl (scripts_scrapping/scrap.py) и импортировать их в метод get_result_main_url, соединив с главной ссылкой__

_---> При данных программа сгенерирует ссылку и начнет поиск. Но HH может поменять пути в HTML-элементах, из-за чего может нарушиться логика работы. В таком случае потребуется изменить пути поиска. Изменение может затронуть следующие параметры в файле scripts_scrapping/scrap.py:_
* Базовая ссылка для поиска находится на строке 171;
* Составление дополнительных заголовков (имена поиска, ключевые слова, ЗП, опыт и т.д.) находится в метода класса HHurl (get_params, get_region, get_experience и т.д.);
* Путь для поиска ссылок на вакансии находится в переменной path_HTML в строке 83;
* Пути для поиска названия вакансии, имя компании, региона вакансии, требуемого опыта и заработной платы находятся в строчках 97-101.

✲ При запуске скрипт анализирует страницу по выбранным параметрам, отбирает ссылки на вакансии и начинает их анализ. Если указанное количество поиска вакансий на странице не набралось, то скрипт переходит на вторую страницу и так до тех пор, пока не найдётся нужно количество вакансий или не закончатся доступные вакансии по указанным параметрам.

✲ Во время работы скрипта в консоли будет отображаться текущий прогресс. После окончания поиска данные будут записаны в json файл по указанному пути в переменной path_file (строка 48 в файле main.py). При необходимости можно закончить работу скрипта досрочно, просто остановив работу скрипта (нажать надо будет 2 раза), найденные файлы при этом не удалятся, а всё так же сохранятся в json. Так же будет отображено, сколько нашлось вакансий, выборка поиска, путь сохранения данных и время, потраченное на поиск:

![image](https://github.com/user-attachments/assets/d1c6df5e-148c-4848-ad56-b77d4900aeec)

_Содержимое файла json выглядит следующим образом:_

![image](https://github.com/user-attachments/assets/21b08147-8c32-40e1-9cf4-70ba100a7f02)

Вначале в нём указаны параметры поиска, а далее (в значении ключа 'Вакансии') перечисляются найденные вакансии.

_Функции в скрипте перехватют множество исключений. В большинстве слючаев, при возникновении ошибок или случанйных действий пользователя (например, закрытие браузера во время работы), программа продолжит работать. Если же остановить программу досрочно, текущие данные сохранятся в файл json. Поэтому найденная информация утеряна не будет._
