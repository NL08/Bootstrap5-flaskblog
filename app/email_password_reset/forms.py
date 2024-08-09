from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields import StringField ,EmailField
from wtforms.validators import DataRequired, EqualTo, Length

from app.email_password_reset.functions import check_if_email_is_in_db, compare_hashed_passwords


class VefiryEmailForm(FlaskForm):
    '''
    This is in the /verify_email route
    The form is the token 
    '''
    email = EmailField('Email', validators=
    [
    DataRequired('Email is required'),
    # Is the line below useful
    Length(min=4, max=25, message='Must be between 4 and 25 characters'),
    check_if_email_is_in_db
    ])    

class TokenForm(FlaskForm):
    '''
    This is in the /registration_verification_code route
    The form is the token 
    '''
    token = StringField('Token', validators=
    [
    DataRequired(message='Token is required'),
    Length(min=5, max=5 , message='The token must be 5 characters'),
    ])
 
class EmptyForm(FlaskForm):
    pass 

class ResetPasswordForm(FlaskForm):
    '''
    This is in the /reset_password/<token> route
    The forms are password and confirm_password
    '''
    password = PasswordField('Password', 
    [
        DataRequired('Password is required'),
        validators.Length(min=4, max=25),
        EqualTo('confirm_password', message='The password field is not equal to the confirm password field'),
        compare_hashed_passwords
    ])
     
    submit = SubmitField('Submit')
 
    
    confirm_password = PasswordField('Confirm Password', 
    [
        DataRequired('Password is required'),
        validators.Length(min=4, max=25)
    ]) 
    submit = SubmitField('Submit')


     

