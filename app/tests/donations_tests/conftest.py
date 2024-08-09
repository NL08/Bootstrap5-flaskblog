import os, pytest
from app.tests.models import UserTest, PaymentsTest



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

@pytest.fixture 
def email_form(): 
    email_form = os.environ['TESTING_EMAIL_USERNAME']
    return email_form 

@pytest.fixture
def item_name_form():
    item_name_form = 'donation'  
    return item_name_form

@pytest.fixture
def price_of_donation_form():    
    '''This price_of_donation_form is for pytest'''
    # equal to 66 cents
    price_of_donation_form = 66
    return price_of_donation_form

from app import db
#from app.tests.models import UserTest, PaymentsTest
from app.app import app

@pytest.fixture
def yield_email_db(): 
    '''
    add the 2 tables UserTest + PaymentsTest then return the email
    '''
    #with app.test_request_context(): # = with app.app_context() except won't work for pytest
    with app.test_request_context(): 
        bind_key="testing_app_db"
        def _subfunction(username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form):
            # Create the databases and the database table
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()
            payment_db = PaymentsTest(item_name=item_name_form, price_of_donation=price_of_donation_form, email=email_form)
            db.session.add(payment_db)
            db.session.commit()
            return email_form 
        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key) 


@pytest.fixture
def yield_nonexistent_email_form():  
    '''
    This is in the test_donations_functions.py  
    Create the UserTest and the PaymentsTest db.
    Then yield the email column and finally delete the db.
    '''
    with app.test_request_context():
        bind_key="testing_app_db"
        def _subfunction(username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form):
            db.create_all(bind_key)
            usertest_db = UserTest(username=username_form, hashed_password=hashed_password_form, email=email_form)
            db.session.add(usertest_db)
            db.session.commit()  
            payment_db = PaymentsTest(item_name=item_name_form, price_of_donation=price_of_donation_form, email=email_form)
            db.session.add(payment_db)
            db.session.commit()
            incorrect_email_form = 'zbkjuhnbuh'
            return incorrect_email_form
        # yield unlike return doesn't stop when called.
        yield _subfunction 
        db.drop_all(bind_key)