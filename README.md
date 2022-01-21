**Задача: спроектировать и разработать API для системы опросов пользователей.**

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание.
После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса,
тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя
в API передается числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может
участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по развертыванию приложения (в docker или локально)
- документация по API



**Инструкция по развертыванию приложения**

1. Открыть терминал
2. Создать папку для проекта: mkdir project_survey
3. Перейти в папку: cd project survey
4. Скачать репозиторий: git clone https://github.com/KorkhovPavel/fr.git
5. Создать виртуальное окружение: python3 -m venv env
6. Активировать виртуальное окружение: source env/bin/activate (деактивация deactivate)
7. Перейти в папку: сd fr
8. Установить зависимости pip install -r requirements.txt
9.  Перейти в папку: сd fr
10. Cоздаем миграции: python manage.py makemigrations
11. Применяем миграции: python manage.py migrate
12. Создаем суперпользователя: python manage.py createsuperuser
13. Запустить python manage.py runserver
14. Зайти в админпанель, создать токен (нужен для авторизации запросов)

**Документация по API**

1. Добавить опрос, вопросы, варианты ответов(запрос POST)
`http://127.0.0.1:8000/api/v1/api_surveys/survey/create/`
 пример запроса: test_data/create_survey.json (что бы опрос был активный меняем дату начала на сегодня)
 Описание:
  - создать один опрос
  - добавить массово вопросы и варианты ответов
  - авторизация обязательна (токен)
2. Изменить опрос, вопросы, варианты ответов(запросы DELETE,PUT)
 `http://127.0.0.1:8000/api/v1/api_surveys/survey/upload-del/id/`
  пример запроса(изменена дата окончания опроса и текст последнего вопроса): test_data/create_survey.json
  Описание:
  - вместо id номер опроса
  - изменить один опрос
  - изменить массово вопросы и варианты ответов
  - авторизация обязательна (токен)
  - изменить дату начала опроса нельзя
3. Получение списка активных опросов(запрос GET)
 `http://127.0.0.1:8000/api/v1/api_surveys/survey/view/active`
  Описание:
  - получить список активных вопросов
  - авторизация не нужна
4. Прохождение опроса (запрос POST)
`http://127.0.0.1:8000/api/v1/api_surveys/answer/create/`
 пример запроса: test_data/create_answer.json
 описание:
  - чтобы персонализировать ответы введи id, можно анонимно
  - отправить данные
5. Получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя(Запрос GET)
` http://127.0.0.1:8000/api/v1/api_surveys/answer/detail/`
  описание:
   -в теле запроса отправляем json вида {"id":1166}, где значение id это id пользователя
 