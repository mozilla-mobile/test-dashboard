import argparse
import sys

from testrail import TestRailDataPump
from github import GithubDataPump


PROJECTS_ABBREV = [
    'fenix',
    'focus-android',
    'reference-browser',
    'firefox-ios',
    'focus-ios',
]

REPORT_TYPES = [
    'test-cases',
    'test-run-counts',
    'issue-regression',
]


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Retrieve and update mobile project test data"
    )

    parser.add_argument(
        "--project",
        help="Indicate project",
        required=True,
        choices=PROJECTS_ABBREV
    )

    parser.add_argument(
        "--report-type",
        help="Indicate report type",
        required=True,
        choices=REPORT_TYPES
    )

    parser.add_argument(
        "--num-days",
        help="Indicate number of historic days of records to include",
        required=False
    )

    return parser.parse_args(args=cmdln_args)


def main():
    args = parse_args(sys.argv[1:])

    if args.report_type == 'test-cases':
        h = TestRailDataPump()
        h.testrail_coverage_update(args.project)
    if args.report_type == 'test-run-counts':
        h = TestRailDataPump()
        if args.num_days:
            num_days = args.num_days
        else:
            num_days = ''
        h.testrail_run_counts_update(args.project, num_days)
    if args.report_type == 'issue-regression':
        h = GithubDataPump()
        h.github_issue_regression(args.project)
        h = GithubDataPump()


if __name__ == '__main__':
    main()
