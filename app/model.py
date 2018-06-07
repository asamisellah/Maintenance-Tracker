from db_connect import MyDatabase
import psycopg2

db = MyDatabase()


class User():
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def create_user(self):
        db.query("""INSERT INTO users(username, email, password)
                VALUES(%s,%s,%s)""",
                 (self.username, self.email, self.password,))

    def get_user(self, username):
        db.query("SELECT * FROM users")
        users = db.cur.fetchall()
        print(users)


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

    def get_request(self, id):
        pass


def serialize(self):
    return {
        "username": self.username,
        "email": self.email,
        "password": self.password
    }
