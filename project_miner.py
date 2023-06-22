import requests, csv
from datetime import timezone, datetime

def format_datetime(timestamp):
    formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
    return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

def pages(org: str) -> int:
    url = f'https://codecov.io/api/v2/gh/{org}/repos?active=true'
    return int(requests.get(url).json()['total_pages'])

headers = [ 'ProjectName', 'OrgName', 'LastUpdateStamp', 'Language', 'DefaultBranch']
open_source_communities = ['publiclab','apache', 'google', 'alibaba', 'kubernetes', 'facebook', 'mozilla', 'netflix'
                           ,'eclipse', 'github']

for oss_org in open_source_communities:
    with open(rf'../commits/{oss_org}RepoNamesOnly.txt', 'a+', encoding='utf-8',newline='') as f:
        writer = csv.writer(f, delimiter=',')
        total_pages = pages(oss_org)
        print('Current Organisation: ', oss_org)
        current_page = 1
        while current_page <= total_pages:
            url = f'https://codecov.io/api/v2/gh/{oss_org}/repos?active=true&page={current_page}&page_size=10'
            response = requests.get(url).json()['results']
            for project in response:
                writer.writerow([
                   project['name']
                 ])
            current_page += 1

for oss_org in open_source_communities:
    with open(rf'../commits/{oss_org}_total_detail_repos.csv', 'a+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([header for header in headers])
        total_pages = pages(oss_org)
        page = 1
        while page <= total_pages:
            url = f'https://codecov.io/api/v2/gh/{oss_org}/repos?active=true&page={page}&page_size=10'
            response = requests.get(url).json()['results']
            for project in response:
                writer.writerow([
                   project['name'] , oss_org, format_datetime(project['updatestamp']), project['language'], project['branch']
                 ])
            page += 1
