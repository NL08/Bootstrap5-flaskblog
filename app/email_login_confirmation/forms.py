from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length



 
class EmptyForm(FlaskForm):
    pass 



class TokenForm(FlaskForm):
    '''
    This is in the /registration_verification_code route
    The form is the token 
    '''
    email_token = StringField('Token', validators=
    [
    DataRequired(message='Token is required'),
    Length(min=6, max=6 , message='The token must be 6 characters')
    ])
   

