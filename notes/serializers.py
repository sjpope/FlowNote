from rest_framework import serializers
from .models import Note, BlogPost

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'last_modified', 'owner']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'published', 'created_at', 'last_modified', 'owner']
