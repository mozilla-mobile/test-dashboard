from database_conn import Session, Base

from sqlalchemy import Table, insert, select


class Projects(Base):
    __table__ = Table('projects', Base.metadata, autoload=True, autoload_with=Base.metadata.bind)  


class Database(object):

    def __init__(self):
        self.session = Session()


    def print_table(self, table_name):
        _table = Table(table_name, Base.metadata, autoload=True)
        s = [c.name for c in _table.columns]
        for row in s:
            print(row)


    def insert_row(self, table_name, row_data):
        _table = Table(table_name, Base.metadata, autoload=True)
        i = insert(_table)
        i = i.values(row_data)
        self.session.execute(i)
        self.session.commit()

 
    def select_test_suite_id(self, project):
        p = self.session.query(Projects).filter_by(project_name_abbrev=project).first()  
        return p.testrail_functional_test_suite_id

        """
        q = self.session.query(Projects).all()    
        for project in q:
            p = self.session.query(Projects).filter_by(project_name_abbrev='fenix').first()  
            print(p.testrail_functional_test_suite_id)
        """

            

    def select_test_suite_id2(self, project):
        _table = Table('projects', Base.metadata, autoload=True)
        q = self.session.query(_table.columns.testrail_functional_test_suite_id)
        return q.filter(_table.columns['project_name_abbrev']=='fenix').first()[0]


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
