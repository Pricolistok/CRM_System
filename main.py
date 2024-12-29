# Подключенные библиотеки
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from clients.register_new_client import add_client
from clients.funcs_for_clients import all_clients, find_client
from clients.auth_client import auth_client
from utils.errors import OK
from clients.client_settings import Client
# from clients.auth_client import Client

# Создание приложения
app = FastAPI()

# Ручка для главной страницы
@app.get("/")
async def root():
    return 'OK'

# Ручка для регистрации нового пользователя
@app.post("/register_new_client")
async def create_new_client(username: str, password: str, name: str, surname: str, email: str, telephone_number: str):
    client = Client(username, password, name, surname, email, telephone_number)
    if add_client(client) != OK:
        raise HTTPException(status_code=300, detail="Client already exists")
    raise HTTPException(status_code=200, detail="Client registered successfully")

# # Функция для авторизации пользователя на площадке
# @app.post("/login_client")
# async def login_client(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     return auth_client(form_data)

# Функция для поиска пользователя в БД
@app.get("/find_client_with_username")
async def find_client(username: str):
    return find_client(username=username)

# @app.get("/items/me")
# async def item(current_user:  Annotated[Client, ])

# Функция для вывода данных о всех клиентах из БД
@app.get("/return_all_clients")
async def find_client() -> dict:
    return all_clients()
