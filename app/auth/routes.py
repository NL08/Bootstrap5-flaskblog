from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

auth = Blueprint('auth', __name__, template_folder='templates')
from argon2 import PasswordHasher 

# import db from __init__.py.
from app import db
from app.auth.forms import RegistrationForm
from app.models import User

@auth.route("/register", methods = ['POST', 'GET'])
def register():
    # if the user is logged in make so they can't go to the register page. 
    # change to @login_required
    if current_user.is_authenticated:
        return redirect(url_for(('main.home')))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        
        username_form = form.username.data
        email_form = form.email.data
        plaintext_password_form = form.password.data
        confirm_plaintext_password_form = form.confirm_password.data
        ph = PasswordHasher()        
        # Hash the password 
        hashed_password_form = ph.hash(plaintext_password_form) 
     
        adding_user = User(username=username_form, email=email_form, hashed_password=hashed_password_form)
        db.session.add(adding_user)
        db.session.commit()
        
        user_db = db.session.execute(db.select(User).filter_by(username=username_form)).scalar_one_or_none() 
        return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username))    
        
    return render_template('register.html',title='register', form=form)

from app.auth.forms import LoginForm
from app.auth.functions import compare_hashed_passwords
@auth.route("/login", methods = ['POST', 'GET'])
def login():
    # change to @login_required
    if current_user.is_authenticated:
        return redirect(url_for('main.home')) 
    
    form = LoginForm()
    # seperate the username_or_email_form into username from db or email from db called user_db 
    if form.validate_on_submit():
        username_or_email_form = form.username_or_email.data

        username_db = db.session.execute(db.select(User).where(User.username==username_or_email_form)).scalar_one_or_none()
        email_db = db.session.execute(db.select(User).where(User.email==username_or_email_form)).scalar_one_or_none()

        if username_db:
            if username_db.username == username_or_email_form:
                user_db = username_db
        elif email_db:
            if email_db.email == username_or_email_form:
                user_db = email_db      


        plaintext_password_form = form.password.data
        # checks if an hashed_password is not an empty field + matches hashed_password in db. 
        hashed_password_db = user_db.hashed_password                
         
        if compare_hashed_passwords(hashed_password_db, plaintext_password_form)== False:
            error = 'The username or email or password do not exist. Please retype your username or email or password.' 
            return render_template('login.html', title='login', form=form, error=error)
        # resend the email if the user didn't click on it by redirecting.
        if user_db.registration_confirmation_email == False:
            # redirect to verify_token 
            # flash ?
            return redirect(url_for('email_login_confirmation.registration_verification_code', username_db=user_db.username))
        
        # remember me makes you logged in for a certain time
        login_user(user_db, remember=True)
        flash('You have logged in successfully') 
        '''                   
        To determine if the URL is relative or absolute, check it with Werkzeug's url_parse() function and then check 
        if the netloc component is set or not. What is netloc?
                    
            next = '/login?next=/index', index is just a route. 
            The 'next' variable can have 3 values

            1st value)
            If the login URL does not have a next argument you will be logged in and redirected to the home page.
            iow's next = '/login?next=/' '.  
                    
            How would the other 2 situations happen?

            2nd value)
            if the user is not logged in and tries to go to a route with @login_required, then for example post/new_post ,
            iow's 'next = login?next=/post/new_post' . (This is relative import).
                
            3rd value)
            To protect from redirect to any other website, in the module it checks if next is relative or full url. 
            if it's full domain then, the user is redirected to home page. 
        '''
        # does this check the current route?
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.home')
        return redirect(next_page)

    return render_template('login.html', title='login', form=form, error=None)



 
@auth.route("/logoff")
@login_required
def logoff():
    logout_user()
    return redirect(url_for('main.home'))
                  


