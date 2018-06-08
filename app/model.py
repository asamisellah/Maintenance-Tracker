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


# def update_user(username):
#     db.cur.execute("SELECT user FROM users WHERE username == ")
#     db.conn.commit()


class UserRequest():
    def __init__(self, id, title, description, type, category, area):
        # self.id = count
        self.title = title
        self.description = description
        self.type = type
        self.category = category
        self.area = area
        count += 1

    def create_request(self):
        pass

    # def get_requests(self, id):
    #     db.cur.execute("SELECT * FROM users")
    #     db.conn.commit()
    #     users = db.cur.fetchall()
    #     return users
