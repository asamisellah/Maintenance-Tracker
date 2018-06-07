from db_connect import MyDatabase
import psycopg2
import sys

db = MyDatabase()


def main():
    try:
        db.query("""DROP TABLE IF EXISTS users""")
        db.query("""DROP TABLE IF EXISTS requests""")

        db.query("""CREATE TABLE users(
            username varchar(255),
            email varchar(255),
            password varchar(255)
        )
            """)
        db.query("""CREATE TABLE requests(
            title varchar(255),
            description varchar(255),
            type varchar(255),
            category varchar(255),
            area varchar(255)
        )
            """)
        db.conn.commit()
    except psycopg2.Error:
        raise SystemExit("Failed {}".format(sys.exc_info()))

        db.close()


if __name__ == "__main__":
    main()
