from AIEngine.services.topic_modeling import perform_topic_modeling
from AIEngine.services.text_processing import extract_keywords
from notes.models import Note, NoteGroup

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import string
import numpy as np
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')

import logging
import spacy

nlp = spacy.load('en_core_web_sm')
from django.utils.timezone import now

""" Data Preprocessing Methods """
def preprocess_text(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
    return " ".join(lemmatized)

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

""" Auto Grouping Methods"""
def compute_similarity_matrix(contents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim


def group_note(target_note, other_notes, similarities, threshold=0.5):
    similar_indices = np.where(similarities > threshold)[0]  # Indices of notes similar to the target note
    similar_notes = [other_notes[i] for i in similar_indices]

    if similar_notes:
        note_group = NoteGroup(title=f"Group for Note {target_note.pk} - {now().strftime('%Y-%m-%d %H:%M:%S')}")
        note_group.save()
        note_group.notes.add(target_note, *similar_notes)
        return note_group

def group_all_notes(notes, similarity_matrix, threshold=0.5):
    note_groups = []
    visited = set()

    for idx, similarities in enumerate(similarity_matrix):
        if idx in visited:
            continue

        similar_indices = np.where(similarities > threshold)[0]
        group = [notes[i] for i in similar_indices if i not in visited]

        visited.update(similar_indices)

        if group:
            note_group = NoteGroup(title=f"Auto Group {len(note_groups) + 1} - {now().strftime('%Y-%m-%d %H:%M:%S')}")
            note_group.save()
            note_group.notes.set(group)
            note_group.save()
            note_groups.append(note_group)

    return note_groups

""" Analysis Methods (Summary, Keywords)"""
def preprocess_and_extract_keywords(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word not in stop_words]
    return keywords

# Create function to make sentence count dynamic based on input size.
def summarize_text_with_lsa(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join([str(sentence) for sentence in summary])
    return summary_text

def analyze(content):
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


