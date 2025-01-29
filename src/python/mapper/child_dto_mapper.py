from src.python.model import *
from src.python.service.date_utils import *


class ChildDTOMapper:
    def from_entity(self, child, group, educator, parent, menu):
        return ChildDTO(
            child.first_name,
            child.last_name,
            get_age(child.birth_date),
            child.gender,
            parent.id,
            f"{parent.first_name} {parent.last_name}",
            group.id,
            group.name,
            educator.id,
            f"{educator.first_name} {educator.last_name}",
            menu.id,
            menu.name)

    def to_entity(self, new_child_dto, parent_id):
        return Child(None,
                     new_child_dto.first_name,
                     new_child_dto.last_name,
                     new_child_dto.birth_date,
                     new_child_dto.gender,
                     new_child_dto.group_id,
                     parent_id,
                     new_child_dto.menu_id)
