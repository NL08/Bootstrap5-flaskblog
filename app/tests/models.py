
from flask_login import UserMixin
from app import db
from itsdangerous.url_safe import URLSafeTimedSerializer

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime
    
  
class UserTest(UserMixin, db.Model):
    '''
    one to many relationship between both tables.
    The One relationship.
    '''
    #__tablename__ = 'user_test'
    __table_args__ = {'extend_existing': True}  
    __bind_key__ = "testing_app_db"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    # unique blocks the same username
    # I can't have Nullable=False because it will make me add the columns everytime I add a column in User table    
    username: so.Mapped[str] = so.mapped_column(sa.String(80), index=True)
    hashed_password:  so.Mapped[str] = so.mapped_column(sa.String(128)) 
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    registration_confirmation_email: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    profile_pic_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String())

    #  from originally VerificationEmailTokenTest
    email_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String())    
    time_token_expired: so.Mapped[Optional[datetime]] = so.mapped_column()
    attempts_token_tried: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    route_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String()) 

    # relationship connects the tables. 
    rel_payments: so.Mapped['PaymentsTest'] = so.relationship(back_populates='rel_user')
    bind_key = "testing_app_db"

    # should I rename this create_email_token?
    def create_route_token(self):  
        SECRET_KEY = 'temp_secret_key'
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        # random number
        data_to_serialize = {'user_id': self.id} 
        print(f'data_to_serialize={data_to_serialize['user_id']}')
        # 30 minutes
        token = serializer.dumps(data_to_serialize['user_id']) # Add a timestamp to ensure uniqueness
        return token    
    @staticmethod
    # Will max_age work?
    def check_expired_route_token(self, email_token):
        SECRET_KEY = 'temp_secret_key' 
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        try:
            # remove max-age when using pytest
            serializer.loads(email_token, max_age=1800)
        except Exception:
            return False
        print('The token works')
        return True

    def __repr__(self):
        return '<UserTest {}>'.format(self.email)           

#class Verification EmailTokenTest(UserMixin, db.Model):
    
#    __table_args__ = {'extend_existing': True}  
#    __bind_key__ = "testing_app_db"

#    id: so.Mapped[int] = so.mapped_column(primary_key=True)
#    email_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String())    
#    time_token_expired: so.Mapped[Optional[datetime]] = so.mapped_column()
#    attempts_token_tried: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
#    route_token: so.Mapped[Optional[str]] = so.mapped_column(sa.String()) 
    
#    fk_usertest_id: so.Mapped[int] = so.mapped_column(ForeignKey(UserTest.id))
#    rel_user: so.Mapped["UserTest"] = so.relationship(back_populates="rel_verification_email_token")

#    bind_key = "testing_app_db"

#    @staticmethod
#    def create_token():  
#        email_token = secrets.token_hex(3)
#        return email_token
    

#    def __repr__(self):
#        return '<mailTokenTests {}>'.format(self.time_token_expired)
    

# if a user has an account the user will connect to the db if not it is not required.
class PaymentsTest(db.Model):
    '''
    One to many relationship
    This is the Many relationship. 
    '''
    __tablename__ = 'payments_test'
    __table_args__ = {'extend_existing': True}  
    __bind_key__ = "testing_app_db"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    item_name: so.Mapped[str] = so.mapped_column(sa.String(80))
    price_of_donation: so.Mapped[int] = so.mapped_column(sa.Integer)
    # How do I turn email into the foreign key? todo.
    email: so.Mapped[str] = so.mapped_column(sa.String(120), unique=True)
    fk_user_id: so.Mapped[Optional[int]] = so.MappedColumn(sa.ForeignKey(UserTest.id)) 
    rel_user: so.Mapped['UserTest'] = so.relationship(back_populates='rel_payments')

    bind_key = "testing_app_db"

    def __repr__(self):
       return '<PaymentsTest {}>'.format(self.email)
    






