ADD_CLIENT = '''
    INSERT INTO clients (username, password, name, surname, email, telephone_number, date_of_birth)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
'''
FIND_CLIENT = '''
    SELECT * FROM  clients WHERE username=%s;
'''
CHECK_EQ_USERNAME = '''
    SELECT COUNT(*) FROM clients WHERE username=%s;
'''

ALL_CLIENTS = '''
    SELECT * FROM  clients;
'''

CHECK_EQ_EMAIL = '''
    SELECT COUNT(*) FROM clients WHERE email=%s;
'''

CHECK_EQ_TELEPHONE_NUMBER = '''
    SELECT COUNT(*) FROM clients WHERE telephone_number=%s;
'''

CHECK_EQ_PASSWORD ='''
    SELECT password FROM clients WHERE username=%s;
'''
