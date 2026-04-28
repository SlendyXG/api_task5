import os
import time
import re

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def parse_salary_from_text(salary_text):
    if not salary_text:
        return None

    salary_text = salary_text.replace(' ', '').replace(' ', '')
    salary_text = salary_text.replace('₽', '').replace('руб.', '').strip()
    numbers = re.findall(r'\d+', salary_text)
    numbers = [int(n) for n in numbers]

    if not numbers:
        return None

    if len(numbers) == 1:
        if 'до' in salary_text.lower():
            return int(numbers[0] * 0.8)
        else:
            return int(numbers[0] * 1.2)
    else:
        return int((numbers[0] + numbers[1]) / 2)


def get_all_vacancy_ids_by_language(language):
    url = 'https://career.habr.com/api/frontend/vacancies'
    vacancy_ids = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        params = {'q': language, 'page': page}
        response = requests.get(url, params=params)
        data = response.json()

        if page == 1:
            total_pages = data.get('meta', {}).get('totalPages', 1)

        for vacancy in data.get('list', []):
            vacancy_ids.append(vacancy['id'])

        page += 1
        time.sleep(0.1)

    return vacancy_ids


def get_salary_from_vacancy_page(vacancy_id):
    url = f'https://career.habr.com/vacancies/{vacancy_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    salary_block = soup.find('div', class_='basic-salary')
    if salary_block:
        return parse_salary_from_text(salary_block.get_text(strip=True))
    return None


def get_habr_stats(language):
    vacancy_ids = get_all_vacancy_ids_by_language(language)
    vacancies_found = len(vacancy_ids)

    salaries = []

    for vac_id in vacancy_ids[:min(100, len(vacancy_ids))]:
        salary = get_salary_from_vacancy_page(vac_id)
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

    if not payment_from and not payment_to:
        return None

    if payment_from and payment_to:
        return (payment_from + payment_to) / 2
    elif payment_from and not payment_to:
        return payment_from * 1.2
    elif not payment_from and payment_to:
        return payment_to * 0.8

    return None


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
    print(f"\n{title}")
    print("+" + "-" * 20 + "+" + "-" * 16 + "+" + "-" * 19 + "+" + "-" * 16 + "+")
    print(
        f"| {'Язык программирования':<18} | {'Найдено вакансий':<14} | {'Обработано вакансий':<17} | {'Средняя зарплата':<14} |")
    print("+" + "-" * 20 + "+" + "-" * 16 + "+" + "-" * 19 + "+" + "-" * 16 + "+")

    for lang, stats in data.items():
        print(
            f"| {lang:<18} | {stats['vacancies_found']:<14} | {stats['vacancies_processed']:<17} | {stats['average_salary'] or 'N/A':<14} |")

    print("+" + "-" * 20 + "+" + "-" * 16 + "+" + "-" * 19 + "+" + "-" * 16 + "+" + "\n")


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