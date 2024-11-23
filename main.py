from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from clients.register_new_client import add_client
from clients.funcs_for_clients import all_clients, find_client
from clients.auth_client import auth_client, Client
from utils.errors import OK

app = FastAPI()


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
    return auth_client(form_data)

@app.get("/find_client_with_username")
async def find_client(username: str):
    return find_client(username=username)


@app.get("/return_all_clients")
async def find_client() -> dict:
    return all_clients()
