from werkzeug.security import check_password_hash
from flask_login import UserMixin


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
