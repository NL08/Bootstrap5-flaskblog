# functions for routes.py 
from wtforms.validators import ValidationError
 
import os
current_config = os.environ['FLASK_ENV']
# allow different imports so the code works during pytest + None pytest
if os.environ['FLASK_ENV']  == 'dev':
    from app.models import User  
elif os.environ['FLASK_ENV'] == 'test': 
    from app.tests.models import UserTest as User 
   
from app import db  
from app.models import User, RouteToken
from flask_mail import Message      
from flask import flash, url_for, render_template, redirect
from datetime import timedelta, datetime
from sqlalchemy import delete
import secrets
from app import mail

 


'''functions in routes.py below''' 

def create_token_db(route_token_db):
    '''create the token and add it to the db'''
    created_email_token = secrets.token_hex(3)
    route_token_db.email_token = created_email_token
    db.session.commit()
    # add token to db

def count_attempts_token_tried(route_token_db):
    # turn this part into its own function
    route_token_db.attempts_token_tried += 1
    db.session.commit()
    # flash(route_token_db.attempts_token_tried ) # remove after testing.


# now is added because of pytest + now represents the current time     
def create_time_token_db(route_token_db, now): 
    '''create the time the token expires and add it to the db'''
    current_time = now
    # add time_token_expired
    thirty_min = timedelta(minutes=30)
    current_time_plus_30_minutes = current_time + thirty_min 
    route_token_db.time_token_expired = current_time_plus_30_minutes
    db.session.commit()

    
# now is added because of pytest + now represents the current time     
def check_expired_token(route_token_db, now):
    ''' 
    check if the max token expires and the max_emails has not been exceeded 
    and wait till next email that has a token. 
    '''    
    time_token_expired_db = route_token_db.time_token_expired
    current_time = now


    # current 12:00
    # expired token 12 33
    # ex token created at 9:33pm and token expires at 9:30pm. 
    # Wait until the token expires to let the user get more emails.
    #  needed "attempts_token_tried_db <= 5"?
    if current_time > time_token_expired_db and route_token_db.attempts_token_tried <= 5:
        # should I just create a new function for pytest?
        db.session.execute(delete(User).where(User.email_token == route_token_db.email_token))
        db.session.execute(delete(User).where(User.time_token_expired == route_token_db.time_token_expired))
        # only works during pytest
        print('check_expired_token, success')
        flash('Your token has expired. Please click resend email for a new email.')
        
        

# now is added because of pytest + now represents the current time  
# is this secure?            
def wait_max_thirty_min_for_new_token(route_token_db, now): 
    '''
    Wait a max of 30 min before getting the last emailed token.
    This only happens when creating the last token. 
    '''
    time_token_expired_db = route_token_db.time_token_expired 
    # executes at 9:00 <= 9:30pm
    current_time = now 
    if route_token_db.attempts_token_tried >= 5 and current_time <= time_token_expired_db:
        # only works duringb pytest
        print('wait_max_thirty_min_for_new_token, success')
        # create times for the created token + expired token
        # better wording.
        flash('You have requested to many tokens. Please wait 30 minutes for a new token from when you recieved youe last token.')
        # is this secure?   
        return 'will redirect to email_password_reset route'
        #Todo add this to the route  return redirect(url_for('email_password_reset.verify_email_token', username_db=user_db.username, token_db=token_db))



# now is added because of pytest + now represents the current time     
# is this secure? 
def reset_attempts_token_tried_to_0(route_token_db, now):
    '''
    if the max attempts of the token tried is exceeded + the 
    token is expired reset the attwempts_token_tried to 0.
    '''
    # why doesn't work
    time_token_expired_db = route_token_db.time_token_expired
    # executes at 9:00 <= 9:30pm
    current_time = now

    if route_token_db.attempts_token_tried >= 5 and current_time >= time_token_expired_db:
        # should I just create a new function for pytest?  
        route_token_db.email_token = None
        route_token_db.time_token_expired = None
        route_token_db.attempts_token_tried = 0
        db.session.commit()

        # change to print     
        flash('You have waited long enough for a new a token. Please login again and you will be sent a email with instructions before you can login.')
        # redirect to login so I won't redirect /resend_token/<username_db> click on the link and a email is sent automatically. 
        # is this secure? 
        return 'going to redirect to login'


