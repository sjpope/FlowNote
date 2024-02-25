from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = 'notes' 


urlpatterns = [
    
    path('', home, name='home'),
    # .as_view() is used to convert the class-based view into a function-based view. See views.py for the difference between the two.
    
    # CRUD URLs
    path('list/', NoteListView.as_view(), name='note_list'), 
    path('<int:pk>/', NoteDetailView.as_view(), name='note_detail'),  # Primary Key used at the route to identify the correct note
    path('create/', create_note, name='create_note'),
    path('generate-response/', generate_response_from_prompt, name='generate-response'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),

    # Registration/User Profile URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),

    # These function-based views were replaced by Django's built-in auth views above.
    # path('login/', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),

    # Search URLs
    path('search/', NoteSearchView.as_view(), name='note_search'),
]