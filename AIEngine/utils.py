import re
import string
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

import nltk

from notes.models import Note
nltk.download('wordnet')

from django.core.cache import cache
import logging

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])


def preprocess_text(text):
    
    doc = nlp(text)
    keywords = [token.lemma_ for token in doc if not token.is_stop and token.pos_ in ('NOUN', 'PROPN', 'VERB', 'ADJ') and not token.is_punct]
    
    return list(set(keywords))

def strip_html_tags(input_string):
    
    html_tag_pattern = re.compile('<.*?>')
    cleaned = html_tag_pattern.sub('', input_string)
    
    cleaned = cleaned.replace('&nbsp;', ' ')
    cleaned = cleaned.replace('&amp;', '&')
    cleaned = cleaned.replace('&lt;', '<')
    cleaned = cleaned.replace('&gt;', '>')
    cleaned = cleaned.replace('&quot;', '"')
    cleaned = cleaned.replace('&apos;', "'")
    cleaned = cleaned.replace('&#39;', "'")
    cleaned = cleaned.replace('&#34;', '"')
    cleaned = cleaned.replace('\n', ' ')
    cleaned = ' '.join(cleaned.split())
    return cleaned

def strip_prompt(prompt, content):
    try:
        start_index = content.index(prompt) + len(prompt)
    except ValueError:
        start_index = 0
    return content[start_index:].strip()

def get_preprocessed_content(note: Note):
    try:
        cache_key = f"preprocessed_{note.pk}"
        preprocessed_content = cache.get(cache_key)

        if not preprocessed_content or note.updated_at > cache.get(f"{cache_key}_timestamp", note.updated_at):
            note_content = strip_html_tags(note.content)
            preprocessed_content = preprocess_text(note_content)

            cache.set(cache_key, preprocessed_content, None)        # None timeout means it's cached forever
            cache.set(f"{cache_key}_timestamp", note.updated_at, None)

        return preprocessed_content
    except Exception as e:
        logging.error(f"Error occurred while preprocessing content: {e}")
        return None

def preprocess_group_content(note):
    
    # Basic cleanup, HTML strip, lowering cases
    text = re.sub(r'<[^>]+>', '', note.content) 
    text = text.lower()  
    text = text.translate(str.maketrans('', '', string.punctuation)) 

    # Tokenization and more advanced processing like stemming/lemmatization
    stop_words = set(stopwords.words('english')) - {'over', 'under', 'more', 'most', 'such'}
    word_tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    filtered_sentence = [lemmatizer.lemmatize(w) for w in word_tokens if not w in stop_words]

    return ' '.join(filtered_sentence)
