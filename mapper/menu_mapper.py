from model import *
from service.date_utils import *


class MenuMapper:
    def get_menu_dto(self, menu):
        return MenuDTO(
            menu.id,
            menu.name,
            menu.description,
            get_formatted_date(menu.since))
