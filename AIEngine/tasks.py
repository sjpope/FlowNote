import logging
from celery import shared_task
from django.core.cache import cache

from notes.models import Note
from AIEngine.analyze import *
# from .analyze import *

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re

""" Load GPT-2 Model and Tokenizer Globally """
tokenizer = GPT2Tokenizer.from_pretrained('./tokenizer')
model = GPT2LMHeadModel.from_pretrained('./models')

""" 
Autocompletion Generation Configuration. 
If the note ends on complete sentence, it regurgitates the prompt. 
"""

# def generate_content_task(input_text):
#     logging.info("Generating content...\n")
#     input_text = "As artificial intelligence systems become more integrated into various aspects of life,"
#     inputs = tokenizer.encode_plus(input_text, return_tensors='pt', add_special_tokens=True, max_length=512, truncation=True)

#     outputs = model.generate(
#         inputs['input_ids'], 
#         max_new_tokens=100,  
#         pad_token_id=tokenizer.eos_token_id,
#         attention_mask=inputs['attention_mask']
#     )

    
#     content = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     logging.info(f"GPT-2 Response: {content}")

#     return content

def extract_keywords_with_gpt2(note_content):
    prompt = f"Identify the key concepts in this text: {note_content}"
    content = generate_content_task(prompt, num_return_sequences=1)[0]
    keywords = extract_keywords_with_gpt2(content)
    return keywords

def summarize_with_gpt2(note_content):
    prompt = f"Summarize this content: {note_content}"
    summary = generate_content_task(prompt, num_return_sequences=1)[0]
    cleaned_summary = remove_prompt_from_content(prompt, summary)
    return cleaned_summary

def generate_content_task(prompt, max_length=150, num_return_sequences=2, additional_tokens=500):
    
    encoding = tokenizer(prompt, return_tensors='pt', truncation=True)
    input_ids = encoding['input_ids']
    attention_mask = encoding['attention_mask']

    total_max_length = input_ids.shape[1] + additional_tokens

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=total_max_length,
            min_length=input_ids.shape[1] + 20,  
            temperature=0.8, 
            top_k=50,
            top_p=0.92,
            no_repeat_ngram_size=3,  
            num_return_sequences=num_return_sequences,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    suggestions = [tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
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

""" Utility Methods """
def get_preprocessed_content(note):
    cache_key = f"preprocessed_{note.pk}"
    preprocessed_content = cache.get(cache_key)

    if not preprocessed_content or note.updated_at > cache.get(f"{cache_key}_timestamp", note.updated_at):
        preprocessed_content = preprocess_text(note.content)
        cache.set(cache_key, preprocessed_content, None)  # None timeout means it's cached forever
        cache.set(f"{cache_key}_timestamp", note.updated_at, None)

    return preprocessed_content

def remove_prompt_from_content(prompt, content):
    
    try:
        start_index = content.index(prompt) + len(prompt)
    except ValueError:
        start_index = 0
    
    return content[start_index:].strip()

""" Analysis Methods"""
def perform_note_analysis(note_id):
    note = Note.objects.get(pk=note_id)
    note_content = note.content

    results = analyze(note_content, model, tokenizer)

    note = Note.objects.get(pk=note_id)
    note.analysis = results  # Store (non-parsed) analysis in Note.analysis field.
    note.save()

    return results

@shared_task
def perform_note_analysis_async(note_id):
    # TO-DO: Perform note analysis asynchronously
    pass
    
def analyze(content, model, tokenizer):
    processed_notes = preprocess_text(content)  
    logging.debug(f"Processed Notes: {processed_notes}")

    if len(processed_notes.split()) < 25:
        logging.warning("Text too short or insignificant for analysis.")
        return "Text too short or insignificant for analysis."

    keywords = preprocess_and_extract_keywords(processed_notes)
    logging.info(f"Extracted Keywords: {keywords}")

    # summary = summarize_text_with_lsa(processed_notes)
    # logging.info(f"Summary (LSA): {summary}\n\n\n")
    summary_gpt2 = ""
    try:
        summary_gpt2 = summarize_with_gpt2(content)
        logging.info(f"Summary (GPT-2): {summary_gpt2}")
    except Exception as e:
        logging.error(f"Error in summarize_with_gpt2: {e}")
        summary_gpt2 = "Error generating summary with GPT-2."
    
    keywords_str = ', '.join(keywords)  
    analysis_result = f"Keywords: {keywords_str}\n\nSummary: {summary_gpt2}"
    
    return analysis_result

