import psycopg2
from settings import db_host, db_port, db_user, db_password, db_database

connection = psycopg2.connect(
    host=db_host,
    port=db_port,
    user=db_user, 
    password=db_password, 
    database=db_database)

cursor = connection.cursor()

def store_image(key, image):
    cursor.execute("CREATE TABLE image (uid integer PRIMARY KEY, data bytea);")
    cursor.execute("INSERT INTO image VALUES (%s, %s)", (key, image))

    connection.commit()
