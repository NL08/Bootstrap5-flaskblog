'''
Summary:

Part 1) Verify the email exists in the VefifyEmailForm then redirect to where you type in the token.
Part 2) Verify the token exists in the TokenForm then redirect to where you type in the password. (An email is sent with the token)
Part 3) Type in the new password and now you have a new password.
'''

from flask import Blueprint, flash, redirect, render_template, url_for
from app import db
# used because I want to render login route
from app.email_password_reset.forms import VefiryEmailForm, TokenForm, ResetPasswordForm 
from app.models import User, RouteToken
# from __init__.py
from sqlalchemy import delete  
from app.email_password_reset.functions import \
check_expired_token, wait_max_thirty_min_for_new_token, reset_attempts_token_tried_to_0 \
,send_route_token_email, send_password_reset_token_email
from datetime import datetime

email_password_reset = Blueprint('email_password_reset', __name__, template_folder='templates')
#todo add attempts token tried
#todo better


''' Part 1) '''
 
#todo change token_db to token_route/route_token
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
        flash('An email has been sent.')
        flash('Please click on a link in your email to continue the password resetting process.')
        send_route_token_email(user_db, route_name='/verify_email_token')
        return redirect(url_for('main.home'))
    
    return render_template('verify_email.html', title='reset password', form=form) 

'''
Part 2)
'''

# todo better wording
# is route_token needed in the route. 
@email_password_reset.route('/verify_email_token/<username_db>/<token_db>', methods = ['GET', 'POST']) 
def verify_email_token(username_db, token_db):      
    '''
    functions checks the verification token then redirects you to the password
    '''
    # check if the forms match/exist
    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    route_token_db = db.one_or_404(db.select(RouteToken).filter_by(token=token_db)) 
    token_db = route_token_db.token
    if route_token_db.check_expired_route_token() == False:
        db.session.execute(delete(RouteToken).where(RouteToken.token == token_db))
        flash('Your token has expired. Please click resend email for a new email.')
        # if the route_token is expired redirect to the route  becasue the process needs to restart
        return redirect(url_for('email_password_reset.verify_email'))
 
    if route_token_db.email_token == None:
        flash('A token has been sent to your email. Please follow the instructions in your email.' )
        # send email. 
        # The email gives you a token for the form + will redirect to you 'confirmation.registration_verification_code/route_token'        
        # user_db.registration_confirmation_email is currently False:
        send_password_reset_token_email(user_db, route_token_db)
                
    form = TokenForm()  
    if form.validate_on_submit():
        email_token_db = route_token_db.email_token 
        token_form = form.email_token.data

        # check if the email token from the db and the token_form match
        if email_token_db != token_form: # need a more secure way to compare
            # I am only deleting the token because I want the token to be able to be expired.
            db.session.execute(delete(RouteToken).where(RouteToken.email_token == route_token_db.email_token))
            db.session.execute(delete(RouteToken).where(RouteToken.time_token_expired == route_token_db.time_token_expired))
            flash('Your token did not match the one sent to your email.') 
            return render_template('verify_email_token.html', title='verify_email_token', form=form, user_db=user_db, route_token_db=route_token_db)
        
        check_expired_token(route_token_db, now=datetime.now())
        # is this secure
        if wait_max_thirty_min_for_new_token(route_token_db=route_token_db, now=datetime.now()) == 'will redirect to email_password_reset route': 
            return redirect(url_for('email_password_reset.route.verify_email_token', username_db=username_db, token_db=route_token_db.token))
        # is this secure        
        elif reset_attempts_token_tried_to_0(route_token_db=route_token_db, now=datetime.now()) == 'going to redirect to login':
            return redirect(url_for('auth.login'))
        
        else:
            # everything is correct 
            route_token_db.email_token = None
            route_token_db.time_token_expired = None
            route_token_db.attempts_token_tried = 0
            db.session.commit()
            
            # delete route_token + send a new email with a new token
            db.session.execute(delete(RouteToken).where(RouteToken.token == token_db))
            send_route_token_email(user_db, route_name='/reset_password')
            flash('An email has been sent.')
            flash('Please click on a link in your email to continue the password resetting process.')
            return redirect(url_for('main.home'))
    
    return render_template('verify_email_token.html', title='verify_email_token', form=form, user_db=user_db, route_token_db=route_token_db.token)



 
@email_password_reset.route('/resend_password_reset_token/<username_db>/<token_db>', methods = ['GET', 'POST']) 
def resend_password_reset_token(username_db, token_db):    

    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))  
    route_token_db = db.one_or_404(db.select(RouteToken).filter_by(token=token_db))
    token_db = route_token_db.token

    if route_token_db.check_expired_route_token() == False:
        db.session.execute(delete(RouteToken).where(RouteToken.token == token_db))
        flash('Your token has expired. Please click resend email for a new email.')
        # if the token is expired redirect to the route below becasue the process needs to restart
        return redirect(url_for('email_password_reset.verify_email'))
   
    check_expired_token(route_token_db, now=datetime.now())
    # is this secure
    if wait_max_thirty_min_for_new_token(route_token_db=route_token_db, now=datetime.now()) == 'will redirect to email_login_confirmation route': 
        return redirect(url_for('email_password_reset.route.verify_email_token', username_db=username_db, token_db=route_token_db.token))
    # is this secure        
    elif reset_attempts_token_tried_to_0(route_token_db=route_token_db, now=datetime.now())== 'going to redirect to login':
        return redirect(url_for('auth.login'))
    else:
        flash('A token has been sent to your email. Please follow the instructions in your email.' )
        send_password_reset_token_email(user_db, route_token_db)
        return redirect(url_for('email_password_reset.verify_email_token', username_db=username_db, route_token_db=route_token_db))



'''part 3'''


'''Delete request_reset_password.html'''
from argon2 import PasswordHasher
# This route is triggered after you clicked on the send_reset_password_email in your email account
# create form for password field and confirm password
# should I add a token to the route?
@email_password_reset.route("/reset_password/<username_db>/<token_db>", methods = ['GET', 'POST'])
def reset_password(username_db, token_db):

    user_db = db.one_or_404(db.select(User).filter_by(username=username_db))    
    route_token_db = db.one_or_404(db.select(RouteToken).filter_by(token=token_db)) 
    if route_token_db.check_expired_route_token() == False:
        db.session.execute(delete(RouteToken).where(RouteToken.token == token_db))
        flash('Your token has expired. Please click resend email for a new email.')
        return redirect(url_for('email_password_reset.verify_email'))

    form = ResetPasswordForm()    
    if form.validate_on_submit():
        plaintext_password_form = form.password.data
        confirm_plaintext_password_form = form.confirm_password.data
        #check if password is the same as before?        
        ph = PasswordHasher()
        hashed_password_form = ph.hash(plaintext_password_form)
        user_db.hashed_password = hashed_password_form
        db.session.commit()
        # delete the token so you can't enter this route again.
        db.session.execute(delete(RouteToken).where(RouteToken.token == token_db))
        flash('you have changed your password successfully')
        return redirect(url_for('main.home')) 

    return render_template('reset_password.html', title='reset password', form=form) 

















