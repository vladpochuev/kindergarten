from model import *
from service.date_utils import *


class ChildMapper:
    def get_child_dto(self, child, group, educator, parent, menu):
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
