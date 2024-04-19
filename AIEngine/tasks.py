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
import logging

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

def get_autocomplete_suggestions(note_id, prompt):
    
    
    prompt = strip_html_tags(prompt.strip())
    logging.info(f"Getting autocomplete suggestions...\n\n{prompt}\n\n")
    # if prompt.endswith('.') or prompt.endswith('?') or prompt.endswith('!'):
    #     # Indicate to GPT-2 that it must continue on new sentence.
    #     prompt = prompt[:-1] + ' ' + tokenizer.eos_token
    # elif prompt.endswith(','):
    #     # We can pass as normal, GPT-2 should pick up on it.
    #     prompt = prompt[:-1] + ' '
    # else:
    #     prompt = prompt + '...'
    if not prompt.strip().endswith(('.', '?', '!')):
        prompt = prompt.strip() + ' '

    prompt = f"Continue the following text: {prompt}"
    
    # Generate inputs for the model
    inputs = tokenizer.encode(prompt, return_tensors='pt', add_special_tokens=True)
    attention_mask = inputs.ne(tokenizer.pad_token_id).int()
    
    # Generate continuation sequences with the model
    outputs = model.generate(
        input_ids=inputs,
        attention_mask=attention_mask,
        max_length=inputs.shape[-1] + 50,  # Generate sequences that continue beyond the length of the input
        num_return_sequences=3,
        do_sample=True,
        temperature=0.7,  # Adjust sampling temperature if necessary
        top_k=50,  # Use top-k sampling
        top_p=0.9,  # Use nucleus sampling
        pad_token_id=tokenizer.eos_token_id,
    )
    
    # Decode the output tokens to strings
    suggestions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    
    # Strip the original prompt from the suggestions to get the continuations
    completions = [s[len(prompt):].strip() for s in suggestions]

    return completions

""" Auto Grouping Methods"""
def auto_group_note(note_id, threshold=0.15):
    try:
        target_note = Note.objects.get(pk=note_id)
        other_notes = Note.objects.exclude(pk=note_id)

        target_content = get_preprocessed_content(target_note).lower()
        other_contents = [get_preprocessed_content(note).lower() for note in other_notes]

        contents = [target_content] + other_contents
        sim_matrix = compute_similarity_matrix(contents)
        similarities = sim_matrix[0, 1:]

        group_title = generate_group_title(contents)
        group = group_note(target_note, other_notes, similarities, threshold, group_title)

        return group
    except Exception as e:
        logging.error(f"An error occurred while auto grouping note: {str(e)}")
        return None

def auto_group_all(threshold=0.25, owner=None) -> list[NoteGroup]:
    """
    Group all notes based on overall similarity.
    """
    try:
        notes = Note.objects.all()
        preprocessed_list = [get_preprocessed_content(note).lower() for note in notes]
    
        sim_matrix = compute_similarity_matrix(preprocessed_list)
        all_groups = group_all_notes(notes, sim_matrix, threshold, owner=owner)
        
    except Exception as e:
        logging.error(f"An error occurred while grouping notes: {str(e)}")
        all_groups = []

    return all_groups

def generate_group_title(contents):
    
    prompt = "Generate a meaningful title based on these contents: " + ' '.join(contents)
    title = generate_content(prompt, num_return_sequences=1)[0]
    title = strip_prompt(prompt, title)
    
    return title.strip()

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
