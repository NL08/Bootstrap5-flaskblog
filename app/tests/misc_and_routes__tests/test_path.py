# The reason I import base_dir is because I want the path from config.py
from app.config import base_directory


import os 
def test_db_paths():   

    # I am printing all the db paths to see if they are correct 

    print(f'\n\nbase_directory = {base_directory}\n\n')

    Pytest_db_uri = os.environ.get('TEST_DATABASE_URI') or \
    'sqlite:///' + os.path.join(base_directory, 'test_app.db')
    print(f'Pytest_db_uri = {Pytest_db_uri}\n\n')

    # part 1 or part 2 has to work but not both though if both work it is better
    SQLALCHEMY_DATABASE_URI_part_1 = 'sqlite:///' + os.environ.get('DATABASE_URI') 
    print(f'SQLALCHEMY_DATABASE_URI_part_1 = {SQLALCHEMY_DATABASE_URI_part_1}\n\n')

    SQLALCHEMY_DATABASE_URI_part_2 = 'sqlite:///' + os.path.join(base_directory, 'app.db')
    print(f'SQLALCHEMY_DATABASE_URI_part_2 = {SQLALCHEMY_DATABASE_URI_part_2}\n\n')


    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.environ.get('DATABASE_URI') or \
    'sqlite:///' + os.path.join(base_directory, 'app.db')
    print(f'SQLALCHEMY_DATABASE_URI = {SQLALCHEMY_DATABASE_URI}\n\n')
 



 

 