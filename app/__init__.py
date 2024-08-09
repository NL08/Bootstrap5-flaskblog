from flask import Flask
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

# Setup CSRF protection. This allows html forms to work and be secure
csrf = CSRFProtect()
ckeditor = CKEditor() 
# Make @login_required work
login_manager = LoginManager()
# You get a custom login message when @login_required appears in the code.
login_manager.login_message_category = 'Login is required'
# Should I use auth.login ? What is this?
login_manager.login_view = 'login' 
# setup databases
db = SQLAlchemy()
#for flask migrate
migrate = Migrate()

mail = Mail()


from app.models import User
# This function logs you in and since there is no way of storing it in the database I need the function.
# how does id work in the function below?
@login_manager.user_loader
def load_user(id): 
    return db.session.execute(db.select(User).where(User.id==id)).scalar_one_or_none()


import os
from app.config import DevelopmentConfig, PytestConfig

from app.email_login_confirmation.routes import send_registration_token_email
        
def create_app(): 
    # The function name is from the config file which is "Class config:".
    app = Flask(__name__)
    
    from app.main.forms import SearchForm
    @app.context_processor
    def inject_searchform():
        '''
        Pass Stuff to Navbar such as a form in layout.html from search.html
            
        If I don't pass on the form in base function then I will 
        get an error in layout.html because of {{form.csrf_token}} 
        ''' 
        # The variable name is "searchform" and not "form" because in the html I would have 2 "form" variables
        return dict(searchform=SearchForm()) 
        
    current_config = os.environ['FLASK_ENV']
    if current_config == 'dev':
          app.config.from_object(DevelopmentConfig)
    elif current_config == 'test':
        app.config.from_object(PytestConfig)



    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app) 
    mail.init_app(app)

    # blocks this from pytest. Because I get a weird error when it runs in pytest
    if current_config == 'dev':
        ckeditor.init_app(app)

    # with statement isn't removing the warning
    
    from app.auth.routes import auth
    from app.email_login_confirmation.routes import email_login_confirmation
    from app.email_password_reset.routes import email_password_reset
    from app.main.routes import main
    from app.payment.routes import payment
    from app.postinfo.routes import postinfo
    app.register_blueprint(auth) 
    app.register_blueprint(email_login_confirmation)
    app.register_blueprint(email_password_reset)
    app.register_blueprint(main)
    app.register_blueprint(payment)    
    app.register_blueprint(postinfo)

    return app 








