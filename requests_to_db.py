ADD_CLIENT = '''
    INSERT INTO clients (username, password, name, surname, email, telephone_number, date_of_birth)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
'''