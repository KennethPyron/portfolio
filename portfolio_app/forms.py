from django import forms
from django.core.exceptions import ValidationError
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
        fields = ['title', 'description', 'portfolio', 'status', 'image', 'github_url', 'live_url', 'tags']
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
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://github.com/username/repo'
            }),
            'live_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python, Django, Web Development'
            }),
        }
        labels = {
            'portfolio': 'Select Portfolio',
            'github_url': 'GitHub Repository URL',
            'live_url': 'Live Demo URL',
            'tags': 'Tags (comma-separated)'
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Title must be at least 3 characters long.')
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError('Image file size cannot exceed 5MB.')
        return image


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'major', 'portfolio', 'profile_picture', 'bio', 'graduation_year']
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
            'portfolio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'graduation_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '2025',
                'min': '2020',
                'max': '2030'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@uccs.edu'):
            raise ValidationError('Please use a valid UCCS email address (@uccs.edu).')
        return email

    def clean_graduation_year(self):
        year = self.cleaned_data.get('graduation_year')
        if year and (year < 2020 or year > 2035):
            raise ValidationError('Please enter a valid graduation year between 2020 and 2035.')
        return year