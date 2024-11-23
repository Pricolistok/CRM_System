from datetime import datetime, timedelta, timezone

from jwt import encode
from pydantic import BaseModel
from settings.settings_for_connect import CONNECTION
from requests_to_db.client_requests import CHECK_EQ_USERNAME, CHECK_EQ_PASSWORD
from utils.errors import ERROR, OK
from utils.encrypt_funcs import check_eq_hash
from fastapi import HTTPException
from settings.encrypt_settings import ACCESS_TIME, SECRET_KEY, ALGORITHM_HASH
from fastapi.security import OAuth2PasswordBearer

auth = OAuth2PasswordBearer(tokenUrl="token")

connection = CONNECTION
cursor = connection.cursor()

class Client(BaseModel):
    username: str
    password: str
    name: str
    surname: str
    email: str
    token: str
    date: datetime

class Token(BaseModel):
    access_token: str
    token_type: str


def auth_client(form_data):
    if not find_client_username_in_db(form_data.username):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    if not check_password(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token=access_token, token_type="bearer")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TIME)
    to_encode.update({"exp": expire})
    return encode(to_encode, SECRET_KEY, ALGORITHM_HASH)


def find_client_username_in_db(username: str):
    cursor.execute(CHECK_EQ_USERNAME, (username, ))
    if cursor.fetchone()[0] == 0:
        return ERROR
    return OK


def check_password(username: str, input_password: str):
    cursor.execute(CHECK_EQ_PASSWORD, username)
    plain_password = cursor.fetchone()[0]
    if not check_eq_hash(input_password, plain_password):
        return ERROR
    return OK
