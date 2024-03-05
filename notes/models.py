from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    summary = models.CharField(max_length=255, blank=True)
    analysis = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notes', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

#TO-DO: Implement a BlogPost model with the following fields:
# class BlogPost(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     published = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)
#     owner = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

