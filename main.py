from fastapi import FastAPI
from datetime import date

# from types_of_users import Client
from requests_to_db import ADD_CLIENT
from settings_for_connect import CONNECTION

app = FastAPI()
connection = CONNECTION


@app.get("/")
async def all_clients() -> str:
    return 'OK'

@app.post('/add_new_clients')
async def add_user(username: str, name: str, surname: str, email: str, password: str, telephone_number: str):
    cursor = connection.cursor()
    cursor.execute(ADD_CLIENT, (username, password, name, surname, email, telephone_number, date.today()))
    connection.commit()


