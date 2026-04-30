import os
import time
import re

import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def calculate_expected_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    elif not salary_from and salary_to:
        return salary_to * 0.8
    else:
        return None


def get_salary_from_api(vacancy):
    salary = vacancy.get('salary') or vacancy.get('predictedSalary')

    if not salary:
        return None

    salary_from = salary.get('from')
    salary_to = salary.get('to')
    currency = salary.get('currency', 'RUR')

    if currency != 'RUR':
        return None

    return calculate_expected_salary(salary_from, salary_to)


def get_all_vacancies_by_language(language):
    url = 'https://career.habr.com/api/frontend/vacancies'
    all_vacancies = []
    page = 1
    total_pages = 1
    vacancies_found = 0

    while page <= total_pages:
        params = {'q': language, 'page': page}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if page == 1:
            total_pages = data.get('meta', {}).get('totalPages', 1)
            vacancies_found = data.get('meta', {}).get('totalResults', 0)

        all_vacancies.extend(data.get('list', []))
        page += 1
        time.sleep(0.1)

    return all_vacancies, vacancies_found


def get_habr_stats(language):
    vacancies, vacancies_found = get_all_vacancies_by_language(language)
    salaries = []

    for vacancy in vacancies[:min(100, len(vacancies))]:
        salary = get_salary_from_api(vacancy)
        if salary:
            salaries.append(salary)
        time.sleep(0.2)

    vacancies_processed = len(salaries)
    average_salary = int(sum(salaries) / len(salaries)) if salaries else None

    return {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }


def predict_rub_salary_for_superjob(vacancy):
    payment_from = vacancy.get('payment_from')
    payment_to = vacancy.get('payment_to')
    return calculate_expected_salary(payment_from, payment_to)


def get_superjob_stats(secret_key, language, town_id=4):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key
    }
    vacancies_found = 0
    salaries = []
    page = 0

    while True:
        params = {
            'keyword': language,
            'town': town_id,
            'count': 20,
            'page': page
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if page == 0:
            vacancies_found = data.get('total', 0)

        for vacancy in data.get('objects', []):
            salary = predict_rub_salary_for_superjob(vacancy)
            if salary:
                salaries.append(salary)

        if not data.get('more'):
            break

        page += 1
        time.sleep(0.2)

    vacancies_processed = len(salaries)
    average_salary = int(sum(salaries) / len(salaries)) if salaries else None

    return {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': average_salary
    }


def print_table(title, data):
    table_data = [
        ['Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата']
    ]

    for lang, stats in data.items():
        table_data.append([
            lang,
            str(stats['vacancies_found']),
            str(stats['vacancies_processed']),
            str(stats['average_salary'] or 'N/A')
        ])

    table = AsciiTable(table_data, title)
    print(table.table)


def main():
    load_dotenv()
    secret_key = os.environ['SUPERJOB_SECRET_KEY']

    languages = [
        'Python',
        'Java',
        'JavaScript',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'CSS'
    ]

    habr_stats = {lang: get_habr_stats(lang) for lang in languages}
    superjob_stats = {lang: get_superjob_stats(secret_key, lang) for lang in languages}
    print_table("Habr Moscow", habr_stats)
    print_table("SuperJob Moscow", superjob_stats)


if __name__ == '__main__':
    main()
