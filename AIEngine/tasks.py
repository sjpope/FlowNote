from celery import shared_task
from django.core.cache import cache

from notes.models import Note
from AIEngine.analyze import *
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
""""""
tokenizer = GPT2Tokenizer.from_pretrained('./tokenizer')
model = GPT2LMHeadModel.from_pretrained('./models')

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

def generate_content_task(input_text):
    logging.info("Generating content...\n")
    inputs = tokenizer.encode_plus(input_text, return_tensors='pt', add_special_tokens=True, max_length=512, truncation=True)

    outputs = model.generate(
        inputs['input_ids'], 
        max_new_tokens=100,  # Limits the number of generated tokens
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=inputs['attention_mask']
    )

    # Decode the output tokens to a string
    content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logging.info(f"GPT-2 Response: {content}")

    return content


""" Auto Grouping Methods"""
def auto_group_note(note_id, threshold=0.15):
    """
    Create a group for a specified note based on similarity with other notes.
    """
    target_note = Note.objects.get(pk=note_id)
    other_notes = Note.objects.exclude(pk=note_id)

    target_content = get_preprocessed_content(target_note)
    other_contents = [get_preprocessed_content(note) for note in other_notes]
    preprocessed_list = [target_content] + other_contents  # Prepend the target note content

    sim_matrix = compute_similarity_matrix(preprocessed_list)
    similarities = sim_matrix[0, 1:]  # Similarities of the target note with others

    return group_note(target_note, other_notes, similarities, threshold)


def auto_group_all(threshold=0.25, owner=None):
    """
    Group all notes based on overall similarity.
    """
    notes = Note.objects.all()
    preprocessed_list = [get_preprocessed_content(note) for note in notes]
    sim_matrix = compute_similarity_matrix(preprocessed_list)

    # Pass the owner to the group_all_notes function
    return group_all_notes(notes, sim_matrix, threshold, owner=owner)

def get_preprocessed_content(note):
    cache_key = f"preprocessed_{note.pk}"
    preprocessed_content = cache.get(cache_key)

    if not preprocessed_content or note.updated_at > cache.get(f"{cache_key}_timestamp", note.updated_at):
        preprocessed_content = preprocess_text(note.content)
        cache.set(cache_key, preprocessed_content, None)  # None timeout means it's cached forever
        cache.set(f"{cache_key}_timestamp", note.updated_at, None)

    return preprocessed_content

""" Analysis Methods"""
def perform_note_analysis(note_id):
    note = Note.objects.get(pk=note_id)
    note_content = note.content

    # Perform analysis
    results = analyze(note_content)

    note = Note.objects.get(pk=note_id)
    note.analysis = results  # Store (non-parsed) analysis in Note.analysis field.
    note.save()

    return results

# async call
@shared_task
def perform_note_analysis_async(note_id):
    # TO-DO: Perform note analysis asynchronously
    pass
    
    

