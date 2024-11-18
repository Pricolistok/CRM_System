from utils.settings_for_connect import CONNECTION
from requests_to_db.client_requests import CHECK_EQ_USERNAME, CHECK_EQ_PASSWORD
from utils.errors import ERROR, OK

connection = CONNECTION
cursor = connection.cursor()

def find_client_username_in_db(username: str):
    cursor.execute(CHECK_EQ_USERNAME, username)
    if cursor.fetchone()[0] == 0:
        return ERROR
    return OK

def check_password(username: str, password: str):
    cursor.execute(CHECK_EQ_PASSWORD, username)
    if cursor.fetchone()[0] == password:
        return OK
    return ERROR
