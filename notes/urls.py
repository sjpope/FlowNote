from django.urls import path
from .views import NoteListView, NoteDetailView, home, create_note, login


app_name = 'notes' 


urlpatterns = [
    # .as_view() is used to convert the class-based view into a function-based view. See views.py for the difference between the two.
    path('', NoteListView.as_view(), name='note_list'), 
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),  # Primary Key used at the route to identify the correct note
    
    # These are function-based views
    path('', home, name='home'),
    path('create/', create_note, name='create_note'),
    path('login', login, name='login'),
]