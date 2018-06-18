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
        self.conn = connect(app.config['DATABASE_URL'])
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()
