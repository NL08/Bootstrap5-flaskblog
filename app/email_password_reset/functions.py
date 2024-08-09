# functions for routes.py 
from wtforms.validators import ValidationError
 
import os
current_config = os.environ['FLASK_ENV']
# allow different imports so the code works during pytest + None pytest
if os.environ['FLASK_ENV']  == 'dev':
    from app.models import User  
elif os.environ['FLASK_ENV'] == 'test': 
    from app.tests.models import UserTest as User 
   
     

from app import db  



def check_if_email_is_in_db(form, field):
    '''
    if the username and email is in the db the code works,
    if not it raises an ValidationError.
    The if statement checks if the query is empty/has no values in db.
    '''
    email_form = field.data
    # if empty list [] return True 
    # I want the username and email to to both be negative because I am using an username or an email to login
    if not db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none():
        raise ValidationError('The email does not exist. Please retype your email.')   


# Don't check passwords seperatly for security reasons!         
from argon2 import PasswordHasher 
def compare_hashed_passwords(hashed_password_db, plaintext_password_form):
    '''   
    Compares the hashed_password in the db and plaintext password form.
    ph.verify(...) returns True if it matches and returns False if it doesn't match.  
    '''
    ph = PasswordHasher()
    verify_password = ph.verify(hashed_password_db, plaintext_password_form)
    return verify_password
    









 