import os
import sys

import pandas as pd

from lib.jira_conn import JiraAPIClient
from database import (
    Database,
    ReportJiraQARequests
)
from utils.datetime_utils import DatetimeUtils as dt
from utils.constants import FILTER_ID_ALL_REQUESTS_2022, MAX_RESULT


# JQL query All QA Requests since 2022 filter_id: 13856
# Extra fields needed
STORY_POINTS = "customfield_10037"
FIREFOX_RELEASE_TRAIN = "customfield_10155"
ENGINEERING_TEAM = "customfield_10134"
DEFAULT_COLUMNS = "id,key,status,created,summary,labels,assignee,"

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
                + DEFAULT_COLUMNS + ',' + STORY_POINTS + ',' \
                + FIREFOX_RELEASE_TRAIN + ',' \
                + ENGINEERING_TEAM + '&' + MAX_RESULT

        return self.client.get_search(query)


class JiraClient(Jira):
    def __init__(self):
        super().__init__()
        self.db = DatabaseJira()

    def jira_qa_requests(self):
        payload = self.filters()
        print("This is the payload returning from filter")
        print(payload)
        '''
        Working Test Payload
        payload = [{
            "key": "QA-2555",
            "fields": {
                "summary": "[QA for] password generator Android",
                "created": "2024-07-01T19:00:26.017-0400",
                "assignee": "None",
                "customfield_10155": {
                    "value": "Fx129"
                },
                "customfield_10134": {
                    "value": "Mobile Android"
                },
                "customfield_10037": "2",
                "status": {
                    "name": "Created"
                },
                "labels": [
                ]
            }},{
            "key": "QA-2555",
            "fields": {
                "summary": "[QA for] password generator Android",
                "created": "2024-08-01T19:00:26.017-0400",
                "assignee": {
                    "self": "https://mozilla-hub.atlassian.net/rest/api/2/user?accountId=712020%3A94a51a44-b5cc-4200-b015-b3344f6829a7", # noqa
                    "accountId": "712020:94a51a44-b5cc-4200-b015-b3344f6829a7",
                    "emailAddress": "dbarladeanu@mozilla.com",
                    "avatarUrls": {
                        "48x48": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/712020:94a51a44-b5cc-4200-b015-b3344f6829a7/744bb20e-d66a-475a-839a-765800c8cfda/48", # noqa
                        "24x24": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/712020:94a51a44-b5cc-4200-b015-b3344f6829a7/744bb20e-d66a-475a-839a-765800c8cfda/24", # noqa
                        "16x16": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/712020:94a51a44-b5cc-4200-b015-b3344f6829a7/744bb20e-d66a-475a-839a-765800c8cfda/16", # noqa
                        "32x32": "https://avatar-management--avatars.us-west-2.prod.public.atl-paas.net/712020:94a51a44-b5cc-4200-b015-b3344f6829a7/744bb20e-d66a-475a-839a-765800c8cfda/32"  # noqa
                    },
                    "displayName": "Diana Andreea Barladeanu",
                    "active": True,
                    "timeZone": "America/Indiana/Indianapolis",
                    "accountType": "atlassian"
                },
                "customfield_10155": {
                    "value": "Fx129"
                },
                "customfield_10134": {
                    "value": "Mobile Android"
                },
                "customfield_10037": None,
                "status": {
                    "name": "CI/Execution"
                },
                "labels": [
                    ]
                }
                }
        ]
        '''
        self.db.qa_requests_delete()

        data_frame = self.db.report_jira_qa_requests_payload(payload)
        print(data_frame)

        self.db.report_jira_qa_requests_insert(data_frame)


class DatabaseJira(Database):

    def __init__(self):
        super().__init__()
        self.db = Database()

    def qa_requests_delete(self):
        """ Wipe out all test suite data.
        NOTE: we'll renew this data from Testrail every session."""
        self.session.query(ReportJiraQARequests).delete()
        self.session.commit()

    def report_jira_qa_requests_payload(self, payload):
        # Normalize the JSON data
        df = pd.json_normalize(payload, sep='_')

        # Check if 'jira_assignee_username' exists
        # if not use 'alternative_assignee_emailAddress'
        if 'fields_assignee_emailAddress' not in df.columns:
            df['fields_assignee_emailAddress'] = df.get('fields_assignee', "None") # noqa
        else:
            df['fields_assignee_emailAddress'] = df['fields_assignee_emailAddress'].fillna("Not Assigned") # noqa

        # Drop the alternative column if it exists
        if 'fields_assignee' in df.columns:
            df.drop(columns=['fields_assignee'], inplace=True)

        # Select specific columns
        selected_columns = {
            'key': 'jira_key',
            'fields_summary': 'jira_summary',
            'fields_created': 'jira_created_at',
            'fields_customfield_10155_value': 'jira_firefox_release_train',
            'fields_customfield_10134_value': 'jira_engineering_team',
            'fields_customfield_10037': 'jira_story_points',
            'fields_status_name': 'jira_status',
            'fields_assignee_emailAddress': 'jira_assignee_username',
            'fields_labels': 'jira_labels'
        }

        # Select specific columns
        df_selected = df[selected_columns.keys()]

        # Rename columns
        df_selected = df_selected.rename(columns=selected_columns)

        df_selected['jira_created_at'] = df_selected['jira_created_at'].apply(dt.convert_to_utc) # noqa

        # Join list of labels into a single string
        df_selected['jira_labels'] = df_selected['jira_labels'].apply(lambda x: ','.join(x) if isinstance(x, list) else x) # noqa

        return df_selected

    def report_jira_qa_requests_insert(self, payload):
        print(payload)

        for index, row in payload.iterrows():
            print(row)
            report = ReportJiraQARequests(jira_key=row['jira_key'],
                                          jira_created_at=row['jira_created_at'].date(), # noqa
                                          jira_summary=row['jira_summary'], # noqa
                                          jira_firefox_release_train=row['jira_firefox_release_train'], # noqa
                                          jira_engineering_team=row['jira_engineering_team'], # noqa
                                          jira_story_points=row['jira_story_points'], # noqa
                                          jira_status=row['jira_status'], # noqa
                                          jira_assignee_username=row['jira_assignee_username'], # noqa
                                          jira_labels=row['jira_labels'])

        # This is the only way working locally to insert data
        # payload.to_sql('report_jira_qa_requests', con=engine, if_exists='append', index=False) # noqa
        self.session.add(report)
        self.session.commit()
