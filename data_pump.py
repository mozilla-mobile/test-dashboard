import argparse
import json
import logging
import os
import sys
from enum import Enum

from database import Database
from testrail_conn import APIClient


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
        required=True,
        choices=SUB_SUITES
    )

    parser.add_argument(
        "--status",
        help="Indicate test case automation status",
        required=True,
        choices=STATUS
    )

    parser.add_argument(
        "--coverage",
        help="Indicate test case automation coverage",
        required=True,
        choices=COVERAGE
    )

    return parser.parse_args(args=cmdln_args)


def main():
    args = parse_args(sys.argv[1:])
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    db = Database()
    db.print_table('projects')
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

