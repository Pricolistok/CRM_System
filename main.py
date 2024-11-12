from fastapi import FastAPI
from types_of_users import Client

app = FastAPI()

clients = []

@app.get("/")
async def all_clients() -> list:
    return clients

@app.post('/add_new_clients')
async def add_user(username: str, name: str, surname: str, email: str, password: str, telephone_number: str):
    new_client = Client(username=username, name=name, surname=surname, email=email, password=password, telephone_number=telephone_number)
    clients.append(new_client)


