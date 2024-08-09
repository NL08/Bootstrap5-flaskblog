from datetime import datetime, timezone
from flask_login import UserMixin
from app import db
from itsdangerous.url_safe import URLSafeTimedSerializer

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so




#user_mixin still used?
class User(UserMixin, db.Model):
    '''
    one to many relationship between both tables.
    The One relationship.
    '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # unique blocks the same username
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table    
    username: so.Mapped[str] = so.mapped_column(sa.String(80), index=True, unique=True)
    hashed_password:  so.Mapped[str] = so.mapped_column(sa.String(128)) 
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    registration_confirmation_email: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    profile_pic_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String())
    '''Might not be needed'''
    #route_salt:  so.Mapped[Optional[str]] = so.mapped_column(sa.String())
    route_token_1: so.Mapped[Optional[str]] = so.mapped_column(sa.String())   
    route_token_2: so.Mapped[Optional[str]] = so.mapped_column(sa.String()) 
  
    # used to be VerificationEmailToken
    email_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String())    
    time_token_created: so.Mapped[Optional[datetime]] = so.mapped_column(index=True)
    time_token_expired: so.Mapped[Optional[datetime]] = so.mapped_column(index=True)
    route_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String()) 
    attempts_token_tried: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    # relationship connects the tables.
    #rel_verification_email_token: so.WriteOnlyMapped["VerificationEmailToken"] = so.relationship(back_populates="rel_user")  
    rel_posts: so.WriteOnlyMapped['Posts'] = so.relationship(back_populates='rel_user')
    rel_payments: so.WriteOnlyMapped['Payments'] = so.relationship(back_populates='rel_user')

    '''Might not be needed'''
    #def create_route_salt(self):  
    #    adding_salt = secrets.token_hex(3)
    #    return adding_salt 

    # should I rename this create_email_token?
    def create_route_token(self):  
        SECRET_KEY = 'temp_secret_key'
        salt = self.random_email_token_salt
        serializer = URLSafeTimedSerializer(SECRET_KEY),# salt)
        # random number
        data_to_serialize = {'user_id': self.id} 
        print(f'data_to_serialize={data_to_serialize['user_id']}')
        # 30 minutes
        token = serializer.dumps(data_to_serialize['user_id']) # Add a timestamp to ensure uniqueness
        return token    
    
    # Will max_age work?
    def check_expired_route_token(self):
        '''If the route_token expired make it False else True. '''
        SECRET_KEY = 'temp_secret_key' 
        # salt = self.random_salt
        serializer = URLSafeTimedSerializer(SECRET_KEY)#, salt)
        try:
            # remove max-age when using pytest
            serializer.loads(self.route_token, max_age=1800)
        except Exception:
            # print("An exception occurred:", e)
            # Re-raise the caught exception
            return False
        print('The token works')
        return True

    def __repr__(self):
        return '<User {}>'.format(self.username)





#class VerificationEmailToken(UserMixin, db.Model):
#    id: so.Mapped[int] = so.mapped_column(primary_key=True)
#    email_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String())    
#    time_token_created: so.Mapped[Optional[datetime]] = so.mapped_column(index=True)
#    time_token_expired: so.Mapped[Optional[datetime]] = so.mapped_column(index=True)
#    attempts_token_tried: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
#    route_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String()) 
#    fk_user_id: so.Mapped[int] = so.mapped_column(ForeignKey(User.id))
#    rel_user: so.Mapped["User"] = so.relationship(back_populates="rel_verification_email_token")

#   def __repr__(self):
#        return '<VerificationEmailToken {}>'.format(self.email_token)



class Posts(UserMixin, db.Model):

    '''
    one to many relationship between both databases.
    This is the Many relationship.
    '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(120))
    content: so.Mapped[str] = so.mapped_column(sa.String(120))
    # Everyone sees the same time based on daylight savings.  
    date_posted: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    '''
    When using the foreign key colmun use the name of the column of the other table except an lowercase and end it with _id.
    # The foreign key creates  an column called user.id. This links the two tables. 
    IOW the foreign key is the primary key just in another table.
    # user.id represents the id from the User database. 
    '''
    # If I have the Posts table and want a value from the user table to Posts.user.id.username?
    fk_user_id: so.Mapped[int] = so.MappedColumn(sa.ForeignKey('user.id'))
    rel_user: so.Mapped['User'] = so.relationship(back_populates='rel_posts')
    
    def __repr__(self):
        return '<Posts {}>'.format(self.content)



