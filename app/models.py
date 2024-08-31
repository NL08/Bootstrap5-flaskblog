from datetime import datetime, timezone
from flask_login import UserMixin
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer
from typing import List
from sqlalchemy import ForeignKey
from itsdangerous.url_safe import URLSafeTimedSerializer

from typing import Optional

#todo add many to many

class User(UserMixin, db.Model):
    
    '''
    one to many relationship between 3 tables.
    The One relationship to 2 tables.
    '''

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    # unique blocks the same username etc
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table    
    username: Mapped[str] = mapped_column(String(80), index=True, unique=True)
    hashed_password:  Mapped[str] = mapped_column(String(128)) 
    email: Mapped[str] = mapped_column(String(120), index=True, unique=True)
    registration_confirmation_email: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_pic_name: Mapped[Optional[str]] = mapped_column(String())
    # token and information sent in an email in the email_login_confirmation 
    email_token: Mapped[Optional[str]] = mapped_column(String())    
    time_token_expired: Mapped[Optional[datetime]] = mapped_column(index=True)
    attempts_token_tried: Mapped[int] = mapped_column(Integer, default=0)
    
    # relationship connects the tables.
    #rel_verification_email_token: ["VerificationEmailToken"] = relationship(back_populates="rel_user")  
    rel_route_token: Mapped[List["RouteToken"]] = relationship(back_populates="rel_user")  
    rel_posts: Mapped[List["Posts"]] = relationship(back_populates='rel_user')
    rel_payments: Mapped[List["Payments"]] = relationship(back_populates='rel_user')
 
    def __repr__(self):
        return '<User {}>'.format(self.username)



# class/db in password reset token route
class RouteToken(UserMixin, db.Model):
    ''' one table '''
    id: Mapped[int] = mapped_column(primary_key=True)    
    # route token
    token: Mapped[Optional[str]] = mapped_column(String())   
    # token and information sent in an email in the email_password_reset route
    email_token: Mapped[Optional[str]] = mapped_column(String())    
    time_token_expired: Mapped[Optional[datetime]] = mapped_column(index=True)
    attempts_token_tried: Mapped[int] = mapped_column(Integer, default=0)    

    fk_user_id: Mapped["int"] = mapped_column(ForeignKey('user.id'))
    rel_user: Mapped["User"] = relationship(back_populates='rel_route_token')


    @staticmethod
    def create_route_token(user_db):  
        '''Uses "user_db" for the User's id'''
        SECRET_KEY = 'temp_secret_key'
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        # random number
        data_to_serialize = {'user_id': user_db.id} 
        print(f'data_to_serialize={data_to_serialize['user_id']}')
        # 30 minutes
        token = serializer.dumps(data_to_serialize) 
        return token    
    

    def check_expired_route_token(self):
        '''
        If the route_token expired make it False else True. 
        Uses "user_db" for the User's id
        '''
        
        SECRET_KEY = 'temp_secret_key' 
        serializer = URLSafeTimedSerializer(SECRET_KEY) 
        try:
            serializer.loads(self.token, max_age=1800)
        except Exception: 
            return False
        print('The token works')
        return True

    def __repr__(self):
        return '<User {}>'.format(self.email)



#class VerificationEmailToken(UserMixin, db.Model):
#    id: Mapped[int] = mapped_column(primary_key=True)
#    token: Mapped[Optional[str]] = mapped_column(String())   

#    email_token: Mapped[Optional[str]] = mapped_column(String())    
#    time_token_expired: Mapped[Optional[datetime]] = mapped_column(index=True)
#    attempts_token_tried: Mapped[int] = mapped_column(Integer, default=0)
#    route_token: Mapped[Optional[str]] = mapped_column(String()) 
#    fk_user_id: Mapped["int"] = mapped_column(ForeignKey('user.id'))
#    rel_user: Mapped["User"] = relationship(back_populates='rel_verification_email_token')
#    def __repr__(self):
#        return '<VerificationEmailToken {}>'.format(self.email_token)



class Posts(UserMixin, db.Model):

    '''
    one to many relationship between both databases.
    This is the Many relationship.
    '''
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    content: Mapped[str] = mapped_column(String(120))
    # Everyone sees the same time based on daylight savings.  
    date_posted: Mapped[datetime] = mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    '''
    When using the foreign key colmun use the name of the column of the other table except an lowercase and end it with _id.
    # The foreign key creates  an column called user.id. This links the two tables. 
    IOW the foreign key is the primary key just in another table.
    # user.id represents the id from the User database. 
    '''
    # If I have the Posts table and want a value from the user table to Posts.user.id.username?
    fk_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    rel_user: Mapped["User"] = relationship(back_populates="rel_posts")    

    def __repr__(self):
        return '<Posts {}>'.format(self.content)



# if a user has an account the user will connect to the db if not it is not required.
class Payments(UserMixin, db.Model):
    '''
    One to many relationship
    This is the Many relationship. 
    '''
    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(80))
    price_of_donation: Mapped[int] = mapped_column(Integer)
    # How do I turn email into the foreign key? todo.
    email: Mapped[str] = mapped_column(String(120), unique=True)
    fk_user_id: Mapped[Optional[int]]= mapped_column(ForeignKey("user.id"))
    rel_user: Mapped["User"] = relationship(back_populates="rel_payments")

    
    def __repr__(self):
        return '<Payments {}>'.format(self.email)
    







 


 

