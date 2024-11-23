from curses.ascii import isdigit
from string import ascii_letters, digits

from utils import errors
from requests_to_db.client_requests import CHECK_EQ_EMAIL, CHECK_EQ_USERNAME, CHECK_EQ_TELEPHONE_NUMBER
import re


def check_username_already_exist(username: str, cursor) -> int:
    cursor.execute(CHECK_EQ_USERNAME, username)
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.USERNAME_ALREADY_EXIST
    return errors.OK

def check_email(email: str, cursor) -> int:
    if not check_email_correct(email):
        return errors.EMAIL_INCORRECT
    print(type(email))
    print(type(email), type(CHECK_EQ_EMAIL))
    cursor.execute(CHECK_EQ_EMAIL, (email,))
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.EMAIL_ALREADY_EXIST
    return errors.OK

def check_email_correct(email: str) -> int:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return errors.OK
    return errors.ERROR


def check_telephone_number(telephone_number: str, cursor) -> int:
    if not check_telephone_correct(telephone_number):
        return errors.TELEPHONE_NUMBER_INCORRECT
    print(type(telephone_number))
    cursor.execute(CHECK_EQ_TELEPHONE_NUMBER, (telephone_number,))
    result = cursor.fetchone()
    if result[0] != 0:
        return errors.TELEPHONE_NUMBER_ALREADY_EXIST
    return errors.OK

def check_telephone_correct(telephone_number: str) -> bool:
    len_telephone_number = len(telephone_number)
    start_check_telephone_number = 2
    if len_telephone_number > 12:
        return errors.ERROR
    elif len_telephone_number < 10:
        return errors.ERROR
    elif len_telephone_number == 12:
        if telephone_number[:2] != '+7':
            return errors.ERROR
    elif len_telephone_number == 11:
        if telephone_number[0] != '7' and telephone_number[0] != '8':
            return errors.ERROR
        telephone_number = '+7' + telephone_number[2:]
    for i in range(start_check_telephone_number, len_telephone_number):
        if not isdigit(telephone_number[i]):
            return errors.ERROR
    return errors.OK


def encrypt_text(data: str):
    alphabet = ascii_letters + digits
    len_alphabet = len(alphabet)
    encrypt_data = ''
    for i in data:
        index = alphabet.index(i)
        if index > len_alphabet - 4:
            index = len_alphabet - index
        encrypt_data += alphabet[index]
    print(encrypt_data)

