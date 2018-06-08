from db_connect import TrackerDB
import psycopg2
from psycopg2.extras import RealDictCursor

db = TrackerDB()


class User():
    def __init__(self, user_id, username, email, password):
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
    db.cur.execute("SELECT * FROM users WHERE USERNAME = (%s);", (username,))
    db.conn.commit()
    user = db.cur.fetchone()
    return user


class UserRequest():
    def __init__(self, request_id, title, description, type, category, area):
        self.title = title
        self.description = description
        self.type = type
        self.category = category
        self.area = area

    def create_request(self):
        db.cur.execute("""INSERT INTO requests(title, description, type, category, area)
                VALUES(%s,%s,%s,%s,%s)""",
                       (self.title,
                        self.description,
                        self.type,
                        self.category,
                        self.area))
        db.conn.commit()


def get_requests():
    db.cur.execute("SELECT * FROM requests")
    db.conn.commit()
    users = db.cur.fetchall()
    return users


# def update_user(username):
#     db.cur.execute("SELECT user FROM users WHERE username == ")
#     db.conn.commit()
