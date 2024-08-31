from flask import Blueprint, flash, redirect, render_template, url_for, request 
from app import db
# used because I want to render login route
from app.auth.forms import LoginForm
from app.email_login_confirmation.forms import TokenForm 
from app.models import User
from flask_mail import Message
# from __init__.py
from app import mail
from sqlalchemy import delete

from app.email_login_confirmation.functions import create_token_db, count_attempts_token_tried, create_time_token_db \
, check_expired_token, wait_max_thirty_min_for_new_token, reset_attempts_token_tried_to_0
from datetime import datetime



email_login_confirmation = Blueprint('email_login_confirmation', __name__, template_folder='templates')
'''
Summary:

Send the email and a fill out the token form. 
Now you can login because you clicked on the confirmation_email and it is true in the db. 
'''

def send_registration_token_email(user_db): # should I move this and rename it ? Probably
    '''
    send email to your email account with a token. 
    This function is in the /registration_verification_code/<username_db> + the previous route
    '''
    create_token_db(user_db)
    count_attempts_token_tried(user_db)
    create_time_token_db(user_db, now=datetime.now())

    subject='Here is the token for the email'
    sender=("do_not_reply@example.com")
    recipients = [user_db.email]

    email_token_db = user_db.email_token 

    subject=subject
    sender=sender
    recipients = recipients
    msg = Message(subject, sender=sender, recipients=recipients)
  
    msg.html = render_template('_send_confirmation_token_email.html', username_db=user_db.username, email_token_db=email_token_db)
    mail.send(msg)


# todo better wording
# is route_token needed in the route.
# 
@email_login_confirmation.route('/registration_verification_code/<username_db>', methods = ['GET', 'POST']) 
def registration_verification_code(username_db):      
    '''
    functions checks the verification token then adds the confirmation_email to True so you can login
    '''
    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    # registration_confirmation_email is True + prevents you from registering twice.  
    if user_db.registration_confirmation_email == True:        
        form = LoginForm()
        flash('You have already registered. Please Login.')
        return render_template('login.html', title='login', form=form, error=None)
    
     
    # This only runs before user_db.email_token table exists for a user
    if user_db.email_token is None: # not working!!
        flash('A token has been sent to your email. Please follow the instructions in your email.' )
        # send email. 
        # The email gives you a token for the form + will redirect to you 'confirmation.registration_verification_code/route_token'        
        # user_db.registration_confirmation_email is currently False:
        send_registration_token_email(user_db)
        
    form = TokenForm()  
    if form.validate_on_submit():
        email_token_db = user_db.email_token 
        token_form = form.email_token.data

        # check if the email token from the db and the token_form match
        if email_token_db != token_form: # need a more secure way to compare
            # I am only deleting the token because I want the token to be able to be expired.
            db.session.execute(delete(User).where(User.email_token == user_db.email_token))
            db.session.execute(delete(User).where(User.time_token_expired == user_db.time_token_expired))
            flash('Your token did not match the one sent to your email.') 
            flash('Please request a new token.')
            return render_template('registration_verification_code.html', title='registration login code', form=form, user_db=user_db)
        
        check_expired_token(user_db, now=datetime.now())
        # is this secure
        if wait_max_thirty_min_for_new_token(user_db=user_db, now=datetime.now()) == 'will redirect to email_login_confirmation route':
            return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username))
        # is this secure        
        elif reset_attempts_token_tried_to_0(user_db, now=datetime.now())== 'going to redirect to login':
            return redirect(url_for('auth.login'))
        else:
            # if the token matches the form and nothing else is wrong the code below executes
            user_db.registration_confirmation_email = True
            user_db.email_token = None
            user_db.time_token_expired = None
            user_db.attempts_token_tried = 0
            db.session.commit()
            # user_db.registration_confirmation_email is now True
            flash('You can now login.')
            return redirect(url_for('auth.login'))
    
    return render_template('registration_verification_code.html', title='registration login code', form=form, user_db=user_db)

# is route_token needed in the route?   
@email_login_confirmation.route('/resend_login_confirmation_token/<username_db>', methods = ['GET', 'POST']) 
def resend_login_confirmation_token(username_db):    
 
    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    # registration_confirmation_email is True + prevents you from registering twice.  
    if user_db.registration_confirmation_email == True:        
        form = LoginForm()
        flash('You have already registered. Please Login.')
        return render_template('login.html', title='login', form=form, error=None)
    
    check_expired_token(user_db, now=datetime.now())
    # is this secure
    if wait_max_thirty_min_for_new_token(user_db=user_db, now=datetime.now()) == 'will redirect to email_login_confirmation route': 
        return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username))
    # is this secure        
    elif reset_attempts_token_tried_to_0(user_db, now=datetime.now())  == 'going to redirect to login':
        return redirect(url_for('auth.login'))
    else:    
        flash('A token has been sent to your email. Please follow the instructions in your email.' )
        send_registration_token_email(user_db) 
        return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username))



