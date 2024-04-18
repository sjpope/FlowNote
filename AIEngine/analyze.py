from notes.models import Note, NoteGroup

from .utils import *
from .config import model, tokenizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import logging
import torch
import numpy as np

from datetime import datetime as dt
from datetime import datetime as dt

def generate_content(prompt, num_return_sequences=1, additional_tokens=500, temperature=0.8, top_k=50, top_p=0.92):
    
    # inputs = tokenizer.encode_plus(input_text, return_tensors='pt', add_special_tokens=True, max_length=512, truncation=True)
    encoding = tokenizer(prompt, return_tensors='pt', truncation=True)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    total_max_length = input_ids.shape[1] + additional_tokens

    with torch.no_grad():
        generated_ids = model.generate(
            
            input_ids=input_ids,
            attention_mask=attention_mask,
            
            # max_new_tokens=100, 
            max_length=total_max_length,
            min_length=input_ids.shape[1] + 20,  
            no_repeat_ngram_size=3,  
            num_return_sequences=num_return_sequences,
            
            temperature=temperature, 
            top_k=top_k,
            top_p=top_p,
            
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    # content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    suggestions = [tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
    return suggestions

""" Analysis Methods (Summary, Keywords)"""

def analyze(content, processed_content):
    
    #if len(processed_content.split()) < 25:
    #     logging.warning("Text too short for analysis.")
    #     return "Text too short for analysis."
    # logging.info(f'Content: {content}\n\nProcessed Content: {processed_content}\n\n')
    keywords = generate_keywords(content, processed_content)
    summary = generate_summary(content)
    # logging.info(f'KEYWORDS\n\n{(keywords)}\n\n')
    # logging.info(f'SUMMARY\n\n{summary}\n\n')
    
    return {
        "keywords": keywords,
        "summary": summary
    }
    
def generate_keywords(note_content, processed_content):
    
    prompt = f"From this list of words: {processed_content} Return only a comma separated list of the most important keywords relevant to this text: {note_content}"
    
    keywords = generate_content(prompt, num_return_sequences=1, additional_tokens=50, temperature=0.5, top_k=20, top_p=0.75)[0]
    keywords = strip_prompt(prompt, keywords)
    
    # TO-DO: Add Post Processing Here in case the model gets any funny ideas.
    
    return keywords

def generate_summary(note_content):
    
    prompt = f"Summarize this content: {note_content}"
    summary = generate_content(prompt, num_return_sequences=1)[0]
    summary = strip_prompt(prompt, summary)
    
    return summary    

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
        note_group = NoteGroup(title=f"Group for Note {target_note.pk} - {dt.now().strftime('%Y-%m-%d %H:%M:%S')}", owner=target_note.owner)
        note_group = NoteGroup(title=f"Group for Note {target_note.pk} - {dt.now().strftime('%Y-%m-%d %H:%M:%S')}", owner=target_note.owner)
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
                title=f"Auto Group {len(note_groups) + 1} - {dt.now().strftime('%Y-%m-%d %H:%M:%S')}",
                owner=owner 
            )
            note_group.save()
            note_group.notes.set(group)
            note_groups.append(note_group)

    return note_groups








