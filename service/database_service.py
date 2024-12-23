from dao import *


class DatabaseService:
    def __init__(self, conn):
        self.children = ChildDAO(conn)
        self.parents = ParentDAO(conn)
        self.educators = EducatorDAO(conn)
        self.groups = GroupDAO(conn)
        self.menus = MenuDAO(conn)
