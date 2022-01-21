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
в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может
участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API


**Инструкция по разворачиванию приложения**

1. Установка Python 3.9.9
2. Создать папку для проекта mkd
3. Перйтив папку и создать виртуальное окружение python3 -m venv env (если нет установить pip install virtualenv)
4. Активировать source env/bin/activate деактивация deactivate
5. Скачать репозиторий git clone https://github.com/KorkhovPavel/fr.git
6. Установить зависимости pip install -r /path/to/requirements.txt
7. Запустить python manage.py runserver

db:
user: admin
password: 123qwe234

