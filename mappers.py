from date_utils import *
from dto import *


def get_child_dto(child, group, educator, parent, menu):
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
        menu.name)


def get_parent_dto(parent):
    return ParentDTO(
        f"{parent.first_name} {parent.last_name}",
        get_formatted_date(parent.birth_date),
        parent.gender,
        parent.phone,
        parent.email
    )


def get_group_dto(group, educator, children):
    return GroupDTO(
        group.name,
        f"{educator.first_name} {educator.last_name}",
        f"{group.from_age}-{group.to_age}",
        len(children))


def get_educator_dto(educator):
    return EducatorDTO(
        f"{educator.first_name} {educator.last_name}",
        get_formatted_date(educator.birth_date),
        educator.gender,
        educator.phone,
        educator.email,
        educator.qualification)
