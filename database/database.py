import sqlite3
from sqlite3 import Error


class DB:
    conn = sqlite3.connect('groupify.db')

    @staticmethod
    def connect():
        try:
            conn = sqlite3.connect('groupify.db')
        except Error:
            print(Error)

    @staticmethod
    def init_table():
        try:
            DB.connect()
            c = conn.cursor()
            sql = open('./database/create_tables.sql', 'r').read()
            c.executescript(sql)
        except Error as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def destroy_table():
        try:
            DB.connect()
            sql = open('./database/destroy_tables.sql', 'r').read()
            conn.cursor().executescript(sql)
        except Error as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    @connect
    def execute(cmd, data=None):
        try:
            DB.connect()
            c = conn.cursor()
            if(data is not None):
                return c.execute(cmd, data)
            return c.execute(cmd)
        except Error as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def executemany(cmd, entities):
        try:
            DB.connect()
            c = conn.cursor()
            c.executemany(cmd, entities)
        except Error as e:
            print(e)
        finally:
            conn.close()
