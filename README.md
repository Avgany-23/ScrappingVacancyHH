# Скрипт для скрапинга вакансий на HeadHunter.

### _[Техническая документация находится в файле 'CodeDocumentation.md'.](./CodeDocumentation.md)_

----

Скрипт позволяет просматривать вакансии на HH и отбирать вакансии с указанными параметрами в файле main.py.

![image](https://github.com/user-attachments/assets/3b3e5f88-4fed-4a44-8f4b-0e899105d1fb)

По данными параметрам будет отобрано 10 python вакансий по всем доступным регионам, в которых содержатся ключевые слова 'Django' или 'Flask'. Ссылка поиска вакансий при указанным параметрах будет выглядеть следующим образом:

--> https://spb.hh.ru/search/vacancy?text=python&area=true

_При желании можно указать свои параметры. Для регионов доступны следующие имена:_

- AllRegions - все регионы 
- Moscow - Москва 
- St.Petersburg - СПБ 
- Ekaterinburg - Екатеренбург 
- Novosibirsk - Новосибирск

При необходимости можно добавить дополнительные регионы поиска в модуле scripts_scrapping/scrap.py, строка 61, для этого нужно знать коды регионов HH. Например, 1 - это код Москвы на HH, 2 - СПБ и т.д: 

--> https://spb.hh.ru/search/vacancy?text=python&area=true%page=N - где N - номер страницы (1 - вторая страница поиска, 2 - третья страница поиска и т.д.).

✲ При запуске скрипт анализирует страницу по выбранным параметрам, отбирает ссылки на вакансии и начинает их анализ. Если указанное количество поиска вакансий на странице не набралось, то скрипт переходит на вторую страницу и так до тех пор, пока не найдётся нужно количество вакансий или не закончатся доступные вакансии по указанным параметрам.

✲ Во время работы скрипта в консоли будет отображаться текущий прогресс. После окончания поиска данные будут записаны в json файл по указанному пути в переменной path_file (строка 44 в файле main.py). При необходимости можно закончить работу скрипта досрочно, просто остановив работу скрипта или закрыв браузер, найденные файлы при этом не удалятся, а всё так же сохранятся в json. Так же будет отображено, сколько нашлось вакансий, выборка поиска, путь сохранения данных и время, потраченное на поиск:

![image](https://github.com/user-attachments/assets/d1c6df5e-148c-4848-ad56-b77d4900aeec)

_Содержимое файла json выглядит следующим образом:_

![image](https://github.com/user-attachments/assets/07f042f8-15ed-4f99-b000-a0b0dc81398b)

Вначале в нём указаны параметры поиска, а далее (в значении ключа 'Вакансии') перечисляются найденные вакансии.
