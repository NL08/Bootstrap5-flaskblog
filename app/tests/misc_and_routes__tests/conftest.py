import pytest
from app.app import app
from app import db
from app.tests.models import UserTest

@pytest.fixture
def valid_username_form():    
    username_form = 'fkpr[kfkuh'
    return username_form



from argon2 import PasswordHasher
@pytest.fixture
def valid_hashed_password_form():    
    plaintext_password_form = 'pojkp[kjpj[pj'
    ph = PasswordHasher()
    hashed_password_form  = ph.hash(plaintext_password_form)
    return hashed_password_form


import os 


@pytest.fixture 
def valid_email_form(): 
    email_form = os.environ['TESTING_EMAIL_USERNAME']
    return email_form 




@pytest.fixture
def valid_yield_user_db(): 
    '''
    add the 1 table UserTest. This fixture doesn't work for querying
    '''
    # with app.test_request_context(): # = with app.app_context() except won't work for pytest
    with app.test_request_context(): 
        bind_key="testing_app_db"
        def _subfunction(valid_username_form, valid_hashed_password_form, valid_email_form):
            # Create the databases and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=valid_username_form, hashed_password=valid_hashed_password_form, email=valid_email_form)
            db.session.add(usertest_db)
            db.session.commit()
            return valid_email_form
        # yield unlike return doesn't stop when called.
        yield _subfunction 

        db.drop_all(bind_key)     

