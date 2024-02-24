# Contains functions and classes related to text processing, such as keyword extraction and text summarization.

import spacy

nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    """Extracts keywords from the given text."""
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]