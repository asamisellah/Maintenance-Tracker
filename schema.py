import sys
import psycopg2

from db_connect import TrackerDB

from app import app

db = TrackerDB(app)


def main():
    try:
        db.query("""DROP TABLE IF EXISTS users""")
        db.query("""DROP TABLE IF EXISTS requests""")

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
        db.conn.close()
    except psycopg2.Error:
        raise SystemExit("Failed {}".format(sys.exc_info()))


if __name__ == "__main__":
    main()
