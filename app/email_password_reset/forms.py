from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, validators
from wtforms.fields import StringField ,EmailField
from wtforms.validators import DataRequired, EqualTo, Length

 
from app.email_password_reset.functions import check_if_email_is_not_in_db
from app.auth.functions import make_password_contain_capital, make_password_contain_number, make_password_contain_special_characters


     
 
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
    check_if_email_is_not_in_db,
    ])    

class TokenForm(FlaskForm):
    '''
    This is in the /registration_verification_code route
    The form is the token 
    '''
    email_token = StringField('Token', validators=
    [
    DataRequired(message='Token is required'),
    Length(min=6, max=6, message='The token must be 5 characters'),
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
        make_password_contain_capital,
        make_password_contain_number,
        make_password_contain_special_characters
    ])
     
 
    confirm_password = PasswordField('Confirm Password', 
    [
        DataRequired('Password is required'),
        validators.Length(min=4, max=25),
        make_password_contain_capital,
        make_password_contain_number,
        make_password_contain_special_characters
    ]) 


    submit = SubmitField('Submit')


     
