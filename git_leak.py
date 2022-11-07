from git import Repo
import re  # signal
import time
import signal
import sys

RED = "\033[38;5;196m"
GREEN = "\033[38;5;40m"
YELLOW = "\033[38;5;226m"
END = "\033[m"


REPO_DIR = './skale/skale-manager'
KEY_WORDS = ['credentials', 'password', 'key']  # ,'password','username','key'


def handler_signal(signal, frame):
    print('Exiting due to keyboard interrupt', end='')
    for _ in range(3):
        print('.', end='', flush=True)
        time.sleep(1)
    sys.exit(0)


def extract(repo_dir):
    repo = Repo(repo_dir)
    commits = list(repo.iter_commits('develop'))
    return commits


def transform(commits):
    commits_with_keywords = []
    for commit in commits:
        for word in KEY_WORDS:
            if re.search(word, commit.message, re.I):
                commits_with_keywords.append(commit)
    return commits_with_keywords


def load(commits):
    print('\nCommits with key-words:')
    time.sleep(1)
    for ind, commit in enumerate(commits):
        print(f'Commit {ind+1}: {commit.message}')
        time.sleep(0.1)


def progress_bar(iz, de, step):
    for i in range(iz, 1+de):
        print("\033[1A\033[2K", end="")
        x = i//3
        if i < 100:
            print(RED + step + ' ╠╣' + '█'*x + '░' *
                  (100-x) + '╠╣ ' + f'{i/3:.2f}' + f'%' + END)
        elif i < 200:
            print(YELLOW + step + ' ╠╣' + '█'*x + '░' *
                  (100-x) + '╠╣ ' + f'{i/3:.2f}' + f'%' + END)
        else:
            print(GREEN + step + ' ╠╣' + '█'*x + '░' *
                  (100-x) + '╠╣ ' + f'{i/3:.2f}' + f'%' + END)
        time.sleep(0.01)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler_signal)
    print('Starting... ╠╣' + '░'*100 + '╠╣' + '0.00%')
    time.sleep(1)
    # Extract
    commits = extract(REPO_DIR)
    progress_bar(0, 100, 'Extracting...')
    time.sleep(1)
    # Transform
    commits_with_keywords = transform(commits)
    progress_bar(101, 200, 'Transforming...')
    time.sleep(1)
    # Load
    progress_bar(201, 300, 'Loading...')
    load(commits_with_keywords)
