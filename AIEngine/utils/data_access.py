# Functions for accessing and retrieving data from your database or external sources.
import sqlite3

def get_db_connection(db_path):
    
    conn = sqlite3.connect(db_path)
    return conn

def fetch_notes(conn):
    """Fetches notes from the database."""
    cursor = conn.cursor()
    
    # Adjust the query according to your table and column names
    query = "SELECT note_text FROM your_table_name"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Convert query results to a list of notes
    notes = [row[0] for row in rows]
    return notes