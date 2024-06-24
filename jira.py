import os
import sys

from lib.jira_conn import JiraAPIClient


# JQL query All QA Requests since 2022 filter_id: 13856
query = 'jql=filter=13856&fields=id,key,status,created,customfield_10037,customfield_10134,customfield_10155&maxResults=100'


class Jira:

    def __init__(self):
        try:
            JIRA_HOST = os.environ['JIRA_HOST']
            self.client = JiraAPIClient(JIRA_HOST)
            self.client.user = os.environ['JIRA_USER']
            self.client.password = os.environ['JIRA_PASSWORD']

        except KeyError:
            print("ERROR: Missing jira env var")
            sys.exit(1)

    # API: Filters
    def filters(self):
        return self.client.get_search(query)
