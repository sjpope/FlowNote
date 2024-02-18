from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']  # TO-DO: Add more fields here, such as 'tags' and 'is_favorite'.