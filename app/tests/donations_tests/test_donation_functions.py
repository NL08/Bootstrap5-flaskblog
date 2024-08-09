from app.app import app
from app.payment.functions import add_foreign_key


def test_adding_foreign_key(yield_email_db, username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form):
    with app.test_request_context():     
        email_db = yield_email_db(username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form)
        assert add_foreign_key(email_db) == 'success'


def test_not_adding_foreign_key(yield_nonexistent_email_form, username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form):
    with app.test_request_context():     
        nonexistent_email_form = yield_nonexistent_email_form(username_form, hashed_password_form, email_form, item_name_form, price_of_donation_form)
        print(add_foreign_key(nonexistent_email_form))
        assert add_foreign_key(nonexistent_email_form) == None










    
 

