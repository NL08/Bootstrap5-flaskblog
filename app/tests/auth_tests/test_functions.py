
from collections import namedtuple
import pytest
from app.app import app
from wtforms.validators import ValidationError
from app.auth.forms import LoginForm
from app.auth.functions import check_if_username_or_email_is_in_db


def test_email_in_db(yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):
    usertest_db = yield_usertest_db(username_form_with_same_value_as_email, hashed_password_form, email_form_with_same_value_as_username)
    email_db = str(usertest_db.email)
    assert isinstance(email_db, str)  
    # assert usertest_db.email != None




# is the yield_usertest_db neccessary? I think so.
@pytest.fixture
def valid_username_form_db(yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):
    usertest_db = yield_usertest_db(username_form_with_same_value_as_email, hashed_password_form, email_form_with_same_value_as_username)
    username_db = str(usertest_db.username) 
    field = namedtuple('field', ['data'])
    username_form = field(username_db)
    return username_form


def test_valid_check_if_username_or_email_is_in_db(valid_username_form_db ,yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):  
    # this example will work
    with app.test_request_context(): 
        form = LoginForm()
        field = valid_username_form_db(yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username)
        assert check_if_username_or_email_is_in_db(field, form) == 'success'









