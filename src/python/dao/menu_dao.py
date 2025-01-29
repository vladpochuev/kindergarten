from src.python.dao.dao import DAO
from src.python.model import Menu


class MenuDAO(DAO):
    def get_by_id(self, menu_id):
        row = self.get_row_args("SELECT * FROM menus WHERE id = %s", (menu_id,))
        return Menu(row[0], row[1], row[2], row[3])

    def get_all(self):
        rows = self.get_rows("SELECT * FROM menus")
        return [Menu(row[0], row[1], row[2], row[3]) for row in rows]
