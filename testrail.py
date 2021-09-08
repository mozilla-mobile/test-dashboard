import argparse
import json
import logging
import os
import sys
from enum import Enum

from testrail_conn import APIClient


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
        self.set_config()

    def set_config(self):
        try:
            TESTRAIL_HOST = os.environ['TESTRAIL_HOST']
            self.client = APIClient(TESTRAIL_HOST)
            self.client.user = os.environ['TESTRAIL_USERNAME']
            self.client.password = os.environ['TESTRAIL_PASSWORD']
        except KeyError:
            _logger.debug("ERROR: Missing testrail env var")
            exit()

    # API: Projects
    def get_projects(self):
        return self.client.send_get('get_projects')


    def get_project(self, project_id):
        return self.client.send_get('get_project/{0}'.format(project_id))


    # API: Cases
    def get_cases(self, project_id, suite_id):
        return self.client.send_get(
            'get_cases/{0}&suite_id={1}'.format(project_id, suite_id))


    def get_case(self, case_id):
        return self.client.send_get(
            'get_case/{0}'.format(case_id))


    # API: Case Fields
    def get_case_fields(self):
        return self.client.send_get(
            'get_case_fields')


    # API: Suites
    def get_suites(self, project_id):
        return self.client.send_get('get_suites/{0}'.format(project_id))


    def get_suite(self, suite_id):
        return self.client.send_get('get_suite/{0}'.format(suite_id))


    # API: Runs
    def get_runs(self, project_id):
        return self.client.send_get('get_runs/{0}'.format(project_id))


    def get_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    
    def write_json(self, blob, file):
        with open(file, "w") as f:
            json.dump(blob, f, sort_keys=True, indent=4)


class Cases:
    json_data = []

    def __init__(self):
        pass


class Sections:
    def __init__(self):
        pass

    def write_section_name(self, sections, suite, stripped):
        data = []

        for s in sections:
            delete = [key for key in s if key != 'suite_id' and key != 'name']
            for key in delete:
                del s[key]
            data.append(s)

        with open('sections-from-suite-{}.json'.format(str(suite)), "w") as f:
            json.dump(data, f, sort_keys=True, indent=4)


class Helpers():
    mobile_projects = [
        'Firefox for Android',
        'Fenix Browser',
        'Focus for Android',
        'Firefox for iOS',
        'Focus for iOS',
        'Reference Browser'
    ]


    def __init__(self, testrail):
        self.testrail = testrail


    def testrail_full_name(self, abbrev_name, full_names):
        for item in full_names:
            for key,val in item.items():
                if key == abbrev_name:
                    return val
        err = 'ERROR: project: "{0}" not found'.format(abbrev_name)
        sys.exit(err)


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
        p = self.testrail.get_projects()
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
    
    #s = t.get_suites('Full Functional Tests Suite')
    s = t.get_case_fields()
    #s = t.get_suites(27)
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
    p = t.get_project(project_id)
    pp.pprint(p)

    _logger.debug("Fetching suite data from TestRail...")
    s = t.get_suite(args.suite)

    _logger.debug("Writing case automation status to JSON dump...")
    c = Cases()

   """

if __name__ == '__main__':
    main()

         
