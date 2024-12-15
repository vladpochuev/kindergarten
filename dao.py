from models import *
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


class ChildDAO(DAO):
    def get_all(self):
        rows = self.get_rows("SELECT * FROM children")
        return [Child(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]

    def get_by_group(self, group_id):
        rows = self.get_rows_args("SELECT * FROM children WHERE group_id = %s", (group_id,))
        return [Child(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) for row in rows]

    def save(self, child):
        self.save_obj(
            "INSERT INTO children (first_name, last_name, birth_date, gender, group_id, parent_id, menu_id) " +
            "VALUES (%s, %s, %s, %s, %s, %s, %s)", (
                child.first_name, child.last_name, child.birth_date, child.gender, child.group_id,
                child.parent_id,
                child.menu_id))


class ParentDAO(DAO):
    def get_by_id(self, parent_id):
        row = self.get_row_args("SELECT * FROM parents WHERE id = %s", (parent_id,))
        return Parent(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def exists_by_name(self, name):
        row = self.get_row_args("SELECT * FROM parents WHERE CONCAT(first_name, ' ', last_name) = %s", (name,))
        return row is not None

    def get_by_name(self, name):
        row = self.get_row_args("SELECT * FROM parents WHERE CONCAT(first_name, ' ', last_name) = %s", (name,))
        if row is None:
            return None
        return Parent(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

    def save(self, parent):
        self.save_obj("INSERT INTO parents (first_name, last_name, birth_date, phone, email, gender, hash_password) " +
                      "VALUES (%s, %s, %s, %s, %s, %s, %s)", (
                          parent.first_name, parent.last_name, parent.birth_date, parent.phone, parent.email,
                          parent.gender,
                          parent.hash_password))


class MenuDAO(DAO):
    def get_by_id(self, menu_id):
        row = self.get_row_args("SELECT * FROM menu WHERE id = %s", (menu_id,))
        return Menu(row[0], row[1], row[2], row[3])

    def get_all(self):
        rows = self.get_rows("SELECT * FROM menu")
        return [Menu(row[0], row[1], row[2], row[3]) for row in rows]


class EducatorDAO(DAO):
    def get_by_id(self, educator_id):
        row = self.get_row_args("SELECT * FROM educators WHERE id = %s", (educator_id,))
        return Educator(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])


class GroupDAO(DAO):
    def get_by_id(self, group_id):
        row = self.get_row_args("SELECT * FROM groups WHERE id = %s", (group_id,))
        return Group(row[0], row[1], row[2], row[3], row[4])

    def get_all(self):
        rows = self.get_rows("SELECT * FROM groups")
        return [Group(row[0], row[1], row[2], row[3], row[4]) for row in rows]
