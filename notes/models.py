from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from ckeditor.fields import RichTextField

class NoteGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:  
        app_label = 'notes'
    

from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    
    summary = models.CharField(max_length=255, blank=True)
    keywords = models.JSONField(default=dict, blank=True)  
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)        # (4/20, SJP) Removed last_modified field
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE)
    groups = models.ManyToManyField('NoteGroup', related_name='notes')

    def __str__(self):
        return self.title

    class Meta:  
        app_label = 'notes'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, default='light')
    
    class Meta:  
        app_label = 'notes'



