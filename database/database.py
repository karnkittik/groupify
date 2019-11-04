import sqlite3
from sqlite3 import Error


class DB:
    # conn = sqlite3.connect('groupify.db')

    @staticmethod
    def connect():
        try:
            conn = sqlite3.connect('groupify.db')
            return conn
        except Error:
            print(Error)

    @staticmethod
    def init_table():
        try:
            conn = DB.connect()
            c = conn.cursor()
            sql = open('./database/create_tables.sql', 'r').read()
            c.executescript(sql)
            conn.commit()
        except Error as e:
            raise

    @staticmethod
    def destroy_table():
        try:
            conn = DB.connect()
            sql = open('./database/destroy_tables.sql', 'r').read()
            conn.cursor().executescript(sql)
            conn.commit()
        except Error as e:
            raise

    @staticmethod
    def execute(cmd, data: tuple = None):
        try:
            conn = DB.connect()
            c = conn.cursor()
            result = None
            if(data is not None):
                result = c.execute(cmd, data)
            else:
                result = c.execute(cmd)
            conn.commit()
            return result
        except Error as e:
            raise

    @staticmethod
    def executemultiplesql(cmdWithData: list):
        try:
            conn = DB.connect()
            c = conn.cursor()
            for (cmd, data) in cmdWithData:
                if data is None:
                    c.execute(cmd)
                else:
                    c.execute(cmd, data)
            conn.commit()
        except Error as e:
            raise

    @staticmethod
    def executemany(cmd, entities: list):
        try:
            conn = DB.connect()
            c = conn.cursor()
            c.executemany(cmd, entities)
            conn.commit()
        except Error as e:
            raise
