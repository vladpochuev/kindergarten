from model import *


class GroupDTOMapper:
    def from_entity(self, group, educator, children):
        return GroupDTO(
            group.id,
            group.name,
            f"{educator.first_name} {educator.last_name}",
            f"{group.from_age}-{group.to_age}",
            len(children))
