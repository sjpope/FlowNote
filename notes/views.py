# from .serializers import NoteSerializer, BlogPostSerializer
# from rest_framework import viewsets
import os
import openai

from AIEngine.services.note_analysis import analyze_notes
from AIEngine.tasks import *

from .forms import *
from .models import Note, NoteGroup

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

""" AI, ML Views """
def analyze(request, note_id):
    try:
        if request.method == "POST" :
            note = get_object_or_404(Note, pk=note_id)

            # analyze_note_task.delay(note_id)  # TO-DO: Trigger the Celery task to analyze the note asynchronously

            result = perform_note_analysis(note_id)
            keywords, summary = result.split('Summary: ')
            keywords = keywords.replace('Keywords: ', '')

            print('Analysis Complete: ', JsonResponse({'keywords': keywords, 'summary': summary}))

            #return redirect('notes:note_detail', pk=note.pk) 
            return JsonResponse({'keywords': keywords, 'summary': summary})
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        # TO-DO: Display the error msg as the analysis result instead of sending to notes/pk/analyze
        return JsonResponse({'error': str(e)})

def generate_response_from_prompt(request):
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        if prompt: #make sure it is not empty
            response = generate_response(prompt)
            return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400) #more error handling

""" Group Views """
def assign_note_to_group(request):
    if request.method == 'POST':
        form = NoteGroupAssignmentForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            groups = form.cleaned_data['groups']
            for group in groups:
                note.groups.add(group)
            return redirect('notes:group_list')
    else:
        form = NoteGroupAssignmentForm()
    
    return render(request, 'group/group_assign.html', {'form': form})

def group_edit(request, pk):
    group = get_object_or_404(NoteGroup, pk=pk)
    if request.method == 'POST':
        form = NoteGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('notes:group_list')
    else:
        form = NoteGroupForm(instance=group)
    return render(request, 'group/group_form.html', {'form': form})
                  
def group_delete(request, pk):
    group = get_object_or_404(NoteGroup, pk=pk)
    if request.method == 'POST':
        group.delete()
        return redirect('notes:group_list')
    return render(request, 'group/group_delete.html', {'group': group})

def group_detail(request, pk):
    group = get_object_or_404(NoteGroup, pk=pk)
    notes = group.notes.all()  # Grab all notes associated with the group
    return render(request, 'group/group_detail.html', {'group': group, 'notes': notes})

def group_create(request):
    if request.method == 'POST':
        form = NoteGroupForm(request.POST)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.owner = request.user
            new_group.save()
            return redirect('notes:group_list')
    else:
        form = NoteGroupForm()
    return render(request, 'group/group_form.html', {'form': form})

def group_list(request):
    groups = NoteGroup.objects.all()  
    return render(request, 'group/group_list.html', {'groups': groups})

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

""" User Auth Views """
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

""" Note Views """
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