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

    def test_delete_note(self):
        self.client.login(username='testuser', password='testpassword')
        note_to_delete = Note.objects.get(title='Test Note')
        response = self.client.post(reverse('notes:note_delete', kwargs={'pk': note_to_delete.pk}))
        self.assertFalse(Note.objects.filter(pk=note_to_delete.pk).exists())
        self.assertRedirects(response, reverse_lazy('notes:note_list'))

    def test_update_note_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('notes:note_update', kwargs={'pk': self.note.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Note')
        self.assertContains(response, 'Initial Title')
        self.assertContains(response, 'Initial content.')

    def test_update_note_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('notes:note_update', kwargs={'pk': self.note.pk}), {
            'title': 'Updated Title',
            'content': 'Updated content.',
        })
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Title')
        self.assertEqual(self.note.content, 'Updated content.')
        self.assertRedirects(response, reverse_lazy('notes:note_list'))
"""
