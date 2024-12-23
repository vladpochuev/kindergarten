from dao.dao import DAO
from model import Group


class GroupDAO(DAO):
    def get_by_id(self, group_id):
        row = self.get_row_args("SELECT * FROM groups WHERE id = %s", (group_id,))
        return Group(row[0], row[1], row[2], row[3], row[4])

    def get_all(self):
        rows = self.get_rows("SELECT * FROM groups")
        return [Group(row[0], row[1], row[2], row[3], row[4]) for row in rows]
