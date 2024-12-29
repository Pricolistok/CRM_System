from datetime import datetime

from PyQt5.QtCore.QUrl import password


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
