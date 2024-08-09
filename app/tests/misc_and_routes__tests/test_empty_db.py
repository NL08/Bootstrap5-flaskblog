from app.tests.models import db, UserTest




#def test_token_is_empty_in_db(valid_yield_user_db, valid_username_form, valid_hashed_password_form, valid_email_form):
#    user_db = valid_yield_user_db(valid_username_form, valid_hashed_password_form, valid_email_form)
    #print(f' print email_db = {user_db.email_token}')

#    user_db = db.one_or_404(db.select(UserTest).filter_by(email=valid_email_form))
#    print(f'user_db = {user_db}')
#    assert user_db != None
#    print(f'user_db.email_token = {user_db.email_token}')
#   assert user_db.email_token == None