import argparse
import json
import logging
import os
import sys
from enum import Enum

from testrail_conn import APIClient
from database import Database


_logger = logging.getLogger('testrail')


SUITES = [
    {'functional': 'Full Functional Tests Suite'}
]

SUB_SUITES = [
    {'functional': 'Full Functional Tests Suite'},
    {'smoke': 'Smoke & Sanity'},
    {'l10n': 'L10n'},
    {'security': 'Security'},
    {'accessibility': 'Accessibility'}
]

PROJECTS = [
    {'fenix': 'Fenix Browser'},
    {'focus-android': 'Focus for Android'},
    {'reference-browser': 'Reference Browser'},
    {'firefox-ios': 'Firefox for iOS'},
    {'focus-ios': 'Focus for iOS'}
]


class Status(Enum):
    UNTRIAGED = 1
    SUITABLE = 2
    UNSUITABLE = 3
    COMPLETED = 4
    DISABLED = 5


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
        self.testrail = TestRail() 
        self.db = Database()


    def testrail_full_name(self, abbrev_name, full_names):
        for item in full_names:
            for key,val in item.items():
                if key == abbrev_name:
                    return val
        err = 'ERROR: project: "{0}" not found'.format(abbrev_name)
        sys.exit(err)


    def test_case_data_raw(self, project):
        import pprint

        pp = pprint.PrettyPrinter(indent=4)
        project_id, functional_test_suite_id = self.db.testrail_identity_ids(project)  
        cases  = self.testrail.test_cases(project_id, functional_test_suite_id)  
        self.db.insert_report(cases)
        #pp.pprint(cases[0])


    def json_to_sql(self, data):
        return "INSERT INTO testrail_test_coverage (project_name, suite, " \
            "automation_state, case_count) VALUES " \
            "('{}', '{}', '{}', '{}')".format(
                data['project_name'],
                data['suite'],
                data['automation_state'],
                data['case_count']
            )


    # note: could also store these in the DB as unlikely to change 
    def project_ids(self, projects=mobile_projects):
        p = self.testrail.projects()
        results = [item for item in p if any(k in item['name'] for k in projects)]

        project_arr = []
        tmp = []
        for result in results:
            tmp.append(result['name'])
            tmp.append(result['id'])
            project_arr.append(tmp)
            tmp = []
            
        return project_arr 


    # give a project name (as stored in Testrail) and return testrail project_id
    def project_id(self, project_name):
        return self.project_ids([project_name])[0][1]
            

def main():
    import json
    import pprint

    pp = pprint.PrettyPrinter(indent=4)

    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    _logger.debug("Fetching project data from TestRail...")
    t = TestRail()
    h = Helpers(t)

    # test suite ids
    
    #s = t.test_suites('Full Functional Tests Suite')
    s = t.test_case_fields()
    #s = t.test_suites(27)
    pp.pprint(s)

    """
    p = h.testrail_full_name('fenix', PROJECTS)
    print(p)
    p = h.testrail_full_name('fenix', PROJECTS)
    print(p)

    # project ids
    pids = h.project_ids(('Fenix Browser', 'Reference Browser', 'Firefox for iOS', 'Focus for Android', 'Focus for iOS'))
    pp.pprint(pids)

    # project id
    project_id = h.project_id(p)
    pp.pprint(project_id)

    # project id
    project_id = h.project_id('Focus for Android')
    pp.pprint(project_id)


    # get_project
    p = t.project(project_id)
    pp.pprint(p)

    _logger.debug("Fetching suite data from TestRail...")
    s = t.test_suite(args.suite)

   """

if __name__ == '__main__':
    main()

         
