import pandas as pd
from sqlalchemy import Table

from lib.database_conn import Session, Base
from utils.datetime_utils import DatetimeUtils


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


class ReportTestCaseCoverage(Base):
    __table__ = Table('report_test_case_coverage', Base.metadata, autoload=True)


class ReportTestRunCounts(Base):
    __table__ = Table('report_test_run_counts', Base.metadata, autoload=True)


class ReportGithubIssues(Base):
    __table__ = Table('report_github_issues', Base.metadata, autoload=True)


class Database:

    def __init__(self):
        self.session = Session()
