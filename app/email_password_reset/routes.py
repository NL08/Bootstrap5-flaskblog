 
'''
Summary:

Part 1) Verify the email exists in the VefifyEmailForm then redirect to where you type in the token.
Part 2) Verify the token exists in the TokenForm then redirect to where you type in the password. (An email is sent with the token)
Part 3) Type in the new password and now you have a new password.
'''

from flask import Blueprint, flash, redirect, render_template, url_for
from app import db
# used because I want to render login route
from app.auth.forms import LoginForm
from app.email_password_reset.forms import VefiryEmailForm, TokenForm, ResetPasswordForm # todo check tokenform
from app.models import User
from flask_mail import Message
# from __init__.py
from app import mail
from sqlalchemy import delete
from app.email_login_confirmation.functions import create_token_db, count_attempts_token_tried, create_time_token_db \
, check_expired_token, wait_max_thirty_min_for_new_token, reset_attempts_token_tried_to_0
from datetime import datetime


email_password_reset = Blueprint('email_password_reset', __name__, template_folder='templates')




#todo add attempts token tried
#todo better


''' Part 1) '''
 

# need a better name
def send_route_token_1_email(user_db): # should I move this and rename it ? Probably
    '''
    send email to your email account with a route_token. 
    This function is in the /verify_email method
    '''
    # better name 
    route_token_1 = user_db.create_route_token()
    user_db.route_token_1 = route_token_1 
    db.session.commit()
    
    route_token_1_db = user_db.route_token_1

    # count_attempts_token_tried(user_db) # replace with a different count and variable here one here 
    # todo maybe add salt not sure if it is needed
    subject='Here is the route token/'
    sender=("do_not_reply@example.com")
    recipients = [user_db.email]

    subject=subject
    sender=sender
    recipients = recipients
    
    msg = Message(subject, sender=sender, recipients=recipients)
    
    msg.html = f'''
    <h2> 
        Please click on the link to be redirected to the new route.
        {url_for('email_password_reset.reset_token', username_db=user_db.username, route_token_1_db=route_token_1_db)}
    </h2>
    '''
    mail.send(msg)


@email_password_reset.route('/verify_email', methods = ['GET', 'POST']) 
def verify_email():
    '''redirected here from forgot password link'''
    form = VefiryEmailForm()   
    if form.validate_on_submit():
        email_form = form.email.data 
        user_db = db.session.execute(db.select(User).filter_by(email=email_form)).scalar_one_or_none() 
        if user_db.email is None:  
            flash("Your email doesn't match. Please try again") 
            return render_template('verify_email.html', title='reset password', form=form)        
        # todo add if try to many emails add attempts_email_tried to db
        send_route_token_1_email(user_db)
        return redirect(url_for('main.home'))
    
    return render_template('verify_email.html', title='reset password', form=form) 

'''
Part 2)

Send the email and a fill out the token form. 
Now you can login because you clicked on the confirmation_email and it is true in the db. 
'''

