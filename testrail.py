import logging
import os
import sys

from lib.testrail_conn import APIClient
from database import Database


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
            after = self.convert_datetime_to_epoch(start_date)
            date_range += '&created_after={0}'.format(after)
        if end_date:
            before = self.convert_datetime_to_epoch(end_date)
            date_range += '&created_before={0}'.format(before)
        #return self.client.send_get('get_runs/{0}'.format(project_id))
        return self.client.send_get('get_runs/{0}{1}'.format(project_id, date_range))

    def test_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))

    # UTILITIES
    def convert_datetime_to_epoch(self, str_date):
        from datetime import datetime

        p = '%Y-%m-%dT%H:%M:%S.%fZ'
        mytime = "{0}T00:00:01.000Z".format(str_date)
        epoch = datetime(1970, 1, 1)
        tmp = (datetime.strptime(mytime, p) - epoch).total_seconds()
        return int(round(tmp))


class TestRailHelpers():

    def __init__(self):
        self.testrail = TestRail()
        self.db = Database()

    def date_range_days(num_days):
        # TODO given a range, return a tuple with start_date, end_date for 
        # last 24 hours, last 7 days, etc
        # will need a more intelligent method to restore historic data
        # since the data will be on a given datetime stamp we cloud "group" weekly data and 
        # insert it with a simulated historic created_at date
        pass

    def testrail_coverage_update(self, project):
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 
        cases = self.testrail.test_cases(testrail_project_id,
                                         functional_test_suite_id)
        totals = self.db.report_test_coverage_totals(cases)
        self.db.report_test_coverage_insert(projects_id, totals)

    def testrail_run_update(self, project, start_date, end_date):
        # Sample Testrail data from one run:
        # [{'run_id': 44113}, {'project_id': 59}, {'suite_id': 3192}, {'name': 'Smoke and sanity automated tests - Beta 90.0.0-beta.2'}, {'created_on': 1623151551}, {'completed_on': 1623158050}, {'failed_count': 0}, {'passed_count': 35}, {'retest_count': 0}, {'blocked_count': 0}, {'untested_count': 0}, {'untested_count': 0}] # noqa
        totals = []
        results = []
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 
        #runs = self.testrail.test_runs(testrail_project_id)
        runs = self.testrail.test_runs(testrail_project_id, start_date, end_date)
        result_count = 0
        for run in runs:
            total = self.db.report_test_run_total(run)
            run_id = total[0]['testrail_run_id']
            print(run_id)
            """
            results = self.testrail.test_results_for_run(run_id)
            for result in results:
                result_count += 1
            # need to add but total a
            totals.append(results)
            """

        # DIAGNOSTIC
        """
        totals_count = len(totals)
        print('TOTALS_COUNT: {0}'.format(totals_count))
        testcase_count = len(results)
        print('RESULT_COUNT: {0}'.format(result_count))
        sys.exit()
        """
        self.db.report_test_runs_insert(projects_id, totals)
