from settings.settings_for_connect import CONNECTION
from requests_to_db.client_requests import FIND_CLIENT, ALL_CLIENTS

connection = CONNECTION
cursor = connection.cursor()

def find_client(username: str):
    cursor.execute(FIND_CLIENT, username)
    result = dict()
    saver = dict()
    result_from_db = cursor.fetchone()
    arr_names = ["id", "username", "password", "name", "surname", "email", "telephone_number", "date"]
    for i in range(len(arr_names)):
        saver[arr_names[i]] = result_from_db[i]
    result[0] = saver
    return result

def all_clients():
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
    return result
