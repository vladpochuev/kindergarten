from dao.base_dao import DAO
from model import Educator


class EducatorDAO(DAO):
    def get_by_id(self, educator_id):
        row = self.get_row_args("SELECT * FROM educators WHERE id = %s", (educator_id,))
        return Educator(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
