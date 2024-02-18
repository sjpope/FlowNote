from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Note

"""
class NoteAPITests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create a note
        self.note = Note.objects.create(title='Test Note', content='Test Content', owner=self.user)

    def test_create_note(self):
        url = reverse('note-list')  # You might need to adjust this based on your URL naming
        data = {'title': 'New Note', 'content': 'New Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.latest('id').title, 'New Note')
"""
