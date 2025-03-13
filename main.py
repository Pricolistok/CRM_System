# Подключенные библиотеки
from typing import Annotated
from fastapi import FastAPI, HTTPException, Response
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from clients.register_new_client import add_client
from clients.funcs_for_clients import all_clients
from clients.auth_client import auth_client
from utils.errors import OK
from clients.client_settings import Client
from clients.forgot_password import check_email_for_forgot

# Создание приложения
app = FastAPI()

# Ручка для главной страницы
@app.get("/")
async def root():
    return 'OK'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ручка для регистрации нового пользователя
@app.post("/register_new_client")
async def create_new_client(username: str, password: str, name: str, surname: str, email: str, telephone_number: str):
    client = Client(username, password, name, surname, email, telephone_number)
    if add_client(client) != OK:
        raise HTTPException(status_code=300, detail="Client already exists")
    raise HTTPException(status_code=200, detail="Client registered successfully")

# Функция для авторизации пользователя на площадке
@app.post("/token")
async def login_client(response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    access_token =  auth_client(form_data).access_token
    response.set_cookie(key="users_access_token", value=access_token,  httponly=True)
    return "The Client was logged"

# # Функция для поиска пользователя в БД
# @app.get("/find_client_with_username")
# async def find_client(username: str):
#     return find_client(username=username)

# Функция для вывода данных о всех клиентах из БД
@app.get("/return_all_clients")
async def find_client(token: str = Depends(oauth2_scheme)) -> dict:
    return all_clients()

# @app.put("/forgot_password_check_email")
# async def forgot_password_check_email(email: str):
#     return check_email_for_forgot(email)
#
#
# @app.get("/sent_email_for_new_password")
# async def sent_email(email: str):
    return
