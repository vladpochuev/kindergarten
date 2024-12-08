from collections import namedtuple


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


class ChildDAO(DAO):
    child_template = namedtuple("Child",
                                ["id", "first_name", "last_name", "birth_date", "gender", "group_id",
                                 "parent_contact_id", "menu_id"])

    def get_all(self):
        rows = self.get_rows("SELECT * FROM children")
        return [self.child_template(*row) for row in rows]

    def get_by_group(self, group_id):
        rows = self.get_rows_args("SELECT * FROM children WHERE group_id = %s", (group_id,))
        return [self.child_template(*row) for row in rows]


class ParentDAO(DAO):
    parent_template = namedtuple("Parent", ["id", "first_name", "last_name", "birth_date",
                                            "phone", "email", "gender"])

    def get_by_id(self, parent_id):
        row = self.get_row_args("SELECT * FROM parents WHERE id = %s", (parent_id,))
        return self.parent_template(*row)


class MenuDAO(DAO):
    menu_template = namedtuple("Menu", ["id", "since", "name", "description"])

    def get_by_id(self, menu_id):
        row = self.get_row_args("SELECT * FROM menu WHERE id = %s", (menu_id,))
        return self.menu_template(*row)


class EducatorDAO(DAO):
    educator_template = namedtuple("Educator",
                                   ["id", "first_name", "last_name", "birth_date", "phone", "email",
                                    "qualification", "gender"])

    def get_by_id(self, educator_id):
        row = self.get_row_args("SELECT * FROM educators WHERE id = %s", (educator_id,))
        return self.educator_template(*row)


class GroupDAO(DAO):
    group_template = namedtuple("Group", ["id", "educator_id", "name", "from_age", "to_age"])

    def get_by_id(self, group_id):
        row = self.get_row_args("SELECT * FROM groups WHERE id = %s", (group_id,))
        return self.group_template(*row)
