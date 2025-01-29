from src.python.model import RegisterDTO
from .form_extractor import Extractor


class RegisterFormExtractor(Extractor):
    def get_register(self):
        first_name = self.extract("first_name")
        last_name = self.extract("last_name")
        birth_date = self.extract("birth_date")
        phone_number = self.extract("phone_number")
        email = self.extract("email")
        gender = self.extract("gender")
        password = self.extract("password")

        return RegisterDTO(first_name, last_name, birth_date, phone_number, email, gender, password)
