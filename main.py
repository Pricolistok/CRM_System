from fastapi import FastAPI
from datetime import date

from requests_to_db import ADD_CLIENT, CHECK_EQ_USERNAME, FIND_CLIENT, ALL_CLIENTS
from settings_for_connect import CONNECTION

app = FastAPI()
connection = CONNECTION


@app.get("/")
async def all_clients() -> str:
    return 'OK'

@app.post('/add_new_clients')
async def add_user(username: str, name: str, surname: str, email: str, password: str, telephone_number: str):
    cursor = connection.cursor()
    cursor.execute(CHECK_EQ_USERNAME, username)
    result = cursor.fetchone()
    print(len(result))
    if result[0] != 0:
        return 101
    cursor.execute(ADD_CLIENT, (username, password, name, surname, email, telephone_number, date.today()))
    connection.commit()
    return 0

@app.get("/find_client_with_username")
async def find_client(username: str):
    cursor = connection.cursor()
    cursor.execute(FIND_CLIENT, username)
    result = dict()
    saver = dict()
    result_from_db = cursor.fetchone()
    print(result_from_db)
    arr_names = ["id", "username", "password", "name", "surname", "email", "telephone_number", "date"]
    for i in range(len(arr_names)):
        saver[arr_names[i]] = result_from_db[i]
    result[0] = saver
    return result

@app.get("/return_all_clients")
async def find_client() -> dict:
    cursor = connection.cursor()
    arr_names = ["id", "username", "password", "name", "surname", "email", "telephone_number", "date"]
    result = dict()
    saver = dict()
    cursor.execute(ALL_CLIENTS)
    result_from_db = cursor.fetchall()
    for i in range(len(result_from_db)):
        for j in range(len(arr_names)):
            saver[arr_names[j]] = result_from_db[i][j]
        result[i] = saver
        saver = dict()
    print(result)
    return result
