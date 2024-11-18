from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from clients.register_new_client import add_client
from clients.funcs_for_clients import all_clients, find_client
from clients.auth_client import find_client_username_in_db, check_password
from utils.errors import OK

app = FastAPI()

auth = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return 'OK'

@app.post("/register_new_client")
async def create_new_client(username: str, password: str, name: str, surname: str, email: str, telephone_number: str):
    if add_client(username, name, surname, email, password, telephone_number) != OK:
        raise HTTPException(status_code=300, detail="Client already exists")
    raise HTTPException(status_code=200, detail="Client registered successfully")

@app.post("/login_client")
async def login_client(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not find_client_username_in_db(form_data.username):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    if not check_password(form_data.username, form_data.password):
        raise HTTPException(status_code=400, detail="Error Authenticating")
    return {"access_token": form_data.username, "token_type": "bearer"}


@app.get("/find_client_with_username")
async def find_client(username: str):
    return find_client(username=username)

@app.get("/return_all_clients")
async def find_client() -> dict:
    return all_clients()
