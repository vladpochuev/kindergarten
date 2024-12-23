from model import *
from service.date_utils import *


class MenuDTOMapper:
    def from_entity(self, menu):
        return MenuDTO(
            menu.id,
            menu.name,
            menu.description,
            get_formatted_date(menu.since))
