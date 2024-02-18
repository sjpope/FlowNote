from django.shortcuts import render, redirect
# from rest_framework import viewsets
from .models import Note, BlogPost
from .forms import NoteForm
# from .serializers import NoteSerializer, BlogPostSerializer
from django.views.generic import ListView, DetailView


class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'  
    context_object_name = 'notes'

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'  

def home(request):
    return render(request, 'home.html')  

def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.owner = request.user  # TO-DO: Implement User Authentication / Guest User Logic
            new_note.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

