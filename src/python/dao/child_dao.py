from src.python.dao.dao import DAO
from src.python.model import Child


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
