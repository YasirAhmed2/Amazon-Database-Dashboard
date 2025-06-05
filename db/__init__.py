import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="amazon",
        user="yasir2",
        port = "32768",
        password="uiop12345"
    )
