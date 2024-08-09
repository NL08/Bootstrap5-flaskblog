import pytest, os
from argon2 import PasswordHasher

from app import db
from app.tests.models import UserTest as User
from app.app import app
import time_machine
import datetime as dt


@pytest.fixture
def username_form():    
    username_form = 'fkpr[kfkuh'
    return username_form

@pytest.fixture
def hashed_password_form():    
    plaintext_password_form = 'pojkp[kjpj[pj'
    ph = PasswordHasher()
    hashed_password_form  = ph.hash(plaintext_password_form)
    return hashed_password_form

@pytest.fixture 
def email_form(): 
    email_form = os.environ['TESTING_EMAIL_USERNAME']
    return email_form 
 
@pytest.fixture  
def create_token_form():
    email_tokentest_form = User.create_token()
    return email_tokentest_form

@pytest.fixture
@time_machine.travel("2016-04-23 14:33 +0000")
def time_token_expired_form():
    # add time_token_expired
    current_time_plus_30_minutes = dt.datetime.strptime('04/23/2016 14:30', '%m/%d/%Y %H:%M')
    time_token_expired_form = current_time_plus_30_minutes
    return time_token_expired_form


@pytest.fixture
def attempts_token_tried_form_equal_to_1_form():
    attempts_token_tried = 1
    return attempts_token_tried
 

@pytest.fixture 
def attempts_token_tried_form_equal_to_5_form():
    attempts_token_tried = 5
    return attempts_token_tried 



@pytest.fixture
def yield_just_usertest_db(): 
    '''
    add the table UserTest + return usertest
    attempts_token_tried = 1

    '''
    # with app.test_request_context(): # = with app.app_context() except won't work for pytest
    with app.test_request_context(): 
        bind_key="testing_app_db"
        def _subfunction(username_form, hashed_password_form, email_form):
            # Create the databases and the database table
            db.create_all(bind_key)
            usertest_db = User(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()
            
            usertest_db = db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none()
            if usertest_db is None:
                print('user_db is none')            
            return usertest_db
        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 









 
#@pytest.fixture
#def yield_usertest_db_2(): 
#    '''
#    add the 2 tables UserTest + VerificationEmailTokenTest + return usertest
#    attempts_token_tried = 5
#    '''
    # with app.test_request_context(): # = with app.app_context() except won't work for pytest
#    with app.test_request_context(): 
#        bind_key="testing_app_db"
#        def _subfunction(username_form, hashed_password_form, email_form, email_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_5_form):
            # Create the databases and the database table
#            db.create_all(bind_key)
#            usertest_db = User(username=username_form, hashed_password=hashed_password_form, email=email_form)
#            db.session.add(usertest_db)
#            db.session.commit()
            
#            usertest_db = db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none()
#            if usertest_db is None:
#                print('user_db is none')
            
#            auth_tokentest_db = VerificationEmailToken(email_token=email_token_form, time_token_expired=time_token_expired_form, attempts_token_tried=attempts_token_tried_form_equal_to_5_form,
#                usertest_id=usertest_db.id)
#           db.session.add(auth_tokentest_db)
#            db.session.commit()
        
#            return usertest_db
        # yield unlike return doesn't stop when called.
#        yield _subfunction 
#        db.drop_all(bind_key) 






