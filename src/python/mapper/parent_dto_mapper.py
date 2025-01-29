from src.python.model import *
from src.python.service.date_utils import *


class ParentDTOMapper:
    def from_entity(self, parent):
        return ParentDTO(
            f"{parent.first_name} {parent.last_name}",
            get_formatted_date(parent.birth_date),
            parent.gender,
            parent.phone,
            parent.email
        )

    def to_entity(self, register_dto, password_hash):
        return Parent(None,
                      register_dto.first_name,
                      register_dto.last_name,
                      register_dto.birth_date,
                      register_dto.phone_number,
                      register_dto.email,
                      register_dto.gender,
                      password_hash)
