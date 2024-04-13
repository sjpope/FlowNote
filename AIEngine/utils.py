import re
import string
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from django.core.cache import cache

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    
    return " ".join(lemmatized)

def strip_html_tags(input_string):
    
    html_tag_pattern = re.compile('<.*?>')
    
    return html_tag_pattern.sub('', input_string)

def strip_prompt(prompt, content):
    try:
        start_index = content.index(prompt) + len(prompt)
    except ValueError:
        start_index = 0
    return content[start_index:].strip()

def get_preprocessed_content(note):
    
    cache_key = f"preprocessed_{note.pk}"
    preprocessed_content = cache.get(cache_key)

    if not preprocessed_content or note.updated_at > cache.get(f"{cache_key}_timestamp", note.updated_at):
        preprocessed_content = preprocess_text(note.content)
        cache.set(cache_key, preprocessed_content, None)        # None timeout means it's cached forever
        cache.set(f"{cache_key}_timestamp", note.updated_at, None)

    return preprocessed_content

def preprocess_and_extract_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words]
    return keywords
