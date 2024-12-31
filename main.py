# Подключенные библиотеки
from typing import Annotated
from fastapi import FastAPI, HTTPException, Response, Request
# from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from clients.register_new_client import add_client
from clients.funcs_for_clients import all_clients, find_client
from clients.auth_client import auth_client
from utils.errors import OK
from clients.client_settings import Client

# Создание приложения
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="templates/static"), name="static")


# Ручка для главной страницы
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@app.get("/register_page")
async def register_page(request: Request):
    return templates.TemplateResponse(request=request, name='registration.html')

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
