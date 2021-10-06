import logging
import os
import sys

from lib.testrail_conn import APIClient
from database import Database


_logger = logging.getLogger('testrail')


class TestRail:

    def __init__(self):
        self.config()

    def config(self):
        try:
            TESTRAIL_HOST = os.environ['TESTRAIL_HOST']
            self.client = APIClient(TESTRAIL_HOST)
            self.client.user = os.environ['TESTRAIL_USERNAME']
            self.client.password = os.environ['TESTRAIL_PASSWORD']
        except KeyError:
            _logger.debug("ERROR: Missing testrail env var")
            exit()

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
    def test_runs(self, project_id):
        return self.client.send_get('get_runs/{0}'.format(project_id))

    def test_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))

class TestRailHelpers():
    """
    mobile_projects = [
        'Firefox for Android',
        'Fenix Browser',
        'Focus for Android',
        'Firefox for iOS',
        'Focus for iOS',
        'Reference Browser'
    ]
    """

    def __init__(self):
        self.testrail = TestRail()
        self.db = Database()

    def testrail_coverage_update(self, project):
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 
        print('PROJECTS_ID: {0}'.format(projects_id)
        cases = self.testrail.test_cases(testrail_project_id,
                                         functional_test_suite_id)
        totals = self.db.report_test_coverage_totals(cases)
        print(totals)
        self.db.report_test_coverage_insert(projects_id, totals)

    def testrail_run_update(self, project):
        totals = []
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 
        runs = self.testrail.test_runs(testrail_project_id)
        for run in runs:
            total = self.db.report_test_run_total(run)
            print('=====================================')
            print(total)
            print('=====================================')
            run_id = total[0]['run_id']
            # [{'run_id': 44113}, {'project_id': 59}, {'suite_id': 3192}, {'name': 'Smoke and sanity automated tests - Beta 90.0.0-beta.2'}, {'created_on': 1623151551}, {'completed_on': 1623158050}, {'failed_count': 0}, {'passed_count': 35}, {'retest_count': 0}, {'blocked_count': 0}, {'untested_count': 0}, {'untested_count': 0}]
            results = self.testrail.test_results_for_run(run_id)
            for result in results:
                if result['status_id'] in [6]:
                    #print('RESULT: {0}'.format(result))
                    print('RESULT_ID: {0}'.format(result['id']))
                    print('STATUS_ID: {0}'.format(result['status_id']))
                    print('TEST_ID: {0}'.format(result['test_id']))
                    print('------------------------------')
                    #for test in tests:
            # need to add but total a
            totals.append(results)
        sys.exit()
        self.db.report_test_runs_insert(projects_id, totals)

    """
    def project_ids(self, projects=mobile_projects):
        # Note: testrail project ids are also stored in database for
        # convenience as they can't be changed
        p = self.testrail.projects()
        results = [item for item in p if any(k in item['name'] for k in projects)] # noqa

        project_arr = []
        tmp = []
        for result in results:
            tmp.append(result['name'])
            tmp.append(result['id'])
            project_arr.append(tmp)
            tmp = []

        return project_arr

    def project_id(self, project_name):
        # give a project name (as stored in Testrail) and
        # return testrail project_id
        return self.project_ids([project_name])[0][1]
    """

