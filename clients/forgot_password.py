from requests_to_db.client_requests import CHECK_EMAIL
from settings.settings_for_connect import CONNECTION
from clients.check_args import check_email_correct
from utils.errors import OK, EMAIL_NO_REGISTERED, EMAIL_INCORRECT
from settings.encrypt_settings import LEVEL_ENCRYPT
from utils.encrypt_funcs import encrypt_text
import smtplib


cursor = CONNECTION.cursor()

def check_email_for_forgot(email:str):
    if check_email_correct(email) != OK:
        return EMAIL_INCORRECT
    email = encrypt_text(email, LEVEL_ENCRYPT)
    cursor.execute(CHECK_EMAIL, (email, ))
    result = cursor.fetchone()
    if len(result) != 0:
        return OK
    return EMAIL_NO_REGISTERED


def sent_email_for_create_new_pass(email: str):
    smtp = smtplib.SMTP()
