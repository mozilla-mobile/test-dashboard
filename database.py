from database_conn import Session, Base

from sqlalchemy import Table, insert, select


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


    def insert_report(self, cases):

        # determine range for a data array for temp storing values to insert
        stat_ids = self.test_automation_status_option_ids()
        stat_ids = len(stat_ids) + 1
        cov_ids = self.test_automation_coverage_option_ids()
        cov_ids = len(cov_ids) + 1

        # array to store values to insert in database
        totals = [ [0]*(cov_ids) for _ in range(stat_ids)] 
        for case in cases:
            s = case['custom_automation_status']
            c = case['custom_automation_coverage']
            if s is None:
                s = 0
            if c is None:
                c = 0
            totals[s][c] += 1

        #count = 0
        for i in range(1, len(totals)):
            for j in range(1, len(totals[i])):
                #print('TOTALS[{0}][{1}]: {2}'.format(i, j, totals[i][j]))
                #count += totals[i][j] 
                report = ReportTestCoverage(projects_id=1, test_automation_status_id=i, test_automation_coverage_id=j, test_count=totals[i][j])
                self.session.add(report)
                self.session.commit()

 
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
        # Return the 2 ids needed to be able to query the TestRail API for
        # a specific test suite from a specific project 
        # Note: 
        #  these are stored in the database for convenience and will 
        #  never change
        p = self.session.query(Projects).filter_by(project_name_abbrev=project).first()  
        return p.testrail_id, p.testrail_functional_test_suite_id

        """
        q = self.session.query(Projects).all()    
        for project in q:
            p = self.session.query(Projects).filter_by(project_name_abbrev='fenix').first()  
            print(p.testrail_functional_test_suite_id)
        """

    def select_project(self, project):
        #p = Projects()
        #p.column = 'project_name_abbrev'
        result = self.session.query(_table).filter(p.column==project).all()
        #result = self.session.query(_table).count()

        for row in result:
            print(row)
            
        return result


    def main(self):
        table_name = 'songs'
        row_data = {'title': 'Ramones', 'artist': 'The Ramones', 'genre': 'punk'} # noqa
        self.insert_row(table_name, row_data)


if __name__ == '__main__':
    c = Database()
    c.main()
