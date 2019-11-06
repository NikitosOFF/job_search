import requests


def predict_rub_salary(job_title):
    url = 'https://api.hh.ru/vacancies/'
    parametres = {'text': 'программист {}'.format(job_title), 'area': '1', 'period': '30', 'only_with_salary': 'true'}
    response = requests.get(url, params=parametres)
    salary_of_various_vacancies = []
    for vacancy in response.json()['items']:
        if vacancy['salary']['currency'] != 'RUR':
            break
        elif vacancy['salary']['from'] is None:
            salary_of_various_vacancies.append(vacancy['salary']['to'] * 0.8)
        elif vacancy['salary']['to'] is None:
            salary_of_various_vacancies.append(vacancy['salary']['from'] * 1.2)
        elif vacancy['salary']['from'] is not None and vacancy['salary']['to'] is not None:
            salary_of_various_vacancies.append((vacancy['salary']['to'] + vacancy['salary']['from']) / 2)
    print(salary_of_various_vacancies)
    print(len(salary_of_various_vacancies))
    print(response.json()['found'])


popular_programming_languages = ['Python', 'Java', 'Javascript', 'Ruby', 'PHP', 'Swift', 'Go', 'Shell']
for programming_language in popular_programming_languages:
    predict_rub_salary(programming_language)
# number_of_programming_language_vacancies={}
# programming_languages = ['Python', 'Java', 'Javascript', 'Ruby', 'PHP', 'C++', 'C#', 'C']
# lang = ['Python']
# for lang in programming_languages:
# url = 'https://api.hh.ru/vacancies/'
# parametres = {'text': 'программист {}'.format(lang), 'area': '1', 'period' : '30', 'only_with_salary': 'true'}
# response = requests.get(url, params=parametres)
# response.raise_for_status()
# number_of_programming_language_vacancies[lang]=response.json()['found']
# print([vacancy['salary'] for vacancy in response.json()['items']])
# print(number_of_programming_language_vacancies)
# predict_rub_salary(input())
