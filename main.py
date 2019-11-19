import requests
from itertools import count
from dotenv import load_dotenv
import os
from terminaltables import AsciiTable


def predict_rub_salary_hh(job_title):
    salary_of_various_vacancies_hh = []
    salary_statistics_hh = {}
    for page in count(0):
        url = 'https://api.hh.ru/vacancies/'
        parametres = {'text': 'программист {}'.format(job_title),
                      'area': '1', 'period': '30',
                      'only_with_salary': 'true', 'page': page}
        page_response = requests.get(url, params=parametres)
        page_response_json = page_response.json()
        pages_number = page_response_json['pages']
        for vacancy in page_response_json['items']:
            if vacancy['salary']['currency'] != 'RUR':
                continue
            salary_from_on_hh = vacancy['salary']['from']
            salary_to_on_hh = vacancy['salary']['to']
            salary_of_various_vacancies_hh.append(
                predict_salary(salary_from_on_hh, salary_to_on_hh))
        if page >= pages_number:
            break
    salary_statistics_hh['vacancies_found'] = page_response_json['found']
    salary_statistics_hh['vacancies_processed'] = len(
        salary_of_various_vacancies_hh)
    salary_statistics_hh['average_salary'] = (
        int(sum(salary_of_various_vacancies_hh) / len(
            salary_of_various_vacancies_hh)))
    return salary_statistics_hh


def predict_rub_salary_sj(job_title, api_key):
    salary_of_various_vacancies_sj = []
    salary_statistics_sj = {}
    for page in count(0):
        url = 'https://api.superjob.ru/2.27/vacancies'
        headers = {'X-Api-App-Id': api_key}
        parametres = {'keyword': 'программист {}'.format(job_title),
                      'town': '4', 'catalogues': '48',
                      'page': page, 'count': '100'}
        page_response = requests.get(url, headers=headers, params=parametres)
        page_response_json = page_response.json()
        for vacancy in page_response_json['objects']:
            if vacancy['currency'] != 'rub':
                continue
            superjob_salary_to = vacancy['payment_to']
            superjob_salary_from = vacancy['payment_from']
            if superjob_salary_from == 0 and superjob_salary_to == 0:
                break
            salary_of_various_vacancies_sj.append(
                predict_salary(superjob_salary_from, superjob_salary_to))
        if not page_response_json['more']:
            break
    if len(salary_of_various_vacancies_sj) != 0:
        salary_statistics_sj['vacancies_found'] = page_response_json['total']
        salary_statistics_sj['vacancies_processed'] = len(
            salary_of_various_vacancies_sj)
        salary_statistics_sj['average_salary'] = (
            int(sum(salary_of_various_vacancies_sj) / len(
                salary_of_various_vacancies_sj)))
        return salary_statistics_sj


def predict_salary(salary_from, salary_to):
    if salary_from is None and salary_to is not None:
        return salary_to * 0.8
    elif salary_to is None and salary_from is not None:
        return salary_from * 1.2
    elif salary_from is not None and salary_to is not None:
        return (salary_to + salary_from) / 2
    elif salary_to is None and salary_from is None:
        None
    elif salary_to == 0 and salary_from == 0:
        None


def generate_statistics_table(language_salary_statistics, title):
    table_data = [['Язык программирования', 'Вакансий найдено',
                   'Вакансий обработано', 'Средняя зарплата'], ]
    for programming_language in language_salary_statistics.keys():
        current_language_ststistics = [programming_language]
        if language_salary_statistics[programming_language] is not None:
            for statistics_category in \
                    language_salary_statistics[programming_language].keys():
                current_language_ststistics.append(
                    language_salary_statistics[programming_language][
                        statistics_category])
        table_data.append(current_language_ststistics)
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    return table_instance.table + '\n'


if __name__ == '__main__':
    load_dotenv()
    sj_api_key = os.getenv('SUPERJOB_API_KEY')
    popular_programming_languages = ['Python', 'Java',
                                     'Javascript', 'Ruby',
                                     'Objective-C', 'C#',
                                     '1C', 'Shell']
    language_salary_statistics_hh = {}
    language_salary_statistics_sj = {}
    for programming_language in popular_programming_languages:
        language_salary_statistics_hh[
            '{}'.format(programming_language)] = predict_rub_salary_hh(
                programming_language)
        language_salary_statistics_sj[
            '{}'.format(programming_language)] = predict_rub_salary_sj(
                programming_language, sj_api_key)
    print(generate_statistics_table(
        language_salary_statistics_sj, 'SuperJob Moscow'))
    print(generate_statistics_table(
        language_salary_statistics_hh, 'HeadHunter Moscow'))
