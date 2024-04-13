from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

from notes.models import Note, NoteGroup
from .utils import *

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import logging

tokenizer = GPT2Tokenizer.from_pretrained('./tokenizer')
model = GPT2LMHeadModel.from_pretrained('./models')

def generate_content(prompt, max_length=150, num_return_sequences=2, additional_tokens=500):
    
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
            
            temperature=0.8, 
            top_k=50,
            top_p=0.92,
            
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    # content = tokenizer.decode(outputs[0], skip_special_tokens=True)
    suggestions = [tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
    return suggestions

def analyze(content):
    processed_content = preprocess_text(content)
    if len(processed_content.split()) < 25:
        logging.warning("Text too short for analysis.")
        return "Text too short for analysis."
    keywords = preprocess_and_extract_keywords(processed_content)
    summary = generate_content(f"Summarize this content: {content}", num_return_sequences=1)[0]
    cleaned_summary = remove_prompt_from_content(f"Summarize this content: {content}", summary)
    return {
        "keywords": ', '.join(keywords),
        "summary": cleaned_summary
    }
    
"""
TO-DO: ITERATE THROUGH THESE OLD FUNCTIONS AND KEEP WHAT'S NEEDED
"""

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



# def summarize_with_gpt2(note_content):
#     prompt = f"Summarize this content: {note_content}"
#     summary = generate_content_task(prompt, num_return_sequences=1)[0]
#     cleaned_summary = remove_prompt_from_content(prompt, summary)
#     return cleaned_summary






