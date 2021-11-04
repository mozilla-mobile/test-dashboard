import sys

import numpy as np
import pandas as pd
from sqlalchemy import Table

from lib.database_conn import Session, Base
from utils import Utils


class Projects(Base):
    __table__ = Table('projects', Base.metadata, autoload=True)


class TestAutomationStatus(Base):
    __table__ = Table('test_automation_status', Base.metadata, autoload=True)


class TestAutomationCoverage(Base):
    __table__ = Table('test_automation_coverage', Base.metadata, autoload=True)


class TestSuites(Base):
    __table__ = Table('test_suites', Base.metadata, autoload=True)


class TestSubSuites(Base):
    __table__ = Table('test_sub_suites', Base.metadata, autoload=True)


class ReportTestCoverage(Base):
    __table__ = Table('report_test_coverage', Base.metadata, autoload=True)


class ReportTestRuns(Base):
    __table__ = Table('report_test_runs', Base.metadata, autoload=True)


class ReportGithubIssues(Base):
    __table__ = Table('report_github_issues', Base.metadata, autoload=True)


class Database:

    def __init__(self):
        self.session = Session()

    def totals_new_row(self, field_list, data_list):
        """ Given a field list, create an empty dictionary to temporarily
        store a row of data for totals array"""
        row = {}
        i = 0 
        for key in field_list:
            row.update({key: data_list[i]})
            i += 1
        return row 

    def report_test_coverage_totals(self, cases):
        """given testrail data (cases), parse for test case counts"""

        # determine range for a data array for temp storing values to insert
        sub_ids = self.test_sub_suites_option_ids()
        b = len(sub_ids) + 1
        stat_ids = self.test_automation_status_option_ids()
        s = len(stat_ids) + 1
        cov_ids = self.test_automation_coverage_option_ids()
        c = len(cov_ids) + 1

        totals = [] 

        for case in cases:
           b = case['custom_sub_test_suites']
           s = case['custom_automation_status']
           c = case['custom_automation_coverage']
           row = [] 
           for i in b:
               row = [i, s, c, 1]
               totals.append(row)
 
        """
        df1 = pd.DataFrame(totals, columns=['custom_sub_test_suites',
                                           'custom_automation_status',
                                           'custom_automation_coverage'])
        df1.groupby(['custom_automation_status', 'custom_automation_coverage']).sum()
        """
        df1 = pd.DataFrame(data=totals, columns=['sub', 'status', 'cov', 'tally']).groupby(['sub', 'status', 'cov'])['tally'].sum().reset_index()
     
        #df1.groupby(['sub'])['count'].sum().reset_index()

        print(df1)
        sys.exit(1)
        return totals

    def report_test_coverage_totals_NEW(self, cases):
        """given testrail data (cases), parse for test case counts"""

        # create a 'totals' list to store rows of data to insert in database
        totals = []

        # desired fields in 'cases' 
        keys = ['title',
                'custom_automation_status',
                'custom_automation_coverage',
                'custom_sub_test_suites']

        for case in cases:
            vals  = [case[i] for i in keys]
            print(case)
            # each testcase can have MULTIPLE custom_sub_test_suites ids
            # instead of total per test case count
            # we have to decide how to pack in extra counts for sub_test_suites
            for j in case['custom_sub_test_suites']:
                row = self.totals_new_row(keys, vals) 
                # need to fix the last custom_sub_suites_id
                print(row)
                totals.append(row)
        #print(totals)

        sys.exit(1)
        return totals

    def report_test_coverage_insert(self, project_id, totals):
        # insert data from totals into report_test_coverage table
        for i in range(1, len(totals)):
            for j in range(1, len(totals[i])):
                for k in range(1, len(totals[i][j])):
					# sqlalchemy insert statement
                    report = ReportTestCoverage(projects_id=project_id,
                                                test_automation_status_id=i,
                                                test_automation_coverage_id=j,
                                                test_sub_suites_id=k,
                                                test_count=totals[i][j])
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

    def report_github_issues_totals(self, project_id, totals):
        return totals

    def report_test_runs_insert(self, project_id, totals):
        # insert data from totals into report_test_runs table

        for total in totals:
            t = total

            # only count completed testruns
            if t['testrail_completed_on']:
                created_on = Utils.convert_epoch_to_datetime(t['testrail_created_on']) # noqa
                completed_on = Utils.convert_epoch_to_datetime(t['testrail_completed_on']) # noqa
                report = ReportTestRuns(projects_id=project_id,
                                        testrail_run_id=t['testrail_run_id'],
                                        test_case_passed_count=t['passed_count'], # noqa
                                        test_case_retest_count=t['retest_count'], # noqa
                                        test_case_failed_count=t['failed_count'], # noqa
                                        test_case_blocked_count=t['blocked_count'], # noqa
                                        testrail_created_on=created_on,
                                        testrail_completed_on=completed_on)
                self.session.add(report)
                self.session.commit()

    def report_github_issues_insert(self, project_id, totals):
        for total in totals:
            t = total

            # only count xxxxx 
            if t['xxxxx']:
                report = ReportTestRuns(projects_id=project_id,
                                        issue_id=t['issue_id'],
                                        issue_title=t['issue_title'], # noqa
                                        issue_types_id=t['issue_types_id'], #  1=issue, 2=pr
                                        github_created_at=t['github_created_at'], # noqa
                                        github_updated_at=t['github_updated_at'], # noqa
                                        github_closed_at=t['github_closed_at'], # noqa
                                        github_merged_at=t['github_merged_at']) # noqa
                self.session.add(report)
                self.session.commit()
                self.session.add(report)
                self.session.commit()


    def test_sub_suites_option_ids(self):
        # ids corresponding to options in the automation status dropdown
        response = self.session.query(TestSubSuites.testrail_id).all()
        results = []
        for row in response:
            results.append(row[0])
        return results

    def test_automation_status_option_ids(self):
        # ids corresponding to options in the automation status dropdown
        response = self.session.query(TestAutomationStatus.testrail_id).all()
        results = []
        for row in response:
            results.append(row[0])
        return results

    def test_automation_coverage_option_ids(self):
        # ids corresponding to options in the automation coverage dropdown
        response = self.session.query(TestAutomationCoverage.testrail_id).all()
        results = []
        for row in response:
            results.append(row[0])
        return results

    def testrail_identity_ids(self, project):
        """ Return the ids needed to be able to query the TestRail API for
        a specific test suite from a specific project

        projects.id = projects table id
        testrail_id = id of project in testrail
        testrail_functional_test_suite_id = Full Functional Tests Suite id

        # Note:
        # These never change, so we store them in DB for convenience """

        q = self.session.query(Projects)
        p = q.filter_by(project_name_abbrev=project).first()
        return p.id, p.testrail_id, p.testrail_functional_test_suite_id
