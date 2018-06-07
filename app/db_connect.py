import psycopg2


class MyDatabase():
    def __init__(self,
                 host="localhost",
                 db="mtracker",
                 user="postgres", password="db"):
        self.conn = psycopg2.connect(
            host=host, database=db, user=user, password=password)
        self.cur = self.conn.cursor()

    def query(self, query, args):
        self.cur.execute(query, args)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
