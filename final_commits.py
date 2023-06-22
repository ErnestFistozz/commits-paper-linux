import requests, csv
from datetime import timezone, datetime

def format_datetime(timestamp):
    formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
    return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

base_url = 'https://codecov.io/api/v2/gh'

def total_project_pages(org: str) -> int:
    url = f'{base_url}/{org}/repos?active=true'
    return int(requests.get(url).json()['total_pages'])

def total_project_commits_pages(org: str, project: str) -> int:
    url = f'{base_url}/{org}/repos/{project}/commits'
    return int(requests.get(url).json()['total_pages'])

headers = [ 'ProjectName', 'OrgName', 'Language', 'CommitHash', 'CommitDate','CommitMessage', 'CommitMessageSize']
open_source_communities = ['netflix','github',  'publiclab','facebook','eclipse', 'google', 'alibaba', 'kubernetes', 'mozilla','apache']

with open(rf'../commits/all_projects.csv', 'a+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([header for header in headers])

        for org in open_source_communities:
            total_projects_pages = total_project_pages(org)
            starting_page = 1
            project_names = []
            
            # Gets all orojects for A Particular Organization
            while starting_page <= total_projects_pages:
                url = f'{base_url}/{org}/repos?active=true&page={starting_page}&page_size=20'
                result = requests.get(url).json()['results']
                for project in result:
                    project_names.append([project['name'], project['language']])
                    
                starting_page += 1
            # For each Project, Get ALL commmist
            for current_project in project_names:
                try:
                    if org == 'publiclab':
                        commits_url=f'{base_url}/{org}/repos/{current_project[0]}/commits?page_size=20&branch=main'
                    else:
                        commits_url=f'{base_url}/{org}/repos/{current_project[0]}/commits?page_size=20&branch=master'
                    total_commits_pages = total_project_commits_pages(org,current_project[0])
                    commit_page  = 1
                    while commit_page <= total_commits_pages:
                        this_commit = f'{commits_url}&page={commit_page}'
                        response = requests.get(this_commit).json()['results']
                        for d in response:
                            commit_hash, date, msg = d['commitid'], format_datetime(d['timestamp']), d['message']
                            writer.writerow([current_project[0], org, current_project[1], commit_hash, date,  msg, len(msg)])
                        commit_page += 1
                except:
                    continue
