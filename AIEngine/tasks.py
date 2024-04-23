import logging
from typing_extensions import deprecated
from celery import shared_task
from django.core.cache import cache

from notes.models import Note

from .utils import *
from .analyze import *
from .config import model, tokenizer

import logging

""" Content Generation Methods"""

@shared_task
def generate_keywords_task(note_id):
    note = Note.objects.get(pk=note_id)
    
    if note.updated_at < cache.get(f"keywords_{note_id}_timestamp", note.updated_at):
        logging.info("Keywords already up-to-date.")
        return note.keywords
    
    cache.set(f"keywords_{note_id}_timestamp", note.updated_at, None)
    
    note_content = strip_html_tags(note.content)
    preprocessed_content = get_preprocessed_content(note_content)
    
    keywords = generate_keywords(preprocessed_content)
    
    note.keywords = keywords
    note.save()

    return keywords

@shared_task
def generate_summary_task(note_id):
    note = Note.objects.get(pk=note_id)
    
    if note.updated_at < cache.get(f"summary_{note_id}_timestamp", note.updated_at):
        logging.info("Summary already up-to-date.")
        return note.summary
    
    cache.set(f"summary_{note_id}_timestamp", note.updated_at, None)
    
    note_content = strip_html_tags(note.content)
    preprocessed_content = get_preprocessed_content(note_content)
    
    summary = generate_summary(preprocessed_content)
    
    note.summary = summary
    note.save()

    return summary

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

def generate_flashcards_task(note_id):
    note = Note.objects.get(id=note_id)
    flashcards = {}
    for keyword, definition in note.keywords.items():
        if not definition:
            definition = generate_definition(keyword)
            note.keywords[keyword] = definition
    note.save()
    return [{'term': k, 'definition': v} for k, v in note.keywords.items()]

def get_autocomplete_suggestions(note_id, prompt):
    
    prompt = strip_html_tags(prompt.strip())
    logging.info(f"Getting autocomplete suggestions...\n\n")
    
    if not prompt.strip().endswith(('.', '?', '!')):
        prompt = prompt.strip() + ' '

    prompt = f"Continue the following text: {prompt}"
    
    inputs = tokenizer.encode(prompt, return_tensors='pt', add_special_tokens=True)
    attention_mask = inputs.ne(tokenizer.pad_token_id).int()
    
    outputs = model.generate(
        input_ids=inputs,
        attention_mask=attention_mask,
        max_length=inputs.shape[-1] + 50, 
        num_return_sequences=3,
        do_sample=True,
        temperature=0.7,  
        top_k=50,  
        top_p=0.9,  
        pad_token_id=tokenizer.eos_token_id,
    )
    
    suggestions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    
    completions = [s[len(prompt):].strip() for s in suggestions]

    return completions

""" Auto Grouping Methods"""

def auto_group_note(note_id, threshold=0.15):
    try:
        target_note = Note.objects.get(pk=note_id)
        other_notes = Note.objects.exclude(pk=note_id)

        target_content = ' '.join(get_preprocessed_content(target_note)).lower()        
        other_contents = [' '.join(get_preprocessed_content(note)).lower() for note in other_notes]
        
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
        # notes = [strip_html_tags(note.content) for note in notes]
        preprocessed_list = [str(get_preprocessed_content(note)).lower() for note in notes]
        logging.info(f"Preprocessed list contents: {preprocessed_list}")
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

@deprecated("This method is deprecated.")
@shared_task
def analyze_note_task(note_id):
    note = Note.objects.get(pk=note_id)
    
    # Check cache
    if note.updated_at < cache.get(f"analysis_{note_id}_timestamp", note.updated_at):
        logging.info("Analysis already up-to-date.")
        return note.analysis
    
    cache.set(f"analysis_{note_id}_timestamp", note.updated_at, None)
    
    # Pre-process and strip HTML tags
    note_content = strip_html_tags(note.content)
    preprocessed_content = get_preprocessed_content(note_content)
    
    # Analyze note
    results = analyze(note_content, preprocessed_content)
    
    # Save analysis to Note model
    note.analysis = results
    note.save()

    return results
@shared_task
def analyze_note_task(note_id):
    note = Note.objects.get(pk=note_id)
    
    # Check cache
    if note.updated_at < cache.get(f"analysis_{note_id}_timestamp", note.updated_at):
        logging.info("Analysis already up-to-date.")
        return note.analysis
    
    cache.set(f"analysis_{note_id}_timestamp", note.updated_at, None)
    
    # Pre-process and strip HTML tags
    note_content = strip_html_tags(note.content)
    preprocessed_content = get_preprocessed_content(note_content)
    
    # Analyze note
    results = analyze(note_content, preprocessed_content)
    
    # Save analysis to Note model
    note.analysis = results
    note.save()

    return results
