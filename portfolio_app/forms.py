from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Portfolio, Project, Student
import re

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'about', 'contact_email', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter portfolio title',
                'required': True
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe this portfolio...'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com',
                'required': True
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'is_active': 'Make Portfolio Public'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_contact_email(self):
        email = self.cleaned_data.get('contact_email')
        if email and not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError('Please enter a valid email address.')
        return email


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'portfolio']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project title',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your project in detail...'
            }),
            'portfolio': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
        labels = {
            'portfolio': 'Select Portfolio',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'major', 'Portfolio']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@uccs.edu',
                'required': True
            }),
            'major': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Portfolio': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']