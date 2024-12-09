class ChildDTO:
    def __init__(self, first_name, last_name, age, gender, parent_id, parent_name, group_id, group, educator_id,
                 educator, menu_id, menu):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.parent_id = parent_id
        self.parent_name = parent_name
        self.group_id = group_id
        self.group = group
        self.educator_id = educator_id
        self.educator = educator
        self.menu_id = menu_id
        self.menu = menu


class ParentDTO:
    def __init__(self, name, birth_date, gender, phone, email):
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.phone = phone
        self.email = email


class GroupDTO:
    def __init__(self, name, educator, age_range, size):
        self.name = name
        self.educator = educator
        self.age_range = age_range
        self.size = size


class EducatorDTO:
    def __init__(self, name, birth_date, gender, phone, email, qualification):
        self.name = name
        self.birth_date = birth_date
        self.gender = gender
        self.phone = phone
        self.email = email
        self.qualification = qualification


class MenuDTO:
    def __init__(self, name, description, since):
        self.name = name
        self.description = description
        self.since = since
