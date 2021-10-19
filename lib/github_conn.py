import os
import sys
import requests
from datetime import datetime
import datetime as DT


today = DT.date.today()
yesterday = str(today - DT.timedelta(days=1))
BASE_URL = 'https://api.github.com'
GITHUB_ORG = 'mozilla-mobile'


class Github:
    #BASE_URL_ISSUES = 'https://api.github.com/search/issues?q=repo:mozilla-mobile/'


    def __init__(self):
        try:
            self.API_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
            self.API_HEADER = {'Authorization': self.API_TOKEN,
                               'accept': 'application/json'}
        except KeyError:
            print("ERROR: GITHUB_TOKEN env var not set")
            exit()



    def get_app(self, project):
        if not self.APP_REPO:
            resp = requests.get('https://api.github.com/search/issues?q=repo:mozilla-mobile/{0}'.
                                format(project, label),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                print('GET /apps/ {}'.format(resp.status_code))
                sys.exit(1)
            return resp.json()

    def get_open_label(self, project, label):
        if not self.APP_REPO:
            resp = requests.get(('https://api.github.com/search/issues?q=repo:mozilla-mobile/{0}+is:issue+is:open+label:' + label).
                                format(project),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                print('GET /apps/ {}'.format(resp.status_code))
                sys.exit(1)
            open_issues_label_count = resp.json()
            return open_issues_label_count['total_count']

    def get_closed_label(self, project, label):
        if not self.APP_REPO:
            resp = requests.get(('https://api.github.com/search/issues?q=repo:mozilla-mobile/{0}+is:issue+is:closed+label:' + label).
                                format(project),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                print('GET /apps/ {}'.format(resp.status_code))
                sys.exit(1)
            closed_issues_label_count = resp.json()
            return closed_issues_label_count['total_count']

    def get_open_by_day(self, project, label):
            resp = requests.get(('https://api.github.com/search/issues?q=repo:mozilla-mobile/{0}+is:issue+is:open+label:' + label + 'created:>=' + yesterday).
                                format(project),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                print('GET /apps/ {}'.format(resp.status_code))
                sys.exit(1)
            open_issues_day = resp.json()
            return open_issues_day['total_count']

    def get_closed_by_day(self, project, label):
            resp = requests.get(('https://api.github.com/search/issues?q=repo:mozilla-mobile/{0}+is:issue+is:closed+label:' + label + 'created:>=' + yesterday).
                                format(project),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                print('GET /apps/ {}'.format(resp.status_code))
                sys.exit(1)
            closed_issues_day = resp.json()
            return closed_issues_day['total_count']        


class GithubHelpers():

    def __init__(self):
        self.gh = Github()


    def github_url(project,labels):
        # TODO
        #BASE_URL_ISSUES = 'https://api.github.com/search/issues?q=repo:mozilla-mobile/'
        path = ''
        url = '{0}/{1}'.format(BASE_URL, path)
        return url

    def issue_url(self, project, labels, status=''):
        # TODO
        # labels = 
        if not status:
            label_status = ''
        elif status == 'open':
            label_status = 'is:open'
        else:
             label_status = 'is:closed'

        labels = 'eng:intermittent-test'

        return  '{0}/search/issues?q=repo:{1}/{2}+is:issue+{3}+label:{4}'.format(BASE_URL, GITHUB_ORG, project, label_status, labels)


        

def main():
    #project = 'reference-browser'
    #project = 'android-components'
    #project = 'focus-android'
    project = 'fenix'
    labels = "eng:intermittent-test"
    status = 'open'

    g = GithubHelpers()
    url = g.issue_url(project, labels, status) 
    print(url)
    """
    # Get general count of issues (any type)
    repo_open_issues_label = b.get_open_label(args.project, args.label)
    repo_closed_issues_label = b.get_closed_label(args.project, args.label)


    # Get open issues (any type) at a particular date
    repo_open_issues_today = b.get_open_by_day(args.project, args.label)
    repo_closed_issues_today = b.get_closed_by_day(args.project, args.label)
    """

if __name__ == '__main__':
    main()

