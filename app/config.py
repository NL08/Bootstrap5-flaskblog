# used in production config
# REMEMBER_COOKIE_SECURE = True
import os
import stripe

# This gives the path the current folder is in. This is an absolute import. 
# example below
# C:\Users\username\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app
base_directory = os.path.abspath(os.path.dirname(__file__)) 
# DATABASE_URI = sqlite:///test_app.db", this the default path, or 
    # " 'sqlite:///' " + "os.path.join(base_directory, 'test_app.db')" = sqlite:///C:\Users\user\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\test_app.db
Pytest_db_uri = os.environ.get('TEST_DATABASE_URI') or \
    'sqlite:///' + os.path.join(base_directory, 'test_app.db')

from datetime import timedelta


# what does sqlite/// do ?
# what is object ?
class Config(object): 
    # Setup CSRF secret key
    # change to environment variable todo!
    SECRET_KEY = 'temp_secret_key'
    # this is the test key for stripe 
    stripe.api_key = os.environ['STRIPE_SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # setting up Outlook email for flask mail
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    # The max file size is now 16 megabytes.
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000
    # logs you in for 6 min after closing the browser 
    REMEMBER_COOKIE_DURATION = timedelta(seconds=360)
    # DATABASE_URI = sqlite:///app.db, this is the the default path, or 
    # " 'sqlite:///' " + "os.path.join(base_directory, 'app.db')" = sqlite:///C:\Users\user\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\app.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(base_directory, 'app.db')   # correct
    ''' Database For pytest'''
    # for 2+ databases to make the second db work
    SQLALCHEMY_BINDS = { "testing_app_db": Pytest_db_uri }   


 





from pathlib import Path

class DevelopmentConfig(Config):    
    # should it be False? NO.
    DEBUG = True
    # for pytest if True it blocks emails in flask mail from being sent
    TESTING = False    
    # This will be the same value as 'DEBUG = ...' 
    Mail_DEBUG = True  
    # This is the default email that you get when you send an email?
    MAIL_DEFAULT_SENDER = None  
    # You can only send x amount of emails at one time. Can also be set to None.
    MAIL_MAX_EMAILS = 5  
    # same value 'TESTING = ...'. If you are testing your app if you don't want to send emails make it True?
    # ['MAIL_SUPRESS_SEND'] = False 
    # converts the file name to ascii. ascii characters are english characters. (Why use this?)
    MAIL_ASCII_ATTACHMENTS = False 
    # Used to save to the uploaded folder 
    # UPLOAD_FOLDER = r"C:\Users\user\OneDrive\Desktop\flaskcodeusethis\flaskblog2\app\static\profilepictures"
    #UPLOAD_FOLDER = os.path.abspath(base_directory + r"\app\static\profilepictures")
    UPLOAD_FOLDER = Path.cwd().joinpath("app", "static", "profilepictures")
    # max a file can be is 1 megabyte is that big enough? Todo add warning
    MAX_CONTENT_LENGTH = 1024 * 1024
    CKEDITOR_PKG_TYPE = 'standard' 
    # setting up flask mail
    MAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    # app password 
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    # make secret key work in wtf forms
    WTF_CSRF_ENABLED = True


class PytestConfig(Config): 
    DEBUG = False
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = '0' 
    Mail_DEBUG = True  
    # for pytest
    TESTING = True	   
    # This is the same value ['TESTING'] =...
    # If you are testing your app and you don't want to send emails make the value True?
    MAIL_SUPRESS_SEND = True  
    # When this is False wtf_forms is disabled. This makes 'POST' request work for pytest routes.
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    SERVER_NAME = 'localhost'

 