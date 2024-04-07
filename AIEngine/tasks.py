from celery import shared_task
from django.core.cache import cache
from notes.models import Note
from AIEngine.analyze import analyze


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
    
    

