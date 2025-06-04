# db/connection.py

from sqlalchemy import create_engine

def get_engine():
    # Replace with your own credentials
    user = "your_user"
    password = "your_password"
    host = "localhost"
    port = "5432"
    database = "your_db"

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    return engine
