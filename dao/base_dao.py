from psycopg2.errors import CheckViolation


class DAO:
    def __init__(self, conn):
        self.conn = conn

    def get_rows(self, query):
        return self.get_rows_args(query, None)

    def get_row(self, query):
        return self.get_row_args(query, None)

    def get_rows_args(self, query, args):
        cur = self.conn.cursor()
        cur.execute(query, args)
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_row_args(self, query, args):
        cur = self.conn.cursor()
        cur.execute(query, args)
        row = cur.fetchone()
        cur.close()
        return row

    def save_obj(self, query, args):
        cur = self.conn.cursor()
        try:
            cur.execute(query, args)
            self.conn.commit()
        except CheckViolation:
            raise ValueError
        finally:
            cur.close()
