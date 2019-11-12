import requests
url = 'https://api.hh.ru/vacancies/'
parametres = {'text': 'программист {}'.format('python'), 'area': '1', 'period': '30','only_with_salary': 'true', 'page': 20}
page_response = requests.get(url)
page_response.raise_for_status()

page_data = page_response.json()
# if page >= page_data['pages_number']:
#     break
print(page_response.json()['items'])