import os
import sys
import json
from prettytable import PrettyTable
import requests

API_BASE = 'https://api.github.com'
OWNER = 'mozilla-mobile'


# EXAMPLE
# https://api.github.com/search/issues?q=repo:<owner>/<repo>+is:pr+created:>=2020-08-15


class Github:

    try:
        API_TOKEN = os.environ['GITHUB_TOKEN']
        API_HEADER = {'Authorization': API_TOKEN, 'accept': 'application/json'}
    except KeyError:
        print("ERROR: GITHUB_TOKEN env var not set")
        sys.exit()

    # UTILS
    def date_range(self, date_type, date_start, date_end):
        return 'created:>=2020-08-15'.format()
        
    # URL: ISSUES 
    def issues_url_base(self, project):
        return '{0}/search/issues?q=repo:{1}/{2}'.format(API_BASE, OWNER, project)

    def issues_url_is_issue(self, project, created_date):
        
        url_base = self.issues_url_base(project)
        url =  '{0}+created:>=2020-08-15'.format(url_base)
        pass


    def issues_url_is_pr(self, project):
        url_base = self.issues_url_base(project)
        url = '{0}+is:pr'.format(url_base)
        # return '{0}/search/issues?q=repo:<owner>/<repo>+is:pr+created:>=2020-08-15
        pass

    # URL: PULLS
    def url_pr_base(self, project):
        return  '{0}/repos/{1}/{2}/pulls?state=closed'.format(API_BASE, OWNER, project)


class GithubHelpers:

    def __init__(self):
        self.github = Github()

    def add_rows(data, row_count):
        for repository in data:
            title = repository["title"]
            merged_at = repository["merged_at"]
            user= repository["user"]["login"]
         
            if user not in EXCLUDED:
                if merged_at:
                    table.add_row([row_count, title, merged_at, user])
                    row_count += 1

        return table, row_count 

    def paginate(self):
        # github API paginates data: default == 30, max == 100
        PER_PAGE_MAX = 100

        # starting values
        count = 1
        row_count = 1
        another_page = True

        api = self.github.url_pulls_base(project)

        while another_page: 
            params = {'page': count, 'per_page':PER_PAGE_MAX}
            response = requests.get(api, params=params, headers=API_HEADER)
            print(response)
            r = response.json()
            
            # check if there is a next page
            if 'next' in response.links:
                api = response.links['next']['url']
                print(api)
                table, row_count = self.add_rows(r, row_count)
                count += 1
                another_page=True
            else:
                another_page=False
        return table

def diagnostic(project):
    gh = GithubHelpers()
    table = PrettyTable()
    table.field_names = ["count", "title", "merged_at","user"]
    table.align['count'] = "l"
    table.align['title'] = "l"
    table.align['merged_at'] = "l"
    table.align['user'] = "l"
    table = gh.paginate(project, table)
    print(table)

def main():
    date_type = 'created'
    date_start = '2021-09-01'
    date_end = '2021-10-01'
    project = 'reference-browser'

    g = Github()
    r = g.date_range(date_type, date_start, date_end)
    b = g.issues_url_base(project)
    print(b)

if __name__ == '__main__':
    main()
