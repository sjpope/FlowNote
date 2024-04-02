from django import forms
from .models import Note
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class NoteForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Note
        fields = ['title', 'content','summary']  # TO-DO: Add more fields here, such as 'tags' and 'is_favorite'.
        labels = {
            'title': '',
            'content': '',
            'summary': '',
        }
        placeholders = {
            'title': 'Enter title',
            'content': 'Enter content',
            'summary': 'Enter summary',
        }

    def __init__(self, *args, **kwargs):
        super(NoteForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in self.Meta.placeholders:
                self.fields[field].widget.attrs['placeholder'] = self.Meta.placeholders[field]

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(required=False)  

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user