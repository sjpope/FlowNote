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
import re
from .tasks import *

nlp = spacy.load('en_core_web_sm')
from django.utils.timezone import now

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

""" Auto Grouping Methods"""
def compute_similarity_matrix(contents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(contents)
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

def group_note(target_note, other_notes, similarities, threshold=0.5):
    similar_indices = np.where(similarities > threshold)[0] 
    similar_indices = [int(i) for i in similar_indices]
    similar_notes = [other_notes[i] for i in similar_indices]

    if similar_notes:
        note_group = NoteGroup(title=f"Group for Note {target_note.pk} - {now().strftime('%Y-%m-%d %H:%M:%S')}", owner=target_note.owner)
        note_group.save()
        note_group.notes.add(target_note, *similar_notes)
        return note_group
    
def group_all_notes(notes, similarity_matrix, threshold=0.5, owner=None):
    note_groups = []
    visited = set()

    for idx, similarities in enumerate(similarity_matrix):
        if idx in visited:
            continue

        similar_indices = [int(i) for i in np.where(similarities > threshold)[0]]
        group = [notes[i] for i in similar_indices if i not in visited]

        visited.update(similar_indices)

        if group:
            note_group = NoteGroup(
                title=f"Auto Group {len(note_groups) + 1} - {now().strftime('%Y-%m-%d %H:%M:%S')}",
                owner=owner 
            )
            note_group.save()
            note_group.notes.set(group)
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

# Create function to make sentence count dynamic based on input size.
def summarize_text_with_lsa(text, sentence_count=3):
    
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    summary_text = " ".join([str(sentence) for sentence in summary])
    
    return summary_text

# def summarize_with_gpt2(note_content):
#     prompt = f"Summarize this content: {note_content}"
#     summary = generate_content_task(prompt, num_return_sequences=1)[0]
#     # Remove the original prompt from the summary to clean it up
#     cleaned_summary = remove_prompt_from_content(prompt, summary)
#     return cleaned_summary

# def summarize_with_gpt2(text, model, tokenizer):
#     # Ensure the text is clean and free from HTML tags
#     text = strip_html_tags(text)
    
#     # Craft a more concise prompt for summarization
#     prompt = "Summarize this content succinctly:"
#     inputs = tokenizer.encode_plus(prompt + text, return_tensors='pt', max_length=512, truncation=True)
    
#     # Generate summary with the updated parameters
#     summary_ids = model.generate(
#         inputs['input_ids'],
#         attention_mask=inputs['attention_mask'],
#         max_length=150,
#         min_length=40,
#         length_penalty=2.0,
#         num_beams=5,
#         no_repeat_ngram_size=2,
#         early_stopping=True,
#         pad_token_id=tokenizer.eos_token_id,
#         temperature=0.7,  # Adjust temperature for more deterministic output
#         top_k=50,  # Limits the number of highest probability vocabulary tokens considered for each step
#         top_p=0.95,  # Nucleus sampling: only considers the top p% of the cumulative probability distribution
#         do_sample=True  # Enable sampling to utilize temperature and top_p
#     )

#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     return summary


# def analyze(content, model, tokenizer):
#     processed_notes = preprocess_text(content)  
#     logging.debug(f"Processed Notes: {processed_notes}")

#     if len(processed_notes.split()) < 25:
#         logging.warning("Text too short or insignificant for analysis.")
#         return "Text too short or insignificant for analysis."

#     keywords = preprocess_and_extract_keywords(processed_notes)
#     logging.info(f"Extracted Keywords: {keywords}")

#     # summary = summarize_text_with_lsa(processed_notes)
#     # logging.info(f"Summary (LSA): {summary}\n\n\n")
#     summary_gpt2 = ""
#     try:
#         summary_gpt2 = summarize_with_gpt2(content)
#         logging.info(f"Summary (GPT-2): {summary_gpt2}")
#     except Exception as e:
#         logging.error(f"Error in summarize_with_gpt2: {e}")
#         summary_gpt2 = "Error generating summary with GPT-2."
    
#     keywords_str = ', '.join(keywords)  
#     analysis_result = f"Keywords: {keywords_str}\n\nSummary: {summary_gpt2}"
    
#     return analysis_result


