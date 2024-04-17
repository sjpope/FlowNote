import logging
from celery import shared_task
from django.core.cache import cache

from notes.models import Note

from .utils import *
from .analyze import *
from .config import model, tokenizer

import torch
import re
import datetime as dt

""" Content Generation Methods"""

def generate_content_task(prompt, content):
    
    # TO-DO: Add check for empty content here
    input_text = f"{content}\n{prompt}"
    input_text = strip_html_tags(input_text)
    
    # TO-DO: Allow users to specify parameter (max_length, num_return_sequences) size in their settings. Use Slider? 
    max_length=150
    num_return_sequences=1
    additional_tokens=500
    
    suggestions = generate_content(input_text, max_length, num_return_sequences, additional_tokens)
    
    return suggestions

def generate_flashcards_task(key_concepts):
    
    flashcards = []
    
    # flashcards = generate_flashcards(key_concepts)
    # TO-DO: Save flashcards to Django cache or DB directly. Consider saving list of Vocab/Keywords to Note Model directly.
   
    return flashcards

def get_autocomplete_suggestions(prompt):
    inputs = tokenizer.encode(prompt, return_tensors='pt')
    
    # TO-DO: Allow users to specify parameter (max_length, num_return_sequences) size in their settings. Use Slider? 
    outputs = model.generate(inputs, max_length=len(inputs[0]) + 10, num_return_sequences=3, do_sample=True)

    suggestions = []
    for output in outputs:
        text = tokenizer.decode(output, skip_special_tokens=True)
        continuation = text[len(prompt):].strip()           # Isolate the prompt from the suggestion
        suggestion = continuation.split()[0] if continuation else ''
        
        if suggestion not in suggestions:
            suggestions.append(suggestion)

    return suggestions

""" Auto Grouping Methods"""
def auto_group_note(note_id, threshold=0.15):
    """
    Create a group for a specified note based on similarity with other notes.
    """
    target_note = Note.objects.get(pk=note_id)
    other_notes = Note.objects.exclude(pk=note_id)

    target_content = get_preprocessed_content(target_note)
    other_contents = [get_preprocessed_content(note) for note in other_notes]
    
    preprocessed_list = [target_content] + other_contents 

    sim_matrix = compute_similarity_matrix(preprocessed_list)
    similarities = sim_matrix[0, 1:]  

    return group_note(target_note, other_notes, similarities, threshold)

def auto_group_all(threshold=0.25, owner=None):
    """
    Group all notes based on overall similarity.
    """
    notes = Note.objects.all()
    preprocessed_list = [get_preprocessed_content(note) for note in notes]
    sim_matrix = compute_similarity_matrix(preprocessed_list)

    return group_all_notes(notes, sim_matrix, threshold, owner=owner)

""" Analysis Methods"""

def analyze_note(note_id):
    
    note = Note.objects.get(pk=note_id)
    
    # Turned off for Testing/Debugging
    # if note.updated_at < cache.get(f"analysis_{note_id}_timestamp", note.updated_at):
    #     logging.info("Analysis already up-to-date.")
    #     return note.analysis
    
    cache.set(f"analysis_{note_id}_timestamp", note.updated_at, None)
    
    note_content = strip_html_tags(note.content)
    preprocessed_content = get_preprocessed_content(note)
    
    results = analyze(note_content, preprocessed_content)
    
    note.analysis = results  # Store (non-parsed) analysis in Note.analysis field.
    note.save()

    return results
