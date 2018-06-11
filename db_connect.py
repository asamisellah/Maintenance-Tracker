from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import os
from flask import current_app

# Main Database


class TrackerDB(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.conn = connect(postgres: // cprwgabrqpkdmg: 1821cee79a9993b605b275bd608c135fa4e17ded697b53515bb1f7ddf4baa0c0@ec2-50-19-224-165.compute-1.amazonaws.com: 5432/d7bp9i00oopfpn)
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
