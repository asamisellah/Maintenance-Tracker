from psycopg2 import connect
from psycopg2.extras import RealDictCursor

connection = {
    "host": "localhost",
    "database": "mtracker",
    "user": "postgres",
    "password": "db"
}

test_connection = {
    "host": "localhost",
    "database": "mtracker_test",
    "user": "postgres",
    "password": "db"
}

# Main Database


class TrackerDB(object):

    def __init__(self):
        self.conn = connect(**connection)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

# Tests Database


class TestDB(object):

    def __init__(self):
        self.conn = connect(**test_connection)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
