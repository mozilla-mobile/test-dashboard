import argparse
import sys

from github import GithubClient
from jira import JiraClient
from testrail import TestRailClient
from utils.constants import PROJECTS_ABBREV, REPORT_TYPES


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Retrieve and update mobile project test data"
    )

    parser.add_argument(
        "--project",
        help="Indicate project",
        required=False,
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
    if args.report_type == 'test-case-coverage':
        h = TestRailClient()
        h.data_pump(args.project.lower())

    if args.report_type == 'test-run-counts':
        h = TestRailClient()
        if args.num_days:
            num_days = args.num_days
        else:
            num_days = ''
        h.testrail_run_counts_update(args.project, num_days)
    if args.report_type == 'issue-regression':
        h = GithubClient()
        h.github_issue_regression(args.project)
        h = GithubClient()
    if args.report_type == 'jira-qa-requests':
        h = JiraClient()
        h.jira_qa_requests()
    if args.report_type == 'jira-qa-needed':
        h = JiraClient()
        h.jira_qa_needed()


if __name__ == '__main__':
    main()
