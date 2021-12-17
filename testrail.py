import os
import sys

import pandas as pd

from lib.testrail_conn import APIClient
from database import (
    Database,
    Projects,
    ReportTestCaseCoverage,
    ReportTestRunCounts
)

from utils.datetime_utils import DatetimeUtils as dt


class TestRail:

    def __init__(self):
        try:
            TESTRAIL_HOST = os.environ['TESTRAIL_HOST']
            self.client = APIClient(TESTRAIL_HOST)
            self.client.user = os.environ['TESTRAIL_USERNAME']
            self.client.password = os.environ['TESTRAIL_PASSWORD']
        except KeyError:
            print("ERROR: Missing testrail env var")
            sys.exit(1)

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
    def test_runs(self, project_id, start_date='', end_date=''):
        date_range = ''
        if start_date:
            after = dt.convert_datetime_to_epoch(start_date)
            date_range += '&created_after={0}'.format(after)
        if end_date:
            before = dt.convert_datetime_to_epoch(end_date)
            date_range += '&created_before={0}'.format(before)
        return self.client.send_get('get_runs/{0}{1}'.format(project_id, date_range)) # noqa

    def test_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))


class TestRailClient(TestRail):

    def __init__(self):
        super().__init__()
        self.db = DatabaseTestRail()

    def data_pump(self, project='all', suite='all'):
        # call database for 'all' values
        # convert inputs to a list so we can easily
        # loop thru them
        ids_list = self.testrail_project_ids(project)
        print(f'IDS_LIST: {ids_list}')
        for ids in ids_list:         
            suite_ids = self.testrail_suite_ids(testrail_project_id=ids[1])
            for suite_id in suite_ids:
                print(f"ID: {ids[1]}")
                print(f"SUITE_ID: {suite_id}")
                print('--------')
                self.testrail_coverage_update(ids[0], ids[1], suite_id)
                # testrail_coverage_update(self, projects_id, testrail_project_id, test_suite_id):

        """
        for project in projects:
            for suite in suites:
                self.testrail_coverage_update(project, suite)
       """

    def testrail_suite_ids(self, testrail_project_id):
        suite_ids = []
        suites = self.test_suites(testrail_project_id) # testrail_project_id
        for suite in suites:
            suite_ids.append(suite['id'])
        return suite_ids

    def testrail_project_ids(self, project):
        """ Return the ids needed to be able to query the TestRail API for
        a specific test suite from a specific project

        projects.id = projects table id
        testrail_id = id of project in testrail

        Note:
         - These never change, so we store them in DB for convenience
         - We'll use these to query the test suites from each respective project
        """

        q = self.db.session.query(Projects)

        if project == 'all':
            p = q.all()
        else:
            p = []
            proj = q.filter_by(project_name_abbrev=project).first()
            p.append(proj)
        ids = []
        tmp = []

        for item in p:
            if type(item.testrail_id == int):
                tmp.append(item.id)
                tmp.append(item.testrail_id)
                ids.append(tmp)
            tmp = []
        return ids

    def testrail_identity_ids_OLD(self, project):
        """ Return the ids needed to be able to query the TestRail API for
        a specific test suite from a specific project

        projects.id = projects table id
        testrail_id = id of project in testrail
        testrail_functional_test_suite_id = Full Functional Tests Suite id

        # Note:
        # These never change, so we store them in DB for convenience """

        #q = self.session.query(Projects)
        q = self.db.session.query(Projects)
        p = q.filter_by(project_name_abbrev=project).first()
        return p.id, p.testrail_id, p.testrail_functional_test_suite_id

    def testrail_coverage_update(self, projects_id, testrail_project_id, test_suite_id):

        # Pull JSON blob from Testrail
        cases = self.test_cases(testrail_project_id, test_suite_id)

        # Format and store data in a 'totals' array
        totals = self.db.report_test_coverage_totals(cases)
        print(totals)

        # Insert data in 'totals' array into DB
        self.db.report_test_coverage_insert(projects_id, totals)


    def testrail_run_counts_update(self, project, num_days):
        start_date = dt.start_date(num_days)

        # Get reference IDs from DB
        projects_id, testrail_project_id, functional_test_suite_id = self.db.testrail_identity_ids(project) # noqa 

        # Sample Testrail data from one run:
        # [{'run_id': 44113}, {'project_id': 59}, {'suite_id': 3192},
        # {'name': 'Smoke and sanity automated tests - Beta 90.0.0-beta.2'},
        # {'created_on': 1623151551}, {'completed_on': 1623158050},
        # {'failed_count': 0}, {'passed_count': 35}, {'retest_count': 0},
        # {'blocked_count': 0}, {'untested_count': 0}, {'untested_count': 0}]

        # Pull JSON blob from Testrail
        #runs = self.testrail.test_runs(testrail_project_id, start_date) # noqa
        runs = self.test_runs(testrail_project_id, start_date) # noqa

        # Format and store data in a 'totals' array
        totals = self.db.report_test_run_totals(runs)

        # Insert data in 'totals' array into DB
        self.db.report_test_runs_insert(projects_id, totals)


