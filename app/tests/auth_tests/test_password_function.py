from collections import namedtuple

import pytest
from app.app import app
from wtforms.validators import ValidationError

from app.auth.forms import LoginForm
from app.auth.functions import make_password_contain_capital, make_password_contain_number, compare_hashed_passwords 


# form=field and should not return a validation error when used in a function
@pytest.fixture
def plaintext_password_contains_capital_number_special_char_form():
    field = namedtuple('field', ['data'])
    password_form = field('eejfpwo;Afkj4eo;')
    return password_form

# form=field and should return a validation error when used in a function
@pytest.fixture
def does_not_contain_plaintext_password_contains_capital_number_special_char_form():
    field = namedtuple('field', ['data'])
    password_form = field('aaaaaaaaaaaaaa')
    return password_form                      


def test_password_with_capital_do_not_raise_validation_error(plaintext_password_contains_capital_number_special_char_form):
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form
        contains_capital = make_password_contain_capital(form, field)     
        #print(f'test_password_with_capital_do_not_raise_validation_error output is = {make_password_contain_capital}')
        assert contains_capital == 'success'    

def test_password_with_capital_raise_validation_error(does_not_contain_plaintext_password_contains_capital_number_special_char_form):
    with app.test_request_context(): 
        form = LoginForm()
        field = does_not_contain_plaintext_password_contains_capital_number_special_char_form
        #print(f'test_password_with_capital_do_not_raise_validation_error output is = {make_password_contain_capital}')
        with pytest.raises(ValidationError, match=r"Please include a capital letter in the password field"):
            raise make_password_contain_capital(form, field) 
        
        


def test_password_with_number_do_not_raise_validation_error(plaintext_password_contains_capital_number_special_char_form):  
    with app.test_request_context(): 
        form = LoginForm()
        field = plaintext_password_contains_capital_number_special_char_form 
        assert make_password_contain_number(form, field) == 'success' 


    


def test_password_with_number_raise_validation_error_1(does_not_contain_plaintext_password_contains_capital_number_special_char_form):  
    with app.test_request_context(): 
        form = LoginForm()
        field = does_not_contain_plaintext_password_contains_capital_number_special_char_form
        with pytest.raises(ValidationError, match=r"Please include a number in the password field"):
            raise make_password_contain_number(form, field) 

@pytest.fixture
def correct_plaintext_password_form():    
    '''This form will match the hash function in compare_hashed_passwords'''
    plaintext_password_form = 'pojkp[kjpj[pj'
    return plaintext_password_form

@pytest.fixture
def incorrect_plaintext_password_form():    
    '''This form will not match the hash function in compare_hashed_passwords'''
    plaintext_password_form = 'zzzzzzzzzzzz'
    return plaintext_password_form




def test_compare_hashed_passwords_do_not_raise_validation_error(hashed_password_form, correct_plaintext_password_form):
    verified_hashed_password = compare_hashed_passwords(hashed_password_form, correct_plaintext_password_form)  
    assert verified_hashed_password == True
    


def test_compare_hashed_passwords_raise_validation_error(hashed_password_form, incorrect_plaintext_password_form):
    assert compare_hashed_passwords(hashed_password_form, incorrect_plaintext_password_form) == False


