import requests
import psycopg2


class HeadHunterAPI:
    """Класс для работы с API платформы HeadHunter"""

    def __init__(self, keyword: str):
        self.employers_url = 'https://api.hh.ru/employers'
        self.vacancies_url = 'https://api.hh.ru/vacancies'
        self.params = {
            'text': keyword,
            'area': 113,
            'only_with_vacancies': True,
            'page': 0,
            'per_page': 100,
        }

    def get_employers(self):
        """Метод, который возвращает работодателей по заданному параметру"""

        response = requests.get(self.employers_url, params=self.params)
        return response.json()['items']


class DBManager:
    """Класс для взаимодействия с базой данных"""

    def __init__(self, db_name: str, params: dict):
        self.db_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех кампаний и количество вакансий у каждой кампании"""
        connect = psycopg2.connect(database=self.db_name, **self.params)
        try:
            with connect as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT employer_name, COUNT(vacancy_name) FROM employers '
                                'JOIN vacancies USING(employer_id)'
                                'GROUP BY employer_id')
                    rows = cur.fetchall()
            return rows
        finally:
            conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий"""
        connect = psycopg2.connect(database=self.db_name, **self.params)
        try:
            with connect as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT vacancy_name, salary_from, salary_to, salary_currency, vacancies.url, employer_name '
                        'FROM vacancies LEFT JOIN employers USING(employer_id)')
                    rows = cur.fetchall()
            return rows
        finally:
            conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        connect = psycopg2.connect(database=self.db_name, **self.params)
        try:
            with connect as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT AVG(salary_from) AS avg_salary_from, '
                        'AVG(salary_to) AS avf_salary_to '
                        'FROM vacancies')
                    rows = cur.fetchall()
            return rows
        finally:
            conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий у которых з/п выше средней"""
        connect = psycopg2.connect(database=self.db_name, **self.params)
        try:
            with connect as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT vacancy_name FROM vacancies '
                        'WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies) '
                        'AND salary_to > (SELECT AVG(salary_to) FROM vacancies)')
                    rows = cur.fetchall()
            return rows
        finally:
            conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """Получает вакансии по ключевому слову"""
        connect = psycopg2.connect(database=self.db_name, **self.params)
        try:
            with connect as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT * FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{keyword}%'")
                    rows = cur.fetchall()
            return rows
        finally:
            conn.close()
