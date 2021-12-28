from datetime import datetime
from enum import Enum
import os
import sys

import argparse
import logging
import requests


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def parse_args(cmdln_args):
    parser = argparse.ArgumentParser(
        description="Gets build data for a targeted app on Bitrise"
    )

    parser.add_argument(
        "--project",
        help="Use selected project",
        required=True,
        choices=['ios', 'android']
    )

    parser.add_argument(
        "--branch",
        help="Use selected branch",
        required=False,
        default=None
    )

    parser.add_argument(
        "--workflow",
        help="Use selected workflow",
        required=False,
        default=None
    )

    parser.add_argument(
        "--before",
        help="List builds run before a given date (epoch time)",
        required=False,
        default=None,
        type=datetime.fromisoformat
    )

    parser.add_argument(
        "--after",
        help="List builds run after a given date (epoch time)",
        required=False,
        default=None,
        type=datetime.fromisoformat
    )

    return parser.parse_args(args=cmdln_args)


class Status(Enum):
    NOT_FINISHED = 0
    SUCCESSFUL = 1
    FAILURE = 2
    ABORTED_FAILURE = 3
    ABORTED_SUCCESS = 4


class Bitrise:

    def __init__(self):
        try:
            self.API_TOKEN = os.environ['BITRISE_TOKEN']
            self.API_HEADER = {'Authorization': self.API_TOKEN,
                               'accept': 'application/json'}

        except KeyError:
            print("ERROR: must set BITRISE_TOKEN")
            exit()

    def get_apps(self):
        resp = requests.get('https://api.bitrise.io/v0.1/apps',
                            headers=self.API_HEADER)
        if resp.status_code != 200:
            raise print('GET /apps/ {}'.format(resp.status_code))
        return resp.json()

    def set_app(self, project, apps):
        if apps is not None:
            if project == "android":
                self.APP_SLUG = apps['data'][0]['slug']
            elif project == "ios":
                self.APP_SLUG = apps['data'][1]['slug']

    def get_app(self, project, apps):
        if not self.APP_SLUG:
            resp = requests.get('https://api.bitrise.io/v0.1/apps/{0}'.
                                format(self.APP_SLUG),
                                headers=self.API_HEADER)
            if resp.status_code != 200:
                raise _logger.error('GET /apps/ {}'.format(resp.status_code))
            return resp.json()

    def get_workflows(self, APP_SLUG):
        resp = \
            requests.get('https://api.bitrise.io/v0.1/apps/{0}'
                         '/build-workflows'.format(self.APP_SLUG),
                         headers=self.API_HEADER)
        if resp.status_code != 200:
            raise _logger.error('GET /apps/ {}'.format(resp.status_code))
        return resp.json()

    def get_builds(self, params=None):
        resp = \
            requests.get('https://api.bitrise.io/v0.1/apps/{0}'
                         '/builds'.format(self.APP_SLUG),
                         headers=self.API_HEADER, params=params)
        if resp.status_code != 200:
            raise _logger.error('GET /apps/ {}'.format(resp.status_code))
        return resp.json()


def main():
    args = parse_args(sys.argv[1:])

    b = Bitrise()

    all_apps = b.get_apps()

    b.set_app(args.project, all_apps)
    workflows = b.get_workflows(b.APP_SLUG)
    builds = b.get_builds({"branch": args.branch,
                           "workflow": args.workflow,
                           "after": int(datetime.timestamp(args.after))
                           if args.after is not None else None,
                           "before": int(datetime.timestamp(args.before))
                           if args.before is not None else None})

    failures = b.get_failure_count(builds)
    print("All recent builds Failure count: {0}".format(failures))

    successes = b.get_success_count(builds)
    print("All recent builds Success count: {0}".format(successes))

    not_finished = b.get_not_finished_count(builds)
    print("All recent builds Not finished count: {0}".format(not_finished))

    aborted_failure = b.get_aborted_failure(builds)
    print("All recent builds Aborted Failure count: {0}"
          .format(aborted_failure))

    aborted_success = b.get_aborted_success(builds)
    print("All recent builds Aborted Success count: {0}"
          .format(aborted_success))

    print(*workflows['data'], sep=", ")


if __name__ == '__main__':
    main()
