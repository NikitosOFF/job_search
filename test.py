import requests
from itertools import count


def predict_rub_salary_sj(job_title):
    salary_of_various_vacancies_sj = []
    salary_statistics_sj = {}
    for page in count(0):
        url = 'https://api.superjob.ru/2.27/vacancies'
        headers = {'X-Api-App-Id': 'v3.r.131240819.c88ba89c9389ac1ef1c5c98ef8dd98263f535d8f'
                                   '.f9d7c1bb29e616d4e391144493bf0e8ecd36d51e'}
        parametres = {'keyword': 'программист {}'.format(job_title), 'town': '4', 'catalogues': '48', 'page': page,
                      'count': '100'}
        page_response = requests.get(url, headers=headers, params=parametres)
        for vacancy in page_response.json()['objects']:
            if vacancy['currency'] != 'rub':
                break
            else:
                superjob_salary_to = vacancy['payment_to']
                superjob_salary_from = vacancy['payment_from']
                if superjob_salary_from == 0 and superjob_salary_to == 0:
                    break
                salary_of_various_vacancies_sj.append(predict_salary(superjob_salary_from, superjob_salary_to))
        if not page_response.json()['more']:
            break
    if len(salary_of_various_vacancies_sj) != 0:
        salary_statistics_sj['vacancies_found'] = page_response.json()['total']
        salary_statistics_sj['vacancies_processed'] = len(salary_of_various_vacancies_sj)
        salary_statistics_sj['average_salary'] = (
            int(sum(salary_of_various_vacancies_sj) / len(salary_of_various_vacancies_sj)))
    return salary_statistics_sj


def predict_salary(salary_from, salary_to):
    if salary_from is None and salary_to is not None:
        return salary_to * 0.8
    elif salary_to is None and salary_from is None:
        return salary_from * 1.2
    elif salary_from is not None and salary_to is not None:
        return (salary_to + salary_from) / 2
    elif salary_to == 0 and salary_from == 0:
        None


popular_programming_languages = ['Python', 'Java', 'Javascript', 'Ruby', 'Objective-C', 'Swift', 'Go', 'Shell']
language_salary_statistics_hh = {}
language_salary_statistics_sj = {}
for programming_language in popular_programming_languages:
    # language_salary_statistics_hh['{}'.format(programming_language)] = predict_rub_salary_hh(programming_language)
    language_salary_statistics_sj['{}'.format(programming_language)] = predict_rub_salary_sj(programming_language)
print(language_salary_statistics_sj)
