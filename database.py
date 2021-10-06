from lib.database_conn import Session, Base

from sqlalchemy import Table

# TODO remove this
import pprint
pp = pprint.PrettyPrinter(width=41, compact=True)

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


class Database(object):

    def __init__(self):
        self.session = Session()

    def print_table(self, table_name):
        _table = Table(table_name, Base.metadata, autoload=True)
        s = [c.name for c in _table.columns]
        for row in s:
            print(row)

    def report_test_coverage_totals(self, cases):
        """given testrail data (cases), parse for test case counts"""

        # determine range for a data array for temp storing values to insert
        stat_ids = self.test_automation_status_option_ids()
        stat_ids = len(stat_ids) + 1
        cov_ids = self.test_automation_coverage_option_ids()
        cov_ids = len(cov_ids) + 1

        # create array to store values to insert in database
        totals = [[0]*(cov_ids) for _ in range(stat_ids)]
        count = 0
        for case in cases:
            t = case['title']
            s = case['custom_automation_status']
            c = case['custom_automation_coverage']

            if c is None:
                # ============================================
                # DIAGNOSTIC
                # ============================================
                # Testrail data needs housekeeping
                # print will list out cases missing Coverage
                print('{0}. {1}'.format(count, t))
                c = 1
                count += 1
            totals[s][c] += 1
        return totals

    def report_test_run_total(self, run):
        """pack testrail data for 1 run in a data array """

        # create array to store values to insert in database
        tmp = []
        # identifiers
        print('RUN_ID: {0}'.format(run['id']))
        tmp.append({'run_id': run['id']})
        tmp.append({'project_id': run['project_id']})
        tmp.append({'suite_id': run['suite_id']})
        tmp.append({'name': run['name']})
        # epoch dates
        tmp.append({'created_on': run['created_on']})
        tmp.append({'completed_on': run['completed_on']})
        # test data
        tmp.append({'failed_count': run['failed_count']})
        tmp.append({'passed_count': run['passed_count']})
        tmp.append({'retest_count': run['retest_count']})
        tmp.append({'blocked_count': run['blocked_count']})
        tmp.append({'untested_count': run['untested_count']})
        # missing abbrev value for "Not Available" 
        tmp.append({'untested_count': run['untested_count']})
        return tmp

    def report_test_coverage_insert(self, project_id, totals):
        # insert data from totals[][] into report_test_coverage table
        for i in range(1, len(totals)):
            for j in range(1, len(totals[i])):
                # sqlalchemy insert statement
                report = ReportTestCoverage(projects_id=project_id,
                                            test_automation_status_id=i,
                                            test_automation_coverage_id=j,
                                            test_count=totals[i][j])
                self.session.add(report)
                self.session.commit()

    def report_test_runs_insert(self, project_id, totals):
        """
        # insert data from totals[][] into report_test_runs table
        for i in range(1, len(totals)):
            for j in range(1, len(totals[i])):
                # sqlalchemy insert statement
                report = ReportTestCoverage(projects_id=project_id,
                                            test_automation_status_id=i,
                                            test_automation_coverage_id=j,
                                            test_count=totals[i][j])
                self.session.add(report)
                self.session.commit()
        """
        for total in totals:
            print(total)
        pass

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
        # Return the ids needed to be able to query the TestRail API for
        # a specific test suite from a specific project
        # projects.id = projects table id
        # testrail_id = id of project in testrail
        # testrail_functional_test_suite_id = Full Functional Tests Suite id
        # Note:
        #  As these will never change, we store them in db for convenience
        q = self.session.query(Projects)
        p = q.filter_by(project_name_abbrev=project).first()
        return p.id, p.testrail_id, p.testrail_functional_test_suite_id