def send_registration_token_email(user_db): # should I move this and rename it ? Probably
    '''
    send email to your email account with a token. 
    This function is in the /registration_verification_code/<username_db>/<route_token>
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
    
    msg.html = render_template('_send_registration_token_email.html', username_db=user_db.username, email_token_db=email_token_db)
    mail.send(msg)


# need a better name
def send_route_token_2_email(user_db): # should I move this and rename it ? Probably
    '''
    send email to your email account with a route_token. 
    This function is in the /verify_email method
    '''
    # need a better name
    route_token_2 = user_db.create_route_token()
    user_db.create_route_token = route_token_2
    db.session.commit()
    # count_attempts_token_tried(user_db) # replace with a different count and variable here one here 
    # todo maybe add salt not sure if it is needed
    route_token_2_db = user_db.create_route_token
    
    subject='Here is the route token/'
    sender=("do_not_reply@example.com")
    recipients = [user_db.email]

    subject=subject
    sender=sender
    recipients = recipients
    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = f'''
    <h2> 
        Please click on the link to be redirected to reset your password.
        {url_for('email_password_reset.reset_password', username_db=user_db.username, route_token_db=route_token_2_db)}
    '''
    mail.send(msg)

# todo better wording
# is route_token needed in the route. 
@email_password_reset.route('/verify_email_token/<username_db>/<route_token_1_db>', methods = ['GET', 'POST']) 
def verify_email_token(username_db, route_token_1_db):      
    '''
    functions checks the verification token then redirects you to the password
    '''
    # check if the forms match/exist
    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    user_db = db.one_or_404(db.select(User).filter_by(route_token_1=route_token_1_db)) 
 
    check_if_expired_token = User.check_expired_route_token(route_token_1_db)
    if check_if_expired_token == False:
        db.session.execute(delete(User).where(User.route_token_1 == user_db.route_token_1))
        flash('The token is expired. Please try a new token.')
        # if the token is expired redirect to the route below becasue the process needs to restart
        return redirect(url_for('verify_email'))

    # registration_confirmation_email is True + prevents you from registering twice.  
    if user_db.registration_confirmation_email == True:        
        form = LoginForm()
        flash('You have already registered. Please Login.')
        return render_template('login.html', title='login', form=form, error=None)
 
    # This only runs before the VerificationEmailToken table exists for a user
    if user_db == None:
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
            return render_template('registration_verification_code.html', title='registration login code', form=form, user_db=user_db)
        
        check_expired_token(user_db, now=datetime.now())
        wait_max_thirty_min_for_new_token(user_db, now=datetime.now())
        reset_attempts_token_tried_to_0(user_db, now=datetime.now())
        db.session.commit()
        # everything is correct 
        db.session.execute(delete(User).where(User.email_token == user_db.email_token))
        db.session.execute(delete(User).where(User.time_token_expired == user_db.time_token_expired))           
        attempts_token_tried_db = 0
        db.session.commit()
        
        # delete and send a new email with a new token
        db.session.execute(delete(User).where(User.time_token_expired == user_db.time_token_expired))
        send_route_token_2_email(user_db)

        return redirect(url_for('main.home'))
    
    return render_template('verify_email_token.html', title='verify_email_token', form=form, user_db=user_db)



# is route_token needed in the route?   
@email_password_reset.route('/resend_token/<username_db>/<route_token_1_db>', methods = ['GET', 'POST']) 
def resend_token(username_db, route_token_1_db):    

    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    user_db = db.one_or_404(db.select(User).filter_by(route_token_1=route_token_1_db))
 
    check_if_expired_token = User.check_expired_route_token(route_token_1_db)
    if check_if_expired_token == False:
        db.session.execute(delete(User).where(User.route_token_1 == user_db.route_token_1))
        flash('The token is expired. Please try a new token.')
        # if the token is expired redirect to the route below becasue the process needs to restart
        return redirect(url_for('verify_email'))

    # registration_confirmation_email is True + prevents you from registering twice.  
    if user_db.registration_confirmation_email == True:        
        form = LoginForm()
        flash('You have already registered. Please Login.')
        return render_template('login.html', title='login', form=form, error=None)
    
    check_expired_token(user_db, now=datetime.now())
    wait_max_thirty_min_for_new_token(user_db, now=datetime.now())
    reset_attempts_token_tried_to_0(user_db, now=datetime.now())    
    
    send_registration_token_email(user_db) 
    return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username, email_token_db=user_db.route_token))


'''part 3'''


#''' todo change to reset_token rename password_resete_password_token and the .html file'''
#'''todo add token to the route '''
# should I make the route more secure by adding a token to the route?
#@email_password_reset.route("/reset_token/<username_db>/<route_token>", methods = ['POST', 'GET'])
#def reset_token(username_db, route_token):

#    User.verify_route_token(route_token) 
#    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
#    flash("An email has been sent with instructions to your email to reset the password") 
#     send_token_email(user_db)
#     form = TokenForm()   
#     if form.validate_on_submit():
        # todo turn into a function for forms.py?
#         email_token = user_db.create_token()    
#         checking_verify_token = User.verfiy_email_token(email_token)
        # if the token is expired etc
#         if checking_verify_token != True:
            # delete email_token and random_email_salt

#            return redirect(url_for('auth.login'))
#         token_form = form.token.data
#         shortened_email_token = email_token[-5:]
#         if shortened_email_token != token_form: 
#             raise ValidationError('Your token did not match the one sent to your email. Please check your email for the code.') 
        # if the token matches the form redirect      
#         first_route_token = route_token 
#         second_route_token = user_db.create_route_token()
#         if first_route_token != second_route_token: 
#             raise ValidationError('Try a different token.') 

#         User.verify_route_token(second_route_token)  
#         token_route = second_route_token              
#         return redirect(url_for('email_password_reset.reset_password',username_db = user_db.username, token_route=token_route))
#     return render_template('reset_token.html', title='reset token', form=form, username_db=user_db.username)



'''Delete request_reset_password.html'''
from argon2 import PasswordHasher
# This route is triggered after you clicked on the send_reset_password_email in your email account
# create form for password field and confirm password
# should I add a token to the route?
@email_password_reset.route("/reset_password/<username_db>/route_token_2_db", methods = ['GET', 'POST'])
def reset_password(username_db, route_token_2_db):

    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))    
    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))    
 
    check_if_expired_token = User.check_expired_route_token(route_token_2_db)
    if check_if_expired_token == False:
        db.session.execute(delete(User).where(User.route_token_2 == user_db.route_token_2))
        flash('The token is expired. Please try a new token.')
        return redirect(url_for('verify_email'))

    form = ResetPasswordForm()    
    if form.validate_on_submit():

        plaintext_password_form = form.password.data
        confirm_plaintext_password_form = form.confirm_password.data
        #check if password is the same as before?
        user_db = user_db.username
        user_db = db.session.execute(db.select(User).filter_by(username=user_db)).scalar_one_or_none()            
        if not user_db:  
            flash('This is an invalid or expired token')
            return redirect(url_for('email_password_reset.reset_password', username_db=user_db.username))     
        
        ph = PasswordHasher()
        hashed_password_form = ph.hash(plaintext_password_form)
        user = User(hashed_password=hashed_password_form)
        db.session.add(user)
        db.session.commit()

        # delete the token so you can't enter this route again.
        db.session.execute(delete(User).where(User.route_token_2 == user_db.route_token_2))
        flash('you have changed your password successfully')
        return redirect(url_for('main.home')) 

    return render_template('reset_password.html', title='reset password', form=form) 

















