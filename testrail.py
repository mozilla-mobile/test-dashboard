import logging
import os
import sys

from lib.testrail_conn import APIClient
from database import Database


_logger = logging.getLogger('testrail')


class TestRail:

    def __init__(self):
        print('TESTRAIL init')
        #self.config()

        #def config(self):
        try:
            XXX = os.environ['XXX']
            print('XXXX')
        except:
            exit()


        try:
            TESTRAIL_HOST = os.environ['TESTRAIL_HOST']
            self.client = APIClient(TESTRAIL_HOST)
            self.client.user = os.environ['TESTRAIL_USERNAME']
            self.client.password = os.environ['TESTRAIL_PASSWORD']
            print('TESTRAIL config')
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


class TestRailHelpers():
    mobile_projects = [
        'Firefox for Android',
        'Fenix Browser',
        'Focus for Android',
        'Firefox for iOS',
        'Focus for iOS',
        'Reference Browser'
    ]

    def __init__(self):
        print('TESTRAILHELPERS init')
        print('call TestRail')
        self.testrail = TestRail()
        print('call DB')
        self.db = Database()

    def testrail_full_name(self, abbrev_name, full_names):
        for item in full_names:
            for key, val in item.items():
                if key == abbrev_name:
                    return val
        err = 'ERROR: project: "{0}" not found'.format(abbrev_name)
        sys.exit(err)

    def testrail_coverage_update(self, project):
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 
        cases = self.testrail.test_cases(testrail_project_id,
                                         functional_test_suite_id)
        totals = self.db.report_test_coverage_totals(cases)
        print(totals)
        self.db.report_test_coverage_insert(projects_id, totals)

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

    def dummy(self):
        print('PRINT THIS')
        print('PRINT THIS')
        print('PRINT THIS')
        print('PRINT THIS')


def main():
    """
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    _logger.debug("Fetching project data from TestRail...")
    t = TestRail()
    h = TestRailHelpers(t)

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    """

    # TEST FUNCTIONS HERE


if __name__ == '__main__':
    main()
