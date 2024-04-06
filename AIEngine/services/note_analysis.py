from AIEngine.services.topic_modeling import perform_topic_modeling
from AIEngine.services.text_processing import extract_keywords

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

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
import spacy

nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    result = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        result.append(token.lemma_)
    return " ".join(result)

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

    keywords = preprocess_and_extract_keywords(processed_notes)
    logging.info(f"Extracted Keywords: {keywords}")

    summary = summarize_text_with_lsa(processed_notes)
    logging.info(f"Summary: {summary}")

    
    keywords_str = ', '.join(keywords)  
    analysis_result = f"Keywords: {keywords_str}\n\nSummary: {summary}"

    
    return analysis_result


