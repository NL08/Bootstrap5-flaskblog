import pytest
from app.app import app
from app import db
from app.tests.models import UserTest



@pytest.fixture
def username_form():    
    username = 'fkpr[kfkuh'
    return username



from argon2 import PasswordHasher
@pytest.fixture
def hashed_password_form():    
    plaintext_password_form = 'pojkp[kjpj[pj'
    ph = PasswordHasher()
    hashed_password_form  = ph.hash(plaintext_password_form)
    return hashed_password_form


import os 


@pytest.fixture 
def email_form(): 
    email_form = os.environ['TESTING_EMAIL_USERNAME']
    return email_form 


@pytest.fixture
def valid_yield_token_and_verify_token(): 
    '''
    add the 1 table UserTest 
    '''
    # with app.test_request_context(): # = with app.app_context() except won't work for pytest
    with app.test_request_context(): 
        bind_key="testing_app_db"
        def _subfunction(username_form, hashed_password_form, email_form):
            # Create the databases and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()
            user_db = db.session.execute(db.select(UserTest).filter_by(email=email_form)).scalar_one_or_none()
            if user_db is None:
                return print('user_db is none')
            
            token = user_db.create_email_token()
            token_verify = user_db.verify_email_token(token)
            return user_db, token, token_verify  

        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 


@pytest.fixture
def username_form_with_same_value_as_email():    
    '''username and email form are equal to the email'''
    username = os.environ['TESTING_EMAIL_USERNAME']
    return username

import os 
@pytest.fixture 
def email_form_with_same_value_as_username(): 
    '''email and username form are equal to the email'''
    email_form = os.environ['TESTING_EMAIL_USERNAME']
    return email_form 



@pytest.fixture
def yield_usertest_db(): 
    '''
    add the 1 table UserTest 
    '''
    # with app.test_request_context(): # = with app.app_context() except won't work for pytest
    with app.test_request_context(): 
        bind_key="testing_app_db"
        def _subfunction(username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):
            # Create the databases and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form_with_same_value_as_email, hashed_password=hashed_password_form, email=email_form_with_same_value_as_username)
            db.session.add(usertest_db)
            db.session.commit()
            user_db = db.session.execute(db.select(UserTest).filter_by(email=email_form_with_same_value_as_username)).scalar_one_or_none()
            if user_db is None:
                return print('user_db is none')
            return user_db

        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 





