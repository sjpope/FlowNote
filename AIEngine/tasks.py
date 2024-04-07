from celery import shared_task
from django.core.cache import cache

from notes.models import Note
from AIEngine.analyze import *

""" Auto Grouping Methods"""
def auto_group_note(note_id, threshold=0.25):
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


def auto_group_all(threshold=0.25):
    """
    Group all notes based on overall similarity.
    """
    notes = Note.objects.all()
    preprocessed_list = [get_preprocessed_content(note) for note in notes]
    sim_matrix = compute_similarity_matrix(preprocessed_list)

    return group_all_notes(notes, sim_matrix, threshold)

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
    
    

