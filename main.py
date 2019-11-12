import requests
from itertools import count


def predict_rub_salary(job_title):
    salary_of_various_vacancies = []
    salary_statistics = {}
    for page in count(0):
        url = 'https://api.hh.ru/vacancies/'
        parametres = {'text': 'программист {}'.format(job_title), 'area': '1', 'period': '30',
                      'only_with_salary': 'true', 'page': page}
        page_response = requests.get(url, params=parametres)
        pages_number = page_response.json()['pages']
        for vacancy in page_response.json()['items']:
            if vacancy['salary']['currency'] != 'RUR':
                break
            elif vacancy['salary']['from'] is None:
                salary_of_various_vacancies.append(vacancy['salary']['to'] * 0.8)
            elif vacancy['salary']['to'] is None:
                salary_of_various_vacancies.append(vacancy['salary']['from'] * 1.2)
            elif vacancy['salary']['from'] is not None and vacancy['salary']['to'] is not None:
                salary_of_various_vacancies.append((vacancy['salary']['to'] + vacancy['salary']['from']) / 2)
        if page >= pages_number:
            break
    salary_statistics['vacancies_found'] = page_response.json()['found']
    salary_statistics['vacancies_processed'] = len(salary_of_various_vacancies)
    salary_statistics['average_salary'] = (int(sum(salary_of_various_vacancies) / len(salary_of_various_vacancies)))
    return salary_statistics


popular_programming_languages = ['Python', 'Java', 'Javascript', 'Ruby', 'Objective-C', 'Swift', 'Go', 'Shell']
language_salary_statistics = {}
for programming_language in popular_programming_languages:
    language_salary_statistics['{}'.format(programming_language)] = predict_rub_salary(programming_language)
print(language_salary_statistics)
