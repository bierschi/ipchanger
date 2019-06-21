import os
import logging
import sqlite3
import time
from definitions import ROOT_DIR


class ProxyDB:
    """class ProxyDB to save active and dead proxies in a local database

    USAGE:
            ProxyDB()
    """
    def __init__(self, db_name='proxy'):
        self.logger = logging.getLogger('ipchanger')
        self.logger.info("create class ProxyDB")

        self.db_name = db_name + '.db'
        self.db_path = ROOT_DIR + '/db/' + self.db_name

        if not os.path.exists(self.db_path):
            self.__create_db()
        else:
            self.connection = sqlite3.connect(self.db_path)

    def __del__(self):
        """destructor

        """
        self.connection.close()

    def __create_db(self):
        """creates proxy database with PROXYUP and PROXYDEAD tables

        """
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

        proxyup_table = "CREATE TABLE PROXYUP" \
                        "(ID       INT PRIMARY KEY NOT NULL," \
                        "TIMESTAMP INT             NOT NULL," \
                        "IP        TEXT            NOT NULL," \
                        "PORT      INT             NOT NULL);"

        proxydown_table = "CREATE TABLE PROXYDEAD" \
                        "(ID       INT PRIMARY KEY NOT NULL," \
                        "TIMESTAMP INT             NOT NULL," \
                        "IP        TEXT            NOT NULL," \
                        "PORT      INT             NOT NULL);"

        self.cursor.execute(proxyup_table)
        self.cursor.execute(proxydown_table)
        self.connection.commit()

        self.logger.info("created proxyup and proxydown table in %s" % self.db_name)

    def get_last_row(self, table):
        """get last row in 'table'

        :return: set: last row in 'table'
        """
        cur = self.connection.cursor()
        cur.execute("SELECT *  FROM %s ORDER BY id DESC LIMIT 1" % table)
        return cur.fetchone()

    def insert_proxyup(self, id, ip, port):
        """insert a proxy up with id, ip, port

        """
        sql = "INSERT INTO PROXYUP (ID, TIMESTAMP, IP, PORT) Values (?, ?, ?, ?)"
        cur = self.connection.cursor()

        try:
            cur.execute(sql, (id, time.time(), ip, port))
        except sqlite3.IntegrityError as ex:
            self.logger.error("error while trying to insert in db: %s" % ex)

        self.connection.commit()

    def insert_proxydead(self, id , ip, port):
        """insert a proxy dead with id, ip, port

        """
        sql = "INSERT INTO PROXYDEAD (ID, TIMESTAMP, IP, PORT) Values (?, ?, ?, ?)"
        cur = self.connection.cursor()

        try:
            cur.execute(sql, (id, time.time(), ip, port))
        except sqlite3.IntegrityError as ex:
            self.logger.error("error while trying to insert in db: %s" % ex)

        self.connection.commit()

    def delete_proxyup_id(self, id):
        """deletes a proxy in table 'proxyup' with given id

        :param id:
        :return:
        """
        pass

    def delete_proxydead_id(self, id):
        """deletes a proxy in table 'proxydead' with given id

        :param id:
        :return:
        """
        pass


if __name__ == '__main__':
    db = ProxyDB()
    print(db.get_last_row(table='PROXYUP'))