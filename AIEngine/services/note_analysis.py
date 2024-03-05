from AIEngine.utils.data_access import *
from AIEngine.utils.preprocessing import preprocess_text
from AIEngine.services.topic_modeling import perform_topic_modeling
from AIEngine.services.text_processing import extract_keywords
from DataConnector.data_access import getSQL, pushMongoDB

def analyze_notes(content):
    
    processed_notes = preprocess_text(content) 
    topics = perform_topic_modeling(processed_notes)
    # keywords = [extract_keywords(note) for note in processed_notes]
    pushMongoDB( 'NoteData', 'Topics', topics)
    return topics  
