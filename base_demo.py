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

    def main(self):
        table_name = 'songs'
        row_data = {'title': 'Ramones', 'artist': 'The Ramones', 'genre': 'punk'}
        self.insert_row(table_name, row_data)


if __name__ == '__main__':
    c = BaseAPI()
    c.main()
