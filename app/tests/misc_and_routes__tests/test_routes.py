import pytest
from app.app import app

@pytest.fixture
def client():
    return app.test_client()

@pytest.fixture
def runner():
    return app.test_cli_runner()


def test_register_page_get(client):
    '''
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (GET) 
    THEN check that the responses are valid 
    '''      
    with app.test_request_context():    
        response = client.get('/register', follow_redirects=True)
        ## Why use a b string? 
        assert response.status_code == 200
        # checks the html for the string register
        assert b'register' in response.data



def test_register_page_post(client): 
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/register requested (POST) 
    THEN check that the responses are valid 
    '''  
    with app.test_request_context():
        response = client.post('/register')
        assert response.status_code == 200
        assert b'register' in response.data

        
    


def test_donations_page_post(client): 
    ''' 
    GIVEN a Flask application configured for testing
    WHEN the '/donations requested (POST) 
    THEN check that the responses are valid 
    '''  
    with app.test_request_context():
        response = client.post('/donations')
        assert response.status_code == 200
        # assert b'donate' in response.data


 
