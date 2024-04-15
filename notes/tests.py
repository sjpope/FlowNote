from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Note

# notes = Note.objects.all().order_by('-id')[:k]
Note.objects.get(id in [6,7])

from notes.models import Note  
from AIEngine.tasks import analyze_note  


def test_analysis():
    # Fetch FIRST k notes from db
    # notes = Note.objects.all()[:k]
    notes = Note.objects.filter(id__in=[6, 7])
    
    if not notes:
        print(f"No notes found. Please check your database.")
        return
    
    for idx, note in enumerate(notes, start=1):
        print(f"\n\n--- Note {idx} Analysis ---")
        print("Note Content:")
        print(note.content)
        print("\n--- Performing Analysis ---\n")
        
        result = analyze_note(note.pk)  
        
        print("Analysis Results:")
        print(f"Summary: {result['summary']}")
        print(f"Keywords: {result['keywords']}")

test_analysis()