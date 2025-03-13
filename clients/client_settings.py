from datetime import datetime
from pydantic import BaseModel


class Client:
    def __init__(self, username: str, password: str, name: str, surname: str, email: str, telephone_number: str):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email
        self.telephone_number = telephone_number
        self.date_of_birth = datetime.now()

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

class Token:
    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type
