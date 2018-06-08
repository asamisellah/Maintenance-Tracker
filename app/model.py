from db_connect import TrackerDB
import psycopg2
from psycopg2.extras import RealDictCursor

db = TrackerDB()


class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_user(self):
        db.cur.execute("""INSERT INTO users(username, email, password)
                VALUES(%s,%s,%s)""",
                       (self.username, self.email, self.password,))
        db.conn.commit()


def get_users():
    db.cur.execute("SELECT * FROM users")
    db.conn.commit()
    users = db.cur.fetchall()
    return users


def get_user(username):
    db.cur.execute("SELECT * FROM users WHERE username = (%s);", (username,))
    db.conn.commit()
    user = db.cur.fetchone()
    return user


class UserRequest():
    def __init__(self, user_id, title, description, _type, category, area):
        self.user_id = user_id
        self.title = title
        self.description = description
        self._type = _type
        self.category = category
        self.area = area

    def create_request(self):
        db.cur.execute("""INSERT INTO requests(user_id, title, description, type, category, area)
                VALUES(%s,%s,%s,%s,%s,%s)""",
                       (self.user_id,
                        self.title,
                        self.description,
                        self._type,
                        self.category,
                        self.area))
        db.conn.commit()


def get_all_requests():
    db.cur.execute("SELECT * FROM requests")
    db.conn.commit()
    users = db.cur.fetchall()
    return users


def get_user_requests(user_id):
    db.cur.execute(
        "SELECT * FROM requests WHERE user_id = (%s)", (user_id,))
    db.conn.commit()
    requests = db.cur.fetchall()
    return requests


def get_user_request(request_id, user_id):
    db.cur.execute(
        "SELECT * FROM requests WHERE user_id = (%s) AND id = (%s)",
        (user_id, request_id,))
    db.conn.commit()
    _request = db.cur.fetchall()
    return _request
