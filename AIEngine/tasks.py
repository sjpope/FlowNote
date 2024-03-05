from celery import shared_task
from django.core.cache import cache
from notes.models import Note
from DataConnector.data_access import getMongoDB, pushMongoDB
from AIEngine.services.note_analysis import analyze_notes

@shared_task
def analyze_note_task(note_id):
    database_name = 'NoteData'  
    collection_name = 'AnalysisResults'  

    # Check MongoDB for existing analysis results
    existing_results = getMongoDB(
        database_name=database_name,
        collection_name=collection_name,
        query={'note_id': note_id}
    )

    if existing_results:
        # Analysis results already exist in MongoDB, you can choose to use these results
        # or update them depending on your application's logic
        results = existing_results[0]['analysis_results']  # Assuming 'analysis_results' is the key used to store results
    else:
        # Retrieve the note content (assuming Note model has a 'content' field)
        note = Note.objects.get(pk=note_id)
        note_content = note.content

        results = analyze_notes(note_content)

        # Store the new analysis results in MongoDB
        pushMongoDB(
            database=database_name,
            collection=collection_name,
            data={
                'note_id': note_id,
                'analysis_results': results
            }
        )

    # Here, you can decide what to do with the 'results' variable
    # For example, you could update the Note model instance with a summary or keywords
    # Or you might want to notify the user that the analysis is complete