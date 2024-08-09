from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, FileAllowed, FileField, FileRequired
from wtforms import StringField, SubmitField


class FileForm(FlaskForm): 
    '''
    This is in /update_form route.
    The form is image_filename.
    '''
    image_filename = FileField('image_filename', 
    validators=
    [FileRequired() ,FileAllowed(['jpg', 'png'], message='Images only!')  ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    '''
    This is in the '/search' route.
    The form is searched.
    '''   
    search_input = StringField("search", validators=[DataRequired()])
    submit = SubmitField("Submit")


 



    