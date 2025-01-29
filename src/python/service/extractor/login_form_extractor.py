from src.python.model import LoginDTO
from .form_extractor import Extractor


class LoginFormExtractor(Extractor):
    def get_login(self):
        first_name = self.extract("first_name")
        last_name = self.extract("last_name")
        password = self.extract("password")

        return LoginDTO(first_name, last_name, password)
