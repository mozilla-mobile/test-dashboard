import os
import sys

from lib.jira_conn import JiraAPIClient


# JQL query All QA Requests since 2022 filter_id: 13856
FILTER_ID_ALL_REQUESTS_2022 = "13856"
# Fields needed
STORY_POINTS = "customfield_10037"
FIREFOX_RELEASE_TRAIN = "customfield_10155"
ENGINEERING_TEAM = "customfield_10134"
DEFAULT_COLUMNS = "id,key,status,created,"
MAX_RESULT = "maxResults=100"

JQL_QUERY = 'jql=filter='


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
        query = JQL_QUERY + FILTER_ID_ALL_REQUESTS_2022 + '&fields=' \
                + DEFAULT_COLUMNS + STORY_POINTS + FIREFOX_RELEASE_TRAIN \
                + ENGINEERING_TEAM + '&' + MAX_RESULT
        return self.client.get_search(query)
