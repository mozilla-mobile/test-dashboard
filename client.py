from base import Session, Base

from sqlalchemy import Table, insert


class BaseAPI(object):

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

    def update_testrail():
        pass

    def update_github():
        table1 = 'github_fenix_intermittent_tests' # noqa
        table2 = 'github_test' #noqa
        table3 = 'github_test_by_day' #noqa
        pass

    def update_taskcluster():
        pass

    def update_bitrise():
        table = 'bitrise_build_states' #noqa

        """
        | coverage                        |
        | songs                           |
        | test_aaron                      |
        | testrail_test_coverage
        """
        pass

    def main(self):
        table_name = 'songs'
        row_data = {'title': 'Ramones', 'artist': 'The Ramones', 'genre': 'punk'} # noqa
        self.insert_row(table_name, row_data)


if __name__ == '__main__':
    c = BaseAPI()
    c.main()
