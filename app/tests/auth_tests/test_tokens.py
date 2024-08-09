import pytest
from datetime import datetime, timedelta
import time_machine

'''todo fix'''
#from itsdangerous import SignatureExpired
#def test_token(time_machine, valid_yield_token_and_verify_token, username_form, hashed_password_form, email_form):
               
#    user_db, token, verify_token = valid_yield_token_and_verify_token(username_form, hashed_password_form, email_form)        
#    assert user_db != None

#    print(f'The token_1 is = {token}')   
#    print(f'The token is {type(token)}')    
    #assert token != None


 
    #urrent_time = datetime.now()
    #past_current_time = (datetime.now() + timedelta(hours=12)).time()
    #print(past_current_time)




    
    #with travel(datetime(1985, 10, 26), tick=True):
    #with travel(current_time_plus_30_min, tick=True):


    #with time_machine.travel(0, tick=False) as traveller:
    #    time_machine.move_to(current_time)
    #    assert verify_token == True
    #    time_machine.shift(110000)
    #    with pytest.raises(Exception):
    #        verify_token

 


   


#def test_max_age_behavior():
#    max_age = timedelta(days=7)  # max_age set to 7 days for this example
#    past_time_within_max_age = datetime.now() - max_age + timedelta(days=1)
#    past_time_exceeding_max_age = datetime.now() - max_age - timedelta(days=1)

#    with time_machine.travel(past_time_within_max_age):
        # The function should return True as we're within max_age
#        assert function_to_test() == True

        # Move time forward to exceed max_age
        
        # The function should now return False as we've exceeded max_age
#        assert function_to_test() == False





 
    

 
    
