## Проект - парсер вакансий с платформы HeadHunter.

Программа получает данные о работодателях и их вакансиях с сайта hh.ru.
Затем данные сохраняются в базу данных PostgreSQL. Для подключения к базе необходимо создать файл 'database.ini', в котором указать параметры для подключения (имя пользователя и пароль)
После этого можно выбрать некоторые действия с данными (Получить список кампаний или вакансий и т.п.)

#### Структура проекта:

В пакете src:
1. classes.py - файл с классом для взаимодействия с API HeadHunter. И классом для взаимодействия с базой данных.
2. config.py - файл для взаимодействия с 'database.ini'
3. utils.py - файл с основными функциями программы

#### Используется виртуальное окружение poetry

#### Для запуска программы используйте файл main.py в основной ветке
