# from .serializers import NoteSerializer, BlogPostSerializer
# from rest_framework import viewsets
import os
import openai
#import AIEngine

from AIEngine.services.note_analysis import analyze_notes
from AIEngine.tasks import *

from .forms import *
from .models import Note

from django.urls import reverse, reverse_lazy
from django.shortcuts import *   # render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q      # For complex queries (search feature)
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from .ai import generate_response

openai.api_key = os.getenv('OPENAI_API_KEY')

def analyze(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, pk=note_id)

        # Trigger the Celery task to analyze the note asynchronously
        analyze_note_task.delay(note_id)

        messages.add_message(request, messages.INFO, 'Analysis is pending. Please check back shortly.')

        # Redirect the user to the note detail page immediately
        return redirect('note_detail', pk=note.pk)

def generate_response_from_prompt(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        if prompt: #make sure it is not empty
            response = generate_response(prompt)
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400) #more error handling

class NoteSearchView(ListView):
    model = Note
    template_name = 'note_search.html'
    context_object_name = 'notes'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Note.objects.filter(Q(title__icontains=query) | Q(content__icontains=query), owner=self.request.user)
        else:
            return Note.objects.filter(owner=self.request.user)

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:login')
    else:
        form = RegisterForm()  
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))  # TO-DO: Redirect to success page, or add a success message
        else:
            print('Invalid login') # TO-DO: Add error message, session handling logic
    
    # else: method is GET        
    return render(request, 'registration/login.html')  

def user_logout(request):
    logout(request)
    return redirect('home')  # TO-DO: Redirect to success page, or add a success message

def home(request):
    return render(request, 'home.html')  

@login_required
def create_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.owner = request.user  
            new_note.save()
            return redirect('notes:note_list')
    else:
        form = NoteForm()
    return render(request, 'note_form.html', {'form': form})

class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'  
    context_object_name = 'notes'

class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'  

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'note_delete.html'
    success_url = reverse_lazy('notes:note_list') 

class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_update.html'
    success_url = reverse_lazy('notes:note_list')