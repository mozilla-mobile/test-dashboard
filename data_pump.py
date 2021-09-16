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
    h = TestRailHelpers()
    h.test_case_data_raw(args.project)

    # Automatated Status = [Untriaged, Suitable, Unsuitable, Completed, Disabled]
    # Automation Coverage = [None, Partial, Full]
    # Sub Test Suites = [Functional, Smoke & Sanity, Accessibilty, L10n, Security]

    # QUERY TESTRAIL FOR JSON DATA

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

    # FREQUENCY - weekly
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

