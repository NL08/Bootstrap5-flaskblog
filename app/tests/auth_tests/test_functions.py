
from collections import namedtuple
import pytest
from app.app import app
from wtforms.validators import ValidationError
from app.auth.forms import LoginForm
from app.auth.functions import check_if_username_already_exists_in_db


def test_email_in_db(yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):
    usertest_db = yield_usertest_db(username_form_with_same_value_as_email, hashed_password_form, email_form_with_same_value_as_username) 
    assert usertest_db.email != None


#todo check if capital 
def test_valid_check_if_username_already_exists_in_db(yield_usertest_db, username_form_with_same_value_as_email, hashed_password_form,  email_form_with_same_value_as_username):  
    #this will raise an validationerror
    with app.test_request_context(): 
        form = LoginForm()
        usertest_db = yield_usertest_db(username_form_with_same_value_as_email, hashed_password_form, email_form_with_same_value_as_username)
        field = namedtuple('field', ['data'])
        field = field(usertest_db.username)
        with pytest.raises(ValidationError, match=r"Please include a capital letter in the password field"):
            raise check_if_username_already_exists_in_db(form, field)


#todo invalid form


