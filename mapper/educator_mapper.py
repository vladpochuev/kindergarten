from model import *
from service.date_utils import *


class EducatorMapper:
    def get_educator_dto(self, educator):
        return EducatorDTO(
            f"{educator.first_name} {educator.last_name}",
            get_formatted_date(educator.birth_date),
            educator.gender,
            educator.phone,
            educator.email,
            educator.qualification)
