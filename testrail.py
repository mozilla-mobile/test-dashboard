import os
import sys

from lib.testrail_conn import APIClient
from database import TestRailDatabase
from utils import Utils


class TestRail:

    def __init__(self):
        try:
            TESTRAIL_HOST = os.environ['TESTRAIL_HOST']
            self.client = APIClient(TESTRAIL_HOST)
            self.client.user = os.environ['TESTRAIL_USERNAME']
            self.client.password = os.environ['TESTRAIL_PASSWORD']
        except KeyError:
            print("ERROR: Missing testrail env var")
            sys.exit(1)

    # API: Projects
    def projects(self):
        return self.client.send_get('get_projects')

    def project(self, project_id):
        return self.client.send_get('get_project/{0}'.format(project_id))

    # API: Cases
    def test_cases(self, project_id, suite_id):
        return self.client.send_get(
            'get_cases/{0}&suite_id={1}'.format(project_id, suite_id))

    def test_case(self, case_id):
        return self.client.send_get(
            'get_case/{0}'.format(case_id))

    # API: Case Fields
    def test_case_fields(self):
        return self.client.send_get(
            'get_case_fields')

    # API: Suites
    def test_suites(self, project_id):
        return self.client.send_get('get_suites/{0}'.format(project_id))

    def test_suite(self, suite_id):
        return self.client.send_get('get_suite/{0}'.format(suite_id))

    # API: Runs
    def test_runs(self, project_id, start_date='', end_date=''):
        date_range = ''
        if start_date:
            after = Utils.convert_datetime_to_epoch(start_date)
            date_range += '&created_after={0}'.format(after)
        if end_date:
            before = Utils.convert_datetime_to_epoch(end_date)
            date_range += '&created_before={0}'.format(before)
        return self.client.send_get('get_runs/{0}{1}'.format(project_id, date_range)) # noqa

    def test_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))


class TestRailDataPump(TestRail):

    def __init__(self):
        super().__init__()
        self.db = TestRailDatabase()

    def testrail_coverage_update(self, project):

        # Get reference IDs from DB
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 

        # Pull JSON blob from Testrail
        cases = self.test_cases(testrail_project_id,
                                functional_test_suite_id)

        # Format and store data in a 'totals' array
        totals = self.db.report_test_coverage_totals(cases)

        # Insert data in 'totals' array into DB
        self.db.report_test_coverage_insert(projects_id, totals)

    def testrail_run_update(self, project, num_days):
        start_date = Utils.start_date(num_days)

        # Get reference IDs from DB
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 

        # Sample Testrail data from one run:
        # [{'run_id': 44113}, {'project_id': 59}, {'suite_id': 3192},
        # {'name': 'Smoke and sanity automated tests - Beta 90.0.0-beta.2'},
        # {'created_on': 1623151551}, {'completed_on': 1623158050},
        # {'failed_count': 0}, {'passed_count': 35}, {'retest_count': 0},
        # {'blocked_count': 0}, {'untested_count': 0}, {'untested_count': 0}]

        # Pull JSON blob from Testrail
        #runs = self.testrail.test_runs(testrail_project_id, start_date) # noqa
        runs = self.test_runs(testrail_project_id, start_date) # noqa

        # Format and store data in a 'totals' array
        totals = self.db.report_test_run_totals(runs)

        # Insert data in 'totals' array into DB
        self.db.report_test_runs_insert(projects_id, totals)
