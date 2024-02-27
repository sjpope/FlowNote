# from .serializers import NoteSerializer, BlogPostSerializer
# from rest_framework import viewsets
from django.shortcuts import *   # render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.db.models import Q      # For complex queries (search feature)
from .models import Note, BlogPost
from .forms import *
from AIEngine.services.note_analysis import analyze_notes

def analyze(request, note_id):
    if request.method == "POST":
        note = Note.objects.get(pk=note_id)     # note = get_object_or_404(Note, pk=pk)

        # Perform analysis
        
        results = analyze_notes(note.content)
        note.analysis_results = results     # Save the results to the database? Or just display them to the user?

        # Display results to the user without changing the note content 

        # Send em back to the detail page
        return redirect('note_detail', pk=note.pk)
    
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