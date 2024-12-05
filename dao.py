class DAO:
    def __init__(self, conn):
        self.conn = conn


class ChildrenDAO(DAO):
    def get_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM children")
        children = cur.fetchall()
        cur.close()
        return children

    def get_by_group(self, group_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM children WHERE group_id = %s", (group_id,))
        children = cur.fetchall()
        cur.close()
        return children

class ParentDAO(DAO):
    def get_by_id(self, parent_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM parents WHERE id = %s", (parent_id,))
        parent = cur.fetchone()
        cur.close()
        return parent


class MenuDAO(DAO):
    def get_by_id(self, meal_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM menu WHERE id = %s", (meal_id,))
        meal = cur.fetchone()
        cur.close()
        return meal


class EducatorDAO(DAO):
    def get_by_id(self, educator_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM educators WHERE id = %s", (educator_id,))
        educator = cur.fetchone()
        cur.close()
        return educator


class GroupDAO(DAO):
    def get_by_id(self, group_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM groups WHERE id = %s", (group_id,))
        group = cur.fetchone()
        cur.close()
        return group
