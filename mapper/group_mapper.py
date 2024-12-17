from model import *


class GroupMapper:
    def get_group_dto(self, group, educator, children):
        return GroupDTO(
            group.id,
            group.name,
            f"{educator.first_name} {educator.last_name}",
            f"{group.from_age}-{group.to_age}",
            len(children))
