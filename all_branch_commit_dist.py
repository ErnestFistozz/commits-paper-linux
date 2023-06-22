import requests, csv
from pydriller import Repository
import pandas as pd
from datetime import timezone, datetime

headers = ['CommitHash', 'Date', 'CommitMessage', 'CommitMessageSize', 'CommitLines', 'IsMergeRequest', 'NumberFilesChanged']

def format_datetime(timestamp):
    formated_timestamp = datetime.fromisoformat(timestamp[:-1]).astimezone(timezone.utc)
    return formated_timestamp.strftime('%Y-%m-%d %H:%M:%S')

df = pd.read_csv('projects.txt',header=None)

for index in range(len(df)):
    with open(rf'../commits/{df.iloc[index].values[0]}_all_branch_commits.csv', 'a+', encoding='utf-8', newline='\n') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([header for header in headers])
        try:
            gh_repo = f'../commits/{df.iloc[index].values[0]}'
            for commit in Repository(path_to_repo=gh_repo).traverse_commits():
                date, commit_hash, message, commit_msg_size = commit.committer_date, commit.hash, commit.msg, len(commit.msg)
                lines = commit.lines
                is_merge_commit = 'Yes' if commit.merge else 'No'
                no_of_files_modified = commit.files
                writer.writerow([commit_hash, date, message, commit_msg_size, lines, is_merge_commit, no_of_files_modified])
        except:
            continue
