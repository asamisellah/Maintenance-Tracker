from db_connect import TrackerDB

db = TrackerDB()


def register_user(username, email, password):
    db.cur.execute("""INSERT INTO users (username, email, password) VALUES(%s,%s,%s)""",
                   (username, email, password,)),
    db.conn.commit()
    # db.conn.close()


def create_request(title, description, category, _type, area):
    db.cur.execute("""INSERT INTO requests (title, description, category, type, area) VALUES(%s,%s,%s,%s,%s)""",
                   (title, description, category, _type, area,))
    db.conn.commit()
    db.conn.close()


def get_requests():
    db.cur.execute("SELECT * FROM requests")
    db.conn.commit()
    requests = db.cur.fetchall()
    return requests