class DatabaseTestRail(Database):

    def __init__(self):
        super().__init__()
        self.db = Database()

    def report_test_coverage_totals(self, cases):
        """given testrail data (cases), calculate test case counts by type"""

        totals = []

        for case in cases:
            row = []
            """
            # TODO: remove conditional once Focus-iOS data has been fixed
            if not case['custom_sub_test_suites']:
                 print('NOT FOUND: ', case['id'])
                 subs = 1
            """
            suit = case['suite_id']
            subs = case['custom_sub_test_suites']
            print('suite_id: {0}, case_id: {1}, subs: {2}'.format(suit, case['id'], subs))
            stat = case['custom_automation_status']
            cov = case['custom_automation_coverage']

            # iterate through multi-select sub_suite data
            # we need to create a separate row for each
            # test case that belongs to multiple sub suites
            for sub in subs:
                row = [suit, sub, stat, cov, 1]
                totals.append(row)

        df = pd.DataFrame(data=totals,
                          columns=['suit', 'sub', 'status', 'cov', 'tally'])
        return df.groupby(['suit', 'sub', 'status', 'cov'])['tally'].sum().reset_index() # noqa

    def report_test_coverage_insert(self, project_id, totals):
        # TODO:  Error on insert
        # insert data from totals into report_test_coverage table
        for index, row in totals.iterrows():
            print('ROW - suit: {0}, asid: {1}, acid: {2}, ssid: {3}, tally: {4}'.format(row['suit'], row['status'], row['cov'], row['sub'], row['tally'])) 
     
            report = ReportTestCaseCoverage(projects_id=project_id,
                                            testrail_suites_id=row['suit'], # noqa
                                            test_automation_status_id=row['status'], # noqa
                                            test_automation_coverage_id=row['cov'],
                                            test_sub_suites_id=row['sub'],
                                            test_count=row['tally'])
            self.session.add(report)
            self.session.commit()

    def report_test_run_totals(self, runs):
        """pack testrail data for 1 run in a data array

        NOTE:
        run_name

        Because storing data for 1 run will occupy multipe db rows,
        Storing the run name would require inserting into a reference
        table.  For now, we will just store the testrail run id.

        project_id, suite_id

        We will pass along the proj_name_abbrev to the db.
        For suite_id, we will always default to Full Functional.
        """
        # create array to store values to insert in database
        totals = []

        for run in runs:
            tmp = {}

            # identifiers
            # tmp.append({'name': run['name']})
            tmp.update({'testrail_run_id': run['id']})

            # epoch dates
            tmp.update({'testrail_created_on': run['created_on']})
            tmp.update({'testrail_completed_on': run['completed_on']})

            # test data
            tmp.update({'passed_count': run['passed_count']})
            tmp.update({'retest_count': run['retest_count']})
            tmp.update({'failed_count': run['failed_count']})
            tmp.update({'blocked_count': run['blocked_count']})
            totals.append(tmp)
        return totals

    def report_test_runs_insert(self, project_id, totals):
        # insert data from totals into report_test_run_counts table

        for total in totals:
            t = total

            # only count completed testruns
            if t['testrail_completed_on']:
                created_on = dt.convert_epoch_to_datetime(t['testrail_created_on']) # noqa
                completed_on = dt.convert_epoch_to_datetime(t['testrail_completed_on']) # noqa
                report = ReportTestRunCounts(projects_id=project_id,
                                        testrail_run_id=t['testrail_run_id'],
                                        test_case_passed_count=t['passed_count'], # noqa
                                        test_case_retest_count=t['retest_count'], # noqa
                                        test_case_failed_count=t['failed_count'], # noqa
                                        test_case_blocked_count=t['blocked_count'], # noqa
                                        testrail_created_on=created_on,
                                        testrail_completed_on=completed_on)
                self.session.add(report)
                self.session.commit()

    """
    def test_automation_coverage_option_ids(self):
        # ids corresponding to options in the automation coverage dropdown
        response = self.session.query(TestAutomationCoverage.testrail_id).all()
        results = []
        for row in response:
            results.append(row[0])
        return results
    """

