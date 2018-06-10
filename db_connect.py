from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import os
connection = {
    "host": os.getenv('DB_HOST'),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
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
        self.conn = connect(os.getenv(DATABASE_URL))
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
