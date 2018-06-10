from db_connect import TrackerDB
from psycopg2.extras import RealDictCursor
from passlib.hash import pbkdf2_sha256 as sha256
import psycopg2

db = TrackerDB()


class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_user(self):
        db.cur.execute("""INSERT INTO users(username, email, password)
                VALUES(%s,%s,%s)""",
                       (self.username, self.email,
                        generate_hash(self.password),))
        db.conn.commit()


def generate_hash(password):
    return sha256.hash(password)


def drop():
    db.query("""DROP TABLE IF EXISTS users""")
    db.query("""DROP TABLE IF EXISTS requests""")
    db.conn.commit()


def init():
    db.query("""CREATE TABLE users(
            id serial PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255),
            password VARCHAR(255),
            admin_role BOOLEAN DEFAULT FALSE
        )
            """)
    db.query("""CREATE TABLE requests(
            id serial PRIMARY KEY,
            user_id integer,
            title VARCHAR(255),
            description VARCHAR(255),
            type VARCHAR(255),
            category VARCHAR(255),
            area VARCHAR(255),
            status VARCHAR(255)
        )
            """)
    db.conn.commit()


def verify_hash(password, hash):
    return sha256.verify(password, hash)


def get_users():
    db.cur.execute("SELECT * FROM users")
    db.conn.commit()
    users = db.cur.fetchall()
    return users


def get_user_by_id(user_id):
    db.cur.execute("SELECT * FROM users WHERE id = (%s)", (user_id,))
    db.conn.commit()
    users = db.cur.fetchone()
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
        db.cur.execute("""INSERT INTO
                requests(user_id, title, description,
                type, category, area, status)
                VALUES(%s,%s,%s,%s,%s,%s,'pending')""",
                       (self.user_id,
                        self.title,
                        self.description,
                        self._type,
                        self.category,
                        self.area))
        db.conn.commit()
        count = len(get_all_requests())
        db.cur.execute(
            "SELECT * FROM requests WHERE id = (%s) AND user_id = (%s)",
            (count, self.user_id,))
        new_request = db.cur.fetchone()
        return new_request


def get_all_requests():
    db.cur.execute("SELECT * FROM requests")
    db.conn.commit()
    users = db.cur.fetchall()
    return users


def get_request(request_id):
    db.cur.execute(
        "SELECT * FROM requests WHERE id = (%s)", (request_id,))
    db.conn.commit()
    user_request = db.cur.fetchone()
    return user_request


def get_user_requests(user_id):
    db.cur.execute(
        "SELECT * FROM requests WHERE user_id = (%s)", (user_id,))
    db.conn.commit()
    user_requests = db.cur.fetchall()
    return user_requests


def get_user_request(request_id, user_id):
    db.cur.execute(
        "SELECT * FROM requests WHERE user_id = (%s) AND id = (%s)",
        (user_id, request_id,))
    db.conn.commit()
    user_request = db.cur.fetchone()
    return user_request


def update_request(request_id, user_id, title,
                   description, type, category, area):
    db.cur.execute("""UPDATE requests
                SET title = (%s),
                description = (%s),
                type = (%s),
                category = (%s),
                area = (%s)
                WHERE id = (%s) AND user_id = (%s)""",
                   (title, description, type, category,
                    area, request_id, user_id,))
    db.conn.commit()


def delete_request(request_id, user_id):
    db.cur.execute("DELETE FROM requests WHERE id = (%s) AND user_id = (%s)",
                   (request_id, user_id,))
    db.conn.commit()


def update_status(request_id, status):
    db.cur.execute("UPDATE requests SET status = (%s) WHERE id = (%s)",
                   (status, request_id,))
    db.conn.commit()
    return status
