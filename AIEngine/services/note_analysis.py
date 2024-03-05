from AIEngine.utils.data_access import *
from AIEngine.utils.preprocessing import preprocess_text
from AIEngine.services.topic_modeling import perform_topic_modeling
from AIEngine.services.text_processing import extract_keywords
from DataConnector.data_access import getSQL, pushMongoDB

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')

import logging

def preprocess_and_extract_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words]
    return keywords

# Function to summarize text
def summarize_text_with_lsa(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text

def analyze_notes(content):
    processed_notes = preprocess_text(content)  
    logging.debug(f"Processed Notes: {processed_notes}")

    if len(processed_notes.split()) < 25:
        logging.warning("Text too short or insignificant for analysis.")
        return "Text too short or insignificant for analysis."

    # Extract keywords
    keywords = preprocess_and_extract_keywords(processed_notes)
    logging.info(f"Extracted Keywords: {keywords}")

    # Summarize the text
    summary = summarize_text_with_lsa(processed_notes)
    logging.info(f"Summary: {summary}")

    
    keywords_str = ', '.join(keywords)  
    analysis_result = f"Keywords: {keywords_str}\n\nSummary: {summary}"

    # pushMongoDB('NoteData', 'Analysis', analysis_result)
    
    return analysis_result

# def analyze_notes(content):
    
#     processed_notes = preprocess_text(content) 
#     logging.debug(f"Processed Notes: {processed_notes}")

#     if len(processed_notes.split()) < 25:
#         logging.warning("Text too short or insignificant for analysis.")
#         return "Text too short or insignificant for analysis."

#     try:
#         topics = perform_topic_modeling(processed_notes)
#     except ValueError as e:
#         logging.error(f"Error in topic modeling: {str(e)}")
#         return "Failed to analyze topics due to insufficient content."
#     # keywords = [extract_keywords(note) for note in processed_notes]
#     #pushMongoDB( 'NoteData', 'Topics', topics)
#     return topics  
