import requests

url = 'https://codecov.io/api/v2/gh/ErnestFistozz/repos/codecov-python/commits?page_size=20&branch=main&page=1'

res = requests.get(url).json()['results']
print(res)
