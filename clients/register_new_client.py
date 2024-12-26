from requests_to_db.client_requests import ADD_CLIENT
from settings.settings_for_connect import CONNECTION
from utils import errors
from datetime import date
from utils.encrypt_funcs import hash_pwd, encrypt_text
from clients.check_args import check_username_already_exist, check_email, check_telephone_number
from fastapi import HTTPException
from settings.encrypt_settings import LEVEL_ENCRYPT

# Переменная для подключения к БД
connection = CONNECTION

# Функция для добавления пользователя в БД
def add_client(username: str, name: str, surname: str, email: str, password: str, telephone_number: str):
    # Курсор для работы с БД
    cursor = connection.cursor()

    # Проверка, что пользователя с таким именем не существует
    if check_username_already_exist(username, cursor) == errors.USERNAME_ALREADY_EXIST:
        raise HTTPException(status_code=403, detail="Username already exists")

    # Проверка корректности введенного номера телефона
    error_code = check_telephone_number(telephone_number, cursor)

    # Обработка ошибок при некорректном номере телефона
    match error_code:
        case errors.TELEPHONE_NUMBER_INCORRECT:
            raise HTTPException(status_code=403, detail="Incorrect telephone number")
        case errors.TELEPHONE_NUMBER_ALREADY_EXIST:
            raise HTTPException(status_code=403, detail="Telephone number already exists")

    # Проверка на корректность адреса электронной почты
    error_code = check_email(email, cursor)

    # Обработка ошибок при некорректном адресе
    match error_code:
        case errors.EMAIL_INCORRECT:
            raise HTTPException(status_code=403, detail="Incorrect email")
        case errors.EMAIL_ALREADY_EXIST:
            raise HTTPException(status_code=403, detail="Email already exists")

    # В случае успешного прохождения всех проверок, пользователь добавляется в БД
    add_client_to_db(username, name, surname, email, password, telephone_number, cursor)

    connection.commit()
    return errors.OK


# Функция для добавления проверенного пользователя в БД
def add_client_to_db(username: str, name: str, surname: str, email: str, password: str, telephone_number: str, cursor):
    cursor.execute(ADD_CLIENT, (encrypt_text(username, LEVEL_ENCRYPT), hash_pwd(password),
                                encrypt_text(name, LEVEL_ENCRYPT), encrypt_text(surname, LEVEL_ENCRYPT),
                                encrypt_text(email, LEVEL_ENCRYPT), encrypt_text(telephone_number, LEVEL_ENCRYPT),
                                date.today()))
