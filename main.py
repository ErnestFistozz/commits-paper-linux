import requests, csv
from datetime import timezone, datetime
from pydriller import Repository
import pandas as pd

#Bug/Fix, Upgrade/Update/Dedependecy/Version, Feature/Insets, Merge

headers = [ 'CommitHash', 'ProjectName' , 'OrgName' , 'Date', 'CommitMessage', 'CommitMessageSize', 'CommitLines', 'IsMergeRequest', 'NumberFilesChanged']

def format_datetime(timestamp):
    formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
    return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

def get_latest_commit( org: str, repo_name: str) -> str:
    branch, page, size = 'master', 1 , 1
    url = f'https://codecov.io/api/v2/gh/{org}/repos/{repo_name}/commits?branch={branch}&page={page}&page_size={size}'
    response = requests.get(url).json()['results'][0]
    date, hash, message = format_datetime(response['timestamp']), response['commitid'],  \
        response['message']
    return date, hash, message, len(response['message'])

oss_coms = ['publiclab','google','alibaba', 'kubernetes', 'apache','facebook', 'netflix','eclipse', 'github']

with open(rf'../commits/overall_commits.csv', 'a+', encoding='utf-8',newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([header for header in headers])
        for oss in oss_coms:
            df = pd.read_csv(rf'../commits/{oss}_total_detail_repos.csv', delimiter = ',', header=1)
            for index, row in df.iterrows():
                try:
                    gh_repo = f'../commits/{row[0].lower()}'
                    
                    date, hash, message, commit_msg_size = get_latest_commit(row[1],row[0])
                    for commit in Repository(path_to_repo=gh_repo, single=hash).traverse_commits():
                        lines = commit.lines
                        is_merge_commit = 'Yes' if commit.merge else 'No'
                        no_of_files_modified = commit.files
                    writer.writerow([hash, row[0].lower(), row[1].lower(), date, message, commit_msg_size, lines, is_merge_commit, no_of_files_modified ])
                except:
                    print(gh_repo)
                    continue
