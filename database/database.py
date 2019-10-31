import sqlite3
from sqlite3 import Error


class DB:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('groupify.db')
        except Error:
            print(Error)

    def init_table(self):
        c = self.conn.cursor()
        sql = open('./database/create_tables.sql', 'r').read()
        c.executescript(sql)

    def destroy_table(self):
        sql = open('./database/destroy_tables.sql', 'r').read()
        self.conn.cursor().executescript(sql)

    def execute(self, cmd):
        c = self.conn.cursor()
        return c.execute(cmd)

    def executemany(self, cmd, entities):
        c = self.conn.cursor()
        c.executemany(cmd, entities)


if __name__ == "__main__":
    db = DB()
