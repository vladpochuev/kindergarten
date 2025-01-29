from src.python.model import NewChildDTO
from .form_extractor import Extractor


class NewChildFormExtractor(Extractor):
    def get_new_child(self):
        first_name = self.extract("first_name")
        last_name = self.extract("last_name")
        birth_date = self.extract("birth_date")
        gender = self.extract("gender")
        group_id = self.extract("group")
        menu_id = self.extract("menu")

        return NewChildDTO(first_name, last_name, birth_date, gender, group_id, menu_id)
