import argparse
import sys

from testrail import TestRailHelpers


PROJECTS_ABBREV = [
    'fenix',
    'focus-android',
    'reference-browser',
    'firefox-ios',
    'focus-ios',
]

DATA_SOURCES = [
    'testrail',
    'github',
]


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Retrieve and update mobile project test data"
    )

    parser.add_argument(
        "--data-type",
        help="Indicate data source",
        required=True,
        choices=DATA_SOURCES
    )

    parser.add_argument(
        "--project",
        help="Indicate project",
        required=True,
        choices=PROJECTS_ABBREV
    )
    return parser.parse_args(args=cmdln_args)


def main():
    args = parse_args(sys.argv[1:])
    print('begin data_pump')
    print('DATA_TYPE: {0}'.format(args.data_type))
    if args.data_type in 'testrail':
        h = TestRailHelpers()
        print('preparing testrail helper....')
        h.dummy()
        h.testrail_coverage_update(args.project)
    if args.data_type in 'github':
        """
        h = GithubHelpers()
        h.github_coverage_update(args.project)
        h = GithubHelpers()
        """
        pass


if __name__ == '__main__':
    main()
