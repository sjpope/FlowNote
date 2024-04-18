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
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note_delete'),
    path('<int:pk>/update/', NoteUpdateView.as_view(), name='note_update'),

    # Task Status URL
    path('task-status/<str:task_id>/', task_status, name='task-status'),
    
    # Trained GPT-2 Model URLs
    path('generate-content/<int:note_id>/', generate_content_view, name='generate-content'),    
    path('autocomplete', autocomplete_view, name='autocomplete'),

    # Analysis URLs
    path('analyze/<int:note_id>/', analyze, name='analyze'),
    
    # AI Assistant URL
    path('generate-response/', generate_response_from_prompt, name='generate-response'),

    # Note Group URLs
    path('note-groups/search', GroupSearchView.as_view(), name='group_search'),
    
    # Auto Grouping
    path('notes/<int:note_id>/auto-group/', auto_group_note_view, name='auto_group_note'),
    path('notes/auto-group-all/', auto_group_all_view, name='auto_group_all'),
    
    # User Grouping
    path('note-groups/', group_list, name='group_list'),
    path('note-groups/<int:pk>/', group_detail, name='group_detail'),
    path('note-groups/create/', group_create, name='group_create'),
    path('note-groups/<int:pk>/edit/', group_edit, name='group_edit'),
    path('note-groups/<int:pk>/delete/', group_delete, name='group_delete'),
    path('assign-note-to-group/', assign_note_to_group, name='assign-note-to-group'),

    # Registration/User Profile URLs
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/settings/', settings, name='settings'),
    path('accounts/profile/settings/update-theme/', update_theme, name='update_theme'),

    # Search URLs
    path('search/', NoteSearchView.as_view(), name='note_search'),

    
]