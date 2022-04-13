#This is a test script to ensure we are accessing and grabbing the credentials from Secret Manager

from secrets_manager_test import get_secret_test

FLASK_SECRET_KEY     = get_secret_test() # using AWS secrets manager
print (f'The type of FLASK_SECRET_KEY is = ')
print (type(FLASK_SECRET_KEY))
print (f'The OBJECT = ')
print(FLASK_SECRET_KEY)
print ('The string is ')
flask_key = FLASK_SECRET_KEY['FLASK_SECRET_KEY'] #calling the dictionary entry
print (flask_key)
