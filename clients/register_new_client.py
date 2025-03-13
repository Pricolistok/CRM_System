from requests_to_db.client_requests import ADD_CLIENT
from settings.settings_for_connect import CONNECTION
from string import ascii_letters
from utils import errors
from datetime import date
from utils.encrypt_funcs import hash_pwd, encrypt_text
from clients.check_args import check_username_already_exist, check_email, check_telephone_number
from fastapi import HTTPException
from settings.encrypt_settings import LEVEL_ENCRYPT
from clients.client_settings import Client

# Переменная для подключения к БД
connection = CONNECTION
cursor = connection.cursor()

# Функция для добавления пользователя в БД
def add_client(client: Client):
    # Курсор для работы с БД
    cursor = connection.cursor()

    # Проверка username на иные символы
    check_username(client.username)

    # Проверка password на иные символы
    check_password(client.password)

    # Проверка name на иные символы
    check_name(client.name)

    # Проверка surname на иные символы
    check_surname(client.surname)

    # Проверка корректности введенного номера телефона
    error_code = check_telephone_number(client.telephone_number, cursor)

    # Обработка ошибок при некорректном номере телефона
    work_with_errors(error_code, 'Telephone number')

    # Проверка на корректность адреса электронной почты
    error_code = check_email(client.email, cursor)

    # Обработка ошибок при некорректном адресе
    work_with_errors(error_code, 'Email')

    # В случае успешного прохождения всех проверок, пользователь добавляется в БД
    add_client_to_db(client)

    connection.commit()
    return errors.OK


# Функция для обработки ошибок
def work_with_errors(error_code: int, name_of_error: str):
    match error_code:
        case errors.EMAIL_INCORRECT:
            raise HTTPException(status_code=403, detail=f'Incorrect {name_of_error}')
        case errors.EMAIL_ALREADY_EXIST:
            raise HTTPException(status_code=403, detail=f'{name_of_error} already exists')


# Функция для проверки поля username
def check_username(username: str):
    if len(username) > 50:
        HTTPException(status_code=403, detail="Username Incorrect")

    for symbol in username:
        if symbol not in ascii_letters + '_1234567890':
            raise HTTPException(status_code=403, detail="Username Incorrect")

    if check_username_already_exist(username, cursor) == errors.USERNAME_ALREADY_EXIST:
        raise HTTPException(status_code=403, detail="Username already exists")


# Функция для проверки поля name
def check_name(name: str):
    if len(name) > 50:
        HTTPException(status_code=403, detail="Name Incorrect")

    for symbol in name:
        if symbol not in ascii_letters:
            raise HTTPException(status_code=403, detail="Name Incorrect")


# Функция для проверки поля name
def check_surname(surname: str):
    if len(surname) > 50:
        HTTPException(status_code=403, detail="Surname Incorrect")

    for symbol in surname:
        if symbol not in ascii_letters:
            raise HTTPException(status_code=403, detail="Surname Incorrect")


# Функция для проверки поля password
def check_password(password: str):
    if len(password) > 50:
        HTTPException(status_code=403, detail="Password Incorrect")

    for symbol in password:
        if symbol not in ascii_letters + '!?!@#$%^&*()-+=_1234567890':
            raise HTTPException(status_code=403, detail="Password Incorrect")



# Функция для добавления проверенного пользователя в БД
def add_client_to_db(client: Client):
    cursor.execute(ADD_CLIENT, (encrypt_text(client.username, LEVEL_ENCRYPT), hash_pwd(client.password),
                                encrypt_text(client.name, LEVEL_ENCRYPT), encrypt_text(client.surname, LEVEL_ENCRYPT),
                                encrypt_text(client.email, LEVEL_ENCRYPT), encrypt_text(client.telephone_number, LEVEL_ENCRYPT),
                                date.today()))
