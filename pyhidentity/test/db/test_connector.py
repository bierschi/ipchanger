import unittest
import sqlite3
from pyhidentity.db.connector import DBConnector


class TestDBConnector(unittest.TestCase):

    def setUp(self) -> None:

        # set up DBConnector instance
        self.connector = DBConnector()
        self.connector.connect_sqlite("test.db")

    def test_get_cursor(self):

        with self.connector.get_cursor() as cursor:
            self.assertIsInstance(cursor, sqlite3.Cursor, msg="cursor must be type of psycopg2.extensions.cursor")

    def test_get_conn(self):

        with self.connector.get_conn() as conn:
            self.assertIsInstance(conn, sqlite3.Connection, msg="conn must be type of psycopg2.extensions.connection")

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