# change locations where I listed the functions in .


'''in end_registration_token_email '''
# create_token_db
# count_attempts_token_tried
# create_time_token_db

'''in the post request for registration_verification_code and resend_token routes '''
# check_expired_token
# wait_max_thirty_min_for_new_token
# reset_attempts_token_tried_to_0
# check_max_emails_tried



''' end of functions in routes.py'''












# Used in 2 different routes
# need a better name
def send_route_token_email(user_db, route_name): # should I move this and rename it ? Probably
    '''
    send email to your email account with a route_token. 
    This function is in the /verify_email + /reset_password
    '''
    # uses User id when creating the route token
    route_token = RouteToken.create_route_token(user_db)
    add_columns = RouteToken(token=route_token, fk_user_id=user_db.id)
    db.session.add(add_columns)
    db.session.commit()

    route_token_db = db.session.execute(db.select(RouteToken).where(RouteToken.token==route_token)).scalar_one_or_none()
    token_db = route_token_db.token 



    # # replace with a different count and variable here one here 
 
    subject='Here is the route token.'
    sender=("do_not_reply@example.com")
    recipients = [user_db.email]

    subject=subject
    sender=sender
    recipients = recipients
    
    msg = Message(subject, sender=sender, recipients=recipients)

    # is this secure?
    if route_name == '/verify_email_token': 
        url = url_for('email_password_reset.verify_email_token', username_db=user_db.username, token_db=token_db, _external=True)
    elif route_name == '/reset_password': 
        url = url_for('email_password_reset.reset_password', username_db=user_db.username, token_db=token_db, _external=True)
    else:
        flash('Something has gone wrong')
        return redirect(url_for('main.home'))

    msg.html = f'''
    <html>
        <body>
            <h2> 
                Please click on the link to be redirected to the new route to continue the process of resetting your password.
                <a href="{url}" target="_blank" >{url}</a>    
            </h2>
        </body>
    </html>
'''
    mail.send(msg)


def send_password_reset_token_email(user_db, route_token_db): # should I move this and rename it ? Probably
    '''
    send email to your email account with a token for a form. 
    This function is in the /verify_email_token/<username_db>/<route_token> route
    '''
    create_token_db(route_token_db)
    count_attempts_token_tried(route_token_db)
    create_time_token_db(route_token_db, now=datetime.now())

    subject='Here is the token for the email'
    sender=("do_not_reply@example.com")
    recipients = [user_db.email]
    # fixxxxxxxxxxxxxxxxxxxxxx!
    email_token_db = route_token_db.email_token 

    subject=subject
    sender=sender
    recipients = recipients
    msg = Message(subject, sender=sender, recipients=recipients)
    
    msg.html = render_template('_send_password_reset_token_email.html', username_db=user_db.username, token_db=route_token_db.token, email_token_db=email_token_db)
    mail.send(msg)


def check_if_email_is_not_in_db(form, field):
    '''
    if the username and email is in the db the code works,
    if not it raises an ValidationError.
    The if statement checks if the query is empty/has no values in db.
    '''
    email_form = field.data
    # if empty list [] return True 
    # I want the username and email to to both be negative because I am using an username or an email to login
    if not db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none():
        raise ValidationError('The email does not exist. Please retype your email.')   




# Don't check passwords seperatly for security reasons!         
from argon2 import PasswordHasher 
def compare_hashed_passwords(hashed_password_db, plaintext_password_form):
    '''   
    Compares the hashed_password in the db and plaintext password form.
    ph.verify(...) returns True if it matches and returns False if it doesn't match.  
    '''
    ph = PasswordHasher()
    verify_password = ph.verify(hashed_password_db, plaintext_password_form)
    return verify_password
    
 
     













 