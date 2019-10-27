import unittest
from pyhidentity.db.fetcher import DBFetcher
from pyhidentity.db.inserter import DBInserter
from pyhidentity.db.creator import DBCreator, Table, Column
from pyhidentity.db.connector import DBConnector


class TestDBCreator(unittest.TestCase):

    def setUp(self) -> None:

        # set up DBConnector instance
        DBConnector().connect_sqlite("test.db")
        self.fetcher = DBFetcher()
        self.inserter = DBInserter()
        self.creator = DBCreator()
        self.creator.build(obj=Table("test", Column(name="id", type="bigint"),
                                             Column(name="username", type="text")))

    def test_database(self):
        pass

    def test_schema(self):
        pass

    def test_table(self):
        pass

    def test_column(self):
        pass

    def tearDown(self) -> None:

        sql = "delete from test"
        self.inserter.sql(sql=sql)


if __name__ == '__main__':
    unittest.main()