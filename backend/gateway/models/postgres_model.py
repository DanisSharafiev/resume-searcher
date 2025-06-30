import psycopg2

class PostgresModel:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def fetch_from_id(self, item_id):
        self.cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        return self.cur.fetchone()

    def close(self):
        self.cur.close()
        self.conn.close()
