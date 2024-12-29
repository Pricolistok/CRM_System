from requests_to_db.client_requests import ADD_CLIENT
from settings.settings_for_connect import CONNECTION
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

    # Проверка, что пользователя с таким именем не существует
    if check_username_already_exist(client.username, cursor) == errors.USERNAME_ALREADY_EXIST:
        raise HTTPException(status_code=403, detail="Username already exists")

    # Проверка корректности введенного номера телефона
    error_code = check_telephone_number(client.telephone_number, cursor)

    # Обработка ошибок при некорректном номере телефона
    match error_code:
        case errors.TELEPHONE_NUMBER_INCORRECT:
            raise HTTPException(status_code=403, detail="Incorrect telephone number")
        case errors.TELEPHONE_NUMBER_ALREADY_EXIST:
            raise HTTPException(status_code=403, detail="Telephone number already exists")

    # Проверка на корректность адреса электронной почты
    error_code = check_email(client.email, cursor)

    # Обработка ошибок при некорректном адресе
    match error_code:
        case errors.EMAIL_INCORRECT:
            raise HTTPException(status_code=403, detail="Incorrect email")
        case errors.EMAIL_ALREADY_EXIST:
            raise HTTPException(status_code=403, detail="Email already exists")

    # В случае успешного прохождения всех проверок, пользователь добавляется в БД
    add_client_to_db(client)

    connection.commit()
    return errors.OK


# Функция для добавления проверенного пользователя в БД
def add_client_to_db(client: Client):
    cursor.execute(ADD_CLIENT, (encrypt_text(client.username, LEVEL_ENCRYPT), hash_pwd(client.password),
                                encrypt_text(client.name, LEVEL_ENCRYPT), encrypt_text(client.surname, LEVEL_ENCRYPT),
                                encrypt_text(client.email, LEVEL_ENCRYPT), encrypt_text(client.telephone_number, LEVEL_ENCRYPT),
                                date.today()))
