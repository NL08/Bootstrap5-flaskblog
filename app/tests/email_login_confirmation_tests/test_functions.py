from app.email_login_confirmation.functions import check_expired_token\
,wait_max_thirty_min_for_new_token, reset_attempts_token_tried_to_0 
import datetime as dt
import pytest
from wtforms.validators import ValidationError
import time_machine
from flask import redirect, url_for 
from app.app import app
import sys




'''I might want to change both below to flash + redirect instead of ValidationError because I know how to test this.'''
 
#@time_machine.travel("2016-04-23 14:33")
#def test_check_expired_token(yield_usertest_db_1, username_form, hashed_password_form, email_form, create_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_1_form): 
#    user_db = yield_usertest_db_1(username_form, hashed_password_form, email_form, create_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_1_form)
#    print(user_db)
#    assert user_db != None                                       
#    current_time_plus_33_minutes = dt.datetime.strptime('04/23/2016 14:33', '%m/%d/%Y %H:%M')
#    with pytest.raises(ValidationError, match=r'Your token has expired. Please click resend email for a new email.'):
#        raise check_expired_token(user_db, current_time_plus_33_minutes)
 
#@time_machine.travel("2016-04-23 14:01")
#def test_wait_max_thirty_min_for_new_token(yield_usertest_db_2, username_form, hashed_password_form, email_form, 
#    create_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_5_form):
    
#    user_db = yield_usertest_db_2(username_form, hashed_password_form, email_form, 
#    create_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_5_form)
    
#    '''I am just printing because I am getting an error with ValidationError'''
#    print(user_db)
#    assert user_db != None                                       
#    current_time_plus_1_minute = dt.datetime.strptime('04/23/2016 14:01', '%m/%d/%Y %H:%M')
#    wait_max_thirty_min_for_new_token(user_db, now=current_time_plus_1_minute)
    #with pytest.raises(ValidationError, match=r'Your token has expired. Please click resend email for a new email.'):
    #    raise check_expired_token(user_db, current_time_plus_1_minute)





#def redirect_function_1():    
#    return redirect(url_for('auth.login'))

#def redirect_function_2():    
#    return redirect(url_for('auth.login'))

#@time_machine.travel("2016-04-23 14:33")
#def test_reset_attempts_token_tried_to_0(yield_usertest_db_2, 
#    username_form, hashed_password_form, email_form, 
#    create_token_form, time_token_expired_form, attempts_token_tried_form_equal_to_5_form):

#    user_db = yield_usertest_db_2(username_form, hashed_password_form, email_form, create_token_form, 
#        time_token_expired_form, attempts_token_tried_form_equal_to_5_form)
#    current_time_plus_1_minute = dt.datetime.strptime('04/23/2016 14:33', '%m/%d/%Y %H:%M')
#    reset_attempts_token_tried_to_0(user_db, now=current_time_plus_1_minute)
    
    #with app.test_request_context():
    #    testing_redirect_1 = sys.stdout.write(str(redirect_function_1))
            
    #    testing_redirect_2 = sys.stdout.write(str(reset_attempts_token_tried_to_0(user_db, now=current_time_plus_1_minute)))

    #assert testing_redirect_1 != testing_redirect_2



 