# if a user has an account the user will connect to the db if not it is not required.
class Payments(UserMixin, db.Model):
    '''
    One to many relationship
    This is the Many relationship. 
    '''
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    item_name: so.Mapped[str] = so.mapped_column(sa.String(80))
    price_of_donation: so.Mapped[int] = so.mapped_column(sa.Integer)
    # How do I turn email into the foreign key? todo.
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    fk_user_id: so.Mapped[Optional[int]] = so.MappedColumn(sa.ForeignKey('user.id')) 
    rel_user: so.Mapped['User'] = so.relationship(back_populates='rel_payments')
    
    def __repr__(self):
        return '<Payments {}>'.format(self.email)
    





















#from datetime import datetime
#from flask_login import UserMixin
#from app import db
#from itsdangerous.url_safe import URLSafeTimedSerializer


#class User(UserMixin, db.Model):
#    '''
#    one to many relationship between both tables.
#    The One relationship.
#    '''
#    id = db.Column(db.Integer, primary_key=True)
    # unique blocks the same username
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table
#    username = db.Column(db.String(80), unique=True)
#    hashed_password = db.Column(db.String(128))
#    email = db.Column(db.String(120), unique=True)
#    registration_confirmation_email = db.Column(db.Boolean, default=False)       
#    profile_pic_name = db.Column(db.String())
    # relationship connects the tables.
    # db.relationship first argument is named after the many table. This creates a relationship between the 2 tables.
    # What does lazy do?
    # The value of backref allows to get a value from the other table?
#    rel_posts = db.relationship('Posts', backref='profileinfo', lazy=True)
#    rel_payments = db.relationship('Payments', backref='donationinfo', lazy=True)       
        
    # Will this create 2 different tokens?
#    def create_token(self):    
#        SECRET_KEY = 'temp_secret_key' 
#        salt = 'your-salt create env variable'
#        serializer = URLSafeTimedSerializer(SECRET_KEY, salt)
#        data_to_serialize = {'user_id': 'self.id'} 
        # 30 minutes
#        token = serializer.dumps(data_to_serialize)        
#        return token
    
#    @staticmethod
#    def verify_token(token):
#        SECRET_KEY = 'temp_secret_key' 
#        salt = 'your-salt create env variable'
#        serializer = URLSafeTimedSerializer(SECRET_KEY, salt)
#        try:
            # remove max-age when using pytest
#            token_verify = serializer.loads(token)
#            return token_verify
#        except:
#            print('The token has expired or the token does not exist.') # better wording   
#            return None


 
    
   
#    def __repr__(self):
#        return '<User {}>'.format(self.username)



#class Posts(UserMixin, db.Model):
#    '''
#    one to many relationship between both databases.
#    This is the Many relationship.
#    '''

#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(120), nullable=False)
#    content = db.Column(db.String(120), nullable=False) 
#    # Everyone sees the same time based on daylight savings.  
#    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#    '''
#    When using the foreign key colmun use the name of the column of the other table except an lowercase and end it with _id.
    # The foreign key creates  an column called user.id. This links the two tables. 
#    IOW the foreign key is the primary key just in another table.
    # user.id represents the id from the User database. 
#    '''

    # If I have the Posts table and want a value from the user table to Posts.user.id.username?
#    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

#    def __repr__(self):
#        return '<Posts {}>'.format(self.content)



# if a user has an account the user will connect to the db if not it is not required.
#class Payments(db.Model):
#    '''
#    One to many relationship
#    This is the Many relationship. 
#    '''
#    id = db.Column(db.Integer, primary_key=True)
#    item_name = db.Column(db.String(80))
#    price_of_donation = db.Column(db.Integer)
    # How do I turn email into the foreign key? todo.
#    email = db.Column(db.String(120))
#    fk_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
#    def __repr__(self):
#        return '<Payments {}>'.format(self.email)
    

