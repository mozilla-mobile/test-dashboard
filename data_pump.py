import argparse
import json
import logging
import os
import sys
from enum import Enum

#from database import Database
from testrail import TestRailHelpers


_logger = logging.getLogger('testrail')


PROJECTS_ABBREV = [
    'fenix',
    'focus-android',
    'reference-browser',
    'firefox-ios',
    'focus-ios',
]

SUB_SUITES = [
    'functional',
    'smoke',
    'security',
    'l10n',
    'accessibility',
]

STATUS = [
    'untriaged',
    'suitable',
    'unsuitable',
    'completed',
    'disabled',
]
        
COVERAGE = [
    'none', 'partial', 'full',
]


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Retrieve data for TestRail mobile projects"
    )

    parser.add_argument(
        "--project",
        help="Indicate project",
        required=True,
        choices=PROJECTS_ABBREV
    )

    parser.add_argument(
        "--sub-suite",
        help="Indicate sub test suite",
        choices=SUB_SUITES
    )

    return parser.parse_args(args=cmdln_args)


def main():
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    # GET INPUT ARGS
    args = parse_args(sys.argv[1:])
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    # QUERY TESTRAIL IDs FROM DB
    #db = Database()
    h = TestRailHelpers()
    #project_id, functional_test_suite_id = db.select_testrail_project_ids(args.project)
    h.test_case_data_raw(args.project)


    # Automatated Status = [Untriaged, Suitable, Unsuitable, Completed, Disabled]
    # Automation Coverage = [None, Partial, Full]
    # Sub Test Suites = [Functional, Smoke & Sanity, Accessibilty, L10n, Security]


    # QUERY TYPES
    # 1. counts

    # QUERY TESTRAIL FOR JSON DATA

    """
    cases  = t.test_cases(project_id, functional_test_suite_id)

    # TODO: write helper functions
    custom_automation_statuses = [1, 2, 3, 4, 5]
    custom_automation_coverages = [1, 2, 3]
    
    count_custom_automation_status = [0] * 5 
    count_custom_automation_coverage = [0] * 3 

    pp.pprint(cases[0])
    for case in cases:
        for i in custom_automation_statuses:
            if case['custom_automation_status'] == i:
                count_custom_automation_status[i - 1] += 1
        #if case['custom_automation_coverage'] == 3:
        #    count_custom_automation_coverage += 1
    print('COUNTS')
    print('custom_automation_status: {0}'.format(count_custom_automation_status))
    print('custom_automation_coverage: {0}'.format(count_custom_automation_coverage))
    print('---')
    """
    #print(cases[0]['custom_automation_coverage'])


    # CONVERT JSON DATA TO PYTHON LISTS

    # CONVERT PYTHON LISTS TO SQLALCHEMY OBJECTS

    # INSERT DATA TO DB VIA SQLALCHEMY OBJECT

    # TBD

    # TEST COVERAGE (AUTOMATION)
    # 1. Percent 
    # - untriaged > suitable
    # - untriaged > unsuitable
    # 2. Test counts

    # FREQUENCE - once a month? 
    """
    _logger.debug("Fetching project data from TestRail...")
    t = TestRail()
    p = t.get_project(args.project)

    _logger.debug("Fetching suite data from TestRail...")
    s = t.get_suite(args.suite)

    _logger.debug("Writing case automation status to JSON dump...")
    c = Cases()
    cases = t.get_cases(args.project, args.suite)

    """


if __name__ == '__main__':
    main()

