from dao.base_dao import DAO
from model import Parent


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
