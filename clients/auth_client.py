from datetime import datetime, timedelta, timezone
from jwt import encode
from pydantic import BaseModel
from settings.settings_for_connect import CONNECTION
from requests_to_db.client_requests import CHECK_EQ_USERNAME, CHECK_EQ_PASSWORD
from utils.errors import ERROR, OK
from utils.encrypt_funcs import check_eq_hash
from fastapi import HTTPException
from settings.encrypt_settings import ACCESS_TIME, SECRET_KEY, ALGORITHM_HASH, LEVEL_ENCRYPT
from fastapi.security import OAuth2PasswordBearer
from utils.encrypt_funcs import encrypt_text

auth = OAuth2PasswordBearer(tokenUrl="token")

connection = CONNECTION
cursor = connection.cursor()


def auth_client(form_data):
    if not find_client_username_in_db(form_data.username):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    if not check_password(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    return Token(access_token=access_token, token_type="bearer")



def find_client_username_in_db(username: str):
    username = encrypt_text(username, LEVEL_ENCRYPT)
    cursor.execute(CHECK_EQ_USERNAME, (username, ))
    if cursor.fetchone()[0] == 0:
        return ERROR
    return OK


def check_password(username: str, input_password: str):
    username = encrypt_text(username, LEVEL_ENCRYPT)
    cursor.execute(CHECK_EQ_PASSWORD, (username, ))
    plain_password = cursor.fetchone()[0]
    if not check_eq_hash(input_password, plain_password):
        return ERROR
    return OK
