# functions for routes.py 
from wtforms.validators import ValidationError
import os
current_config = os.environ['FLASK_ENV']
# allow different imports so the code works during pytest + None pytest
if os.environ['FLASK_ENV']  == 'dev':
    from app.models import User
elif os.environ['FLASK_ENV'] == 'test':  
    from app.tests.models import UserTest as User 
if os.environ['FLASK_ENV']  == 'dev':
    from app.models import RouteToken
elif os.environ['FLASK_ENV'] == 'test':  
    from app.tests.models import RouteTokenTest as RouteToken

from app import db        
from flask import flash
from datetime import timedelta
from sqlalchemy import delete
import secrets
from app.email_login_confirmation.forms import TokenForm 

'''functions in routes.py in email_login_confirmation below''' 

def create_token_db(user_db):
    '''create the token and add it to the db'''
    created_email_token = secrets.token_hex(3)
    user_db.email_token = created_email_token
    db.session.commit()
    # add token to db

def count_attempts_token_tried(user_db):
    # turn this part into its own function
    user_db.attempts_token_tried += 1
    db.session.commit()
    # flash(user_db.attempts_token_tried ) # remove after testing.


# now is added because of pytest + now represents the current time     
def create_time_token_db(user_db, now): 
    '''create the time the token expires and add it to the db'''
    current_time = now
    # add time_token_expired
    thirty_min = timedelta(minutes=30)
    current_time_plus_30_minutes = current_time + thirty_min 
    user_db.time_token_expired = current_time_plus_30_minutes
    db.session.commit()

    
# now is added because of pytest + now represents the current time     
def check_expired_token(user_db, now):
    ''' 
    check if the max token expires and the max_emails has not been exceeded 
    and wait till next email that has a token. 
    '''    
    time_token_expired_db = user_db.time_token_expired
    current_time = now


    # current 12:00
    # expired token 12 33
    # ex token created at 9:33pm and token expires at 9:30pm. 
    # Wait until the token expires to let the user get more emails.
    #  needed "attempts_token_tried_db <= 5"?
    if current_time > time_token_expired_db and user_db.attempts_token_tried <= 5:
        # should I just create a new function for pytest?
        db.session.execute(delete(User).where(User.email_token == user_db.email_token))
        db.session.execute(delete(User).where(User.time_token_expired == user_db.time_token_expired))
        # only works during pytest
        print('check_expired_token, success')
        flash('Your token has expired. Please click resend email for a new email.')
        
        

# now is added because of pytest + now represents the current time  
# is this secure?            
def wait_max_thirty_min_for_new_token(user_db, now): 
    '''
    Wait a max of 30 min before getting the last emailed token.
    This only happens when creating the last token. 
    '''
    time_token_expired_db = user_db.time_token_expired 
    # executes at 9:00 <= 9:30pm
    current_time = now 
    if user_db.attempts_token_tried >= 5 and current_time <= time_token_expired_db:
        # only works duringb pytest
        print('wait_max_thirty_min_for_new_token, success')
        # create times for the created token + expired token
        # better wording.
        flash('You have requested to many tokens. Please wait 30 minutes for a new token from when you recieved youe last token.')
        # is this secure?  
        return 'will redirect to email_login_confirmation route'
        

# now is added because of pytest + now represents the current time     
# is this secure? 
def reset_attempts_token_tried_to_0(user_db, now):
    '''
    if the max attempts of the token tried is exceeded + the 
    token is expired reset the attwempts_token_tried to 0.
    '''
    # why doesn't work
    time_token_expired_db = user_db.time_token_expired
    # executes at 9:00 <= 9:30pm
    current_time = now

    if user_db.attempts_token_tried >= 5 and current_time >= time_token_expired_db:
        # should I just create a new function for pytest?  
        user_db.email_token = None
        user_db.time_token_expired = None
        user_db.attempts_token_tried = 0
        db.session.commit()

        # change to print     
        flash('You have waited long enough for a new a token. Please login again and you will be sent a email with instructions before you can login.')
        # redirect to login so I won't redirect /resend_token/<username_db> click on the link and a email is sent automatically. 
        # is this secure? 
        return 'going to redirect to login'

 





'''in end_registration_token_email '''
# create_token_db
# count_attempts_token_tried
# create_time_token_db

'''in the post request for registration_verification_code and resend_token routes '''
# check_expired_token
# wait_max_thirty_min_for_new_token
# reset_attempts_token_tried_to_0
# check_max_emails_tried




 

