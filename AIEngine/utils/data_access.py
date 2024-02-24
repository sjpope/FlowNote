# Functions for accessing and retrieving data from your database or external sources.
import sqlite3

#TO-DO: Define DB_PATH in settings.py or as environment variable
def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    return conn

