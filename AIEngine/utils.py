from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

import nltk
nltk.download('punkt')
nltk.download('stopwords')

import logging
import spacy
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nlp = spacy.load('en_core_web_sm')

""" Data Preprocessing Methods """
def preprocess_text(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(lemmatized)

def strip_html_tags(input_string):
    html_tag_pattern = re.compile('<.*?>')
    return html_tag_pattern.sub('', input_string)

def perform_topic_modeling(notes):
    processed_notes = [preprocess_text(note) for note in notes]

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(processed_notes)

    lda = LatentDirichletAllocation(n_components=5)  
    lda.fit(X)

    feature_names = vectorizer.get_feature_names_out()
    for topic_idx, topic in enumerate(lda.components_):
        print(f"Topic #{topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))  

def preprocess_and_extract_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words]
    return keywords

def extract_keywords(text):
    doc = nlp(text)
    return [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]

def extract_vocabulary(text):
    doc = nlp(text)
    vocab = set()
    for token in doc:
        if token.pos_ in ["NOUN", "VERB", "ADJ"] and not token.is_stop:
            vocab.add(token.lemma_)
    return vocab
