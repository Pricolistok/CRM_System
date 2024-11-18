from requests_to_db.client_requests import ADD_CLIENT, CHECK_EQ_USERNAME, CHECK_EQ_EMAIL, CHECK_EQ_TELEPHONE_NUMBER
from utils.settings_for_connect import CONNECTION
from utils import errors
from datetime import date

connection = CONNECTION


def add_client(username: str, name: str, surname: str, email: str, password: str, telephone_number: str):
    cursor = connection.cursor()
    if check_username_in_db(username, cursor) == errors.USERNAME_ALREADY_EXIST:
        return errors.USERNAME_ALREADY_EXIST

    if check_email_in_db(email, cursor) == errors.EMAIL_ALREADY_EXIST:
        return errors.EMAIL_ALREADY_EXIST

    if check_telephone_number_in_db(telephone_number, cursor) == errors.TELEPHONE_NUMBER_ALREADY_EXIST:
        return errors.TELEPHONE_NUMBER_ALREADY_EXIST

    error_code = add_client_to_db(username, name, surname, email, password, telephone_number, cursor)
    if error_code != errors.OK:
        return error_code

    connection.commit()


def add_client_to_db(username: str, name: str, surname: str, email: str, password: str, telephone_number: str, cursor):
    cursor.execute(ADD_CLIENT, (username, password, name, surname, email, telephone_number, date.today()))
    connection.commit()
    return errors.OK


def check_username_in_db(username: str, cursor) -> int:
    cursor.execute(CHECK_EQ_USERNAME, username)
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.USERNAME_ALREADY_EXIST
    return errors.OK


def check_email_in_db(email: str, cursor) -> int:
    cursor.execute(CHECK_EQ_EMAIL, email)
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.EMAIL_ALREADY_EXIST
    return errors.OK


def check_telephone_number_in_db(telephone_number: str, cursor) -> int:
    cursor.execute(CHECK_EQ_TELEPHONE_NUMBER, telephone_number)
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.TELEPHONE_NUMBER_ALREADY_EXIST
    return errors.OK