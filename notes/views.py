from django.shortcuts import render
from rest_framework import viewsets
from .models import Note, BlogPost
from .serializers import NoteSerializer, BlogPostSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Use Django views to render templates (frontend)