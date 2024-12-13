from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Child:
    def __init__(self, id, first_name, last_name, birth_date, gender, group_id, parent_contact_id, menu_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.group_id = group_id
        self.parent_contact_id = parent_contact_id
        self.menu_id = menu_id


class Parent(UserMixin):
    def __init__(self, id, first_name, last_name, birth_date, phone, email, gender, hash_password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.gender = gender
        self.hash_password = hash_password

    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)

    @property
    def username(self):
        return f"{self.first_name} {self.last_name}"


class Menu:
    def __init__(self, id, since, name, description):
        self.id = id
        self.since = since
        self.name = name
        self.description = description


class Educator:
    def __init__(self, id, first_name, last_name, birth_date, phone, email, qualification, gender):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.qualification = qualification
        self.gender = gender


class Group:
    def __init__(self, id, educator_id, name, from_age, to_age):
        self.id = id
        self.educator_id = educator_id
        self.name = name
        self.from_age = from_age
        self.to_age = to_age
