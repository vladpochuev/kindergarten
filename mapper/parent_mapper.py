from model import *
from service.date_utils import *


class ParentMapper:
    def get_parent_dto(self, parent):
        return ParentDTO(
            f"{parent.first_name} {parent.last_name}",
            get_formatted_date(parent.birth_date),
            parent.gender,
            parent.phone,
            parent.email
        )
