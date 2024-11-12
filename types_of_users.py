from pydantic import BaseModel


class Client(BaseModel):
        username: str
        name: str
        surname: str
        email: str
        password: str
        telephone_number: str