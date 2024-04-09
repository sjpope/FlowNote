# from .serializers import NoteSerializer, BlogPostSerializer
# from rest_framework import viewsets
import os
import openai

from AIEngine.analyze import analyze
from AIEngine.tasks import *

from .forms import *
from .models import *

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

from celery.result import AsyncResult
from .ai import generate_response

openai.api_key = os.getenv('OPENAI_API_KEY')

""" Async Task Status Views """
def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'SUCCESS' or task.ready():
        return JsonResponse({'status': task.status, 'result': task.get()})
    else:
        return JsonResponse({'status': task.status})

""" AI, ML Views """
def autocomplete_view(request):
    if request.method == 'GET':
        text = request.GET.get('text', '')
        suggestions = get_autocomplete_suggestions(text)  
        return JsonResponse({'suggestions': suggestions})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def generate_content_view(request, note_id):
    if request.method == 'GET':
        note = get_object_or_404(Note, pk=note_id)  
        prompt = request.GET.get('prompt', '')  
        
        input = f"{note.content}\n{prompt}"

        if input.strip():
            task = generate_content_task(input)
            return JsonResponse({'task_id': str(task.id)})
        else:
            return JsonResponse({'error': 'Note content and prompt are empty'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def auto_group_note_view(request, note_id):
    if request.method == "POST":
        messages.info(request, 'Auto-grouping for this note has been initiated.')

        new_group = auto_group_note(note_id)
        
        if new_group:
            logging.debug(f"Auto Grouping for note {note_id} successful. Group: {new_group}")
            # Display a success message / notification to the user.
        

        return redirect('notes:note_detail', pk=note_id)  
    else:
        note = get_object_or_404(Note, pk=note_id)
        return render(request, 'notes/auto_group_note.html', {'note': note})

def auto_group_all_view(request):
    if request.method == "POST"and request.user.is_authenticated:
        messages.info(request, 'Auto-grouping for all notes has been initiated.')

        new_groups = auto_group_all(owner=request.user)
        
        if new_groups:
            logging.debug(f"Auto Grouping for all notes successful. Created {new_groups.count} new groups: {new_groups}")
            
        # Display a success message / notification to the user.
        return redirect('notes:group_list') 
    return render(request, 'notes/auto_group_all.html')

def analyze(request, note_id):
    try:
        if request.method == "POST" :
            note = get_object_or_404(Note, pk=note_id)

            # analyze_note_task.delay(note_id)          # TO-DO: Trigger the Celery task to analyze the note asynchronously
            messages.info(request, 'Note analysis has been initiated.')
            result = perform_note_analysis(note_id)
            
            if 'Summary' not in result:                 # Likely caused by note content less than 25 words.
                return JsonResponse({'result': result})
            
            keywords, summary = result.split('Summary: ')
            keywords = keywords.replace('Keywords: ', '')

            print('Analysis Complete: ', JsonResponse({'keywords': keywords, 'summary': summary}))

            # return redirect('notes:note_detail', pk=note.pk) 
            return JsonResponse({'keywords': keywords, 'summary': summary})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
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

@login_required
def settings(request):
    return render(request, 'settings.html', {'user': request.user})

def update_theme(request):
    if request.method == 'POST':
        theme = request.POST.get('theme')
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_profile.theme = theme
        user_profile.save()
        messages.success(request, 'Theme updated successfully')
    return redirect('notes:settings')

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
    
    def get_success_url(self):
        pk = self.object.pk
        return reverse('notes:note_detail', kwargs={'pk': pk})