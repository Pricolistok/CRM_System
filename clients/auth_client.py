import jwt
from settings.settings_for_connect import CONNECTION
from requests_to_db.client_requests import CHECK_EQ_USERNAME, CHECK_EQ_PASSWORD
from utils.errors import ERROR, OK
from utils.encrypt_funcs import check_eq_hash
from fastapi import HTTPException
from settings.encrypt_settings import LEVEL_ENCRYPT
from datetime import timedelta, datetime, timezone
from utils.encrypt_funcs import encrypt_text
from clients.client_settings import Token
from settings.jwt_settings import SECRET_JWT_KEY, ALGORITHM_JWT, ACCESS_TOKEN_EXPIRE_MINUTES

connection = CONNECTION
cursor = connection.cursor()

def auth_client(form_data):
    if not find_client_username_in_db(form_data.username):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    if not check_password(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    access_token = create_access_token(data={"sub": form_data.username})
    return Token(access_token, "bearer")



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


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_JWT_KEY, algorithm=ALGORITHM_JWT)
