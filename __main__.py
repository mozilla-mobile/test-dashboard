import argparse
import sys

from github import GithubClient
from jira import JiraClient
from testrail import TestRailClient
from utils.constants import PROJECTS_MOBILE, PROJECTS_ECOSYSTEM, PLATFORM, REPORT_TYPES # noqa


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Retrieve and update mobile project test data"
    )

    parser.add_argument(
        "--project",
        help="Indicate project",
        required=False,
    )

    parser.add_argument(
        "--platform",
        help="Select the platform Mobile or Ecosystem",
        required=False,
        choices=PLATFORM,
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


# Function to validate the project based on the platform
def validate_project(platform, project, report_type):
    # Conditionally require --platform and --project
    # if --report-type is 'test-case-coverage'
    if report_type == 'test-case-coverage':
        if not project:
            print("--project is required for the report selected")
        if not platform:
            print("--platform is required for the report selected")

    if platform == 'mobile' and project not in PROJECTS_MOBILE:
        print(f"Error: Invalid project '{project}' for mobile. Valid options are {PROJECTS_MOBILE}") # noqa 
        sys.exit(1)
    elif platform == 'ecosystem' and project not in PROJECTS_ECOSYSTEM:
        print(f"Error: Invalid project '{project}' for ecosystem. Valid options are {PROJECTS_ECOSYSTEM}") # noqa
        sys.exit(1)


def main():
    args = parse_args(sys.argv[1:])
    validate_project(args.platform, args.project, args.report_type)

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
