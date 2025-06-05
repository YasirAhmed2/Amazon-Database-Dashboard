# db/connection.py

from sqlalchemy import create_engine

def get_engine():
    # Replace with your own credentials
    user = "yasir2"
    password = "uiop12345"
    host = "localhost"
    port = "32768"
    database = "amazon"

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    return engine
