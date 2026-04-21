# myapp/forms.py

from django import forms
from django.contrib.auth.models import User
from student.models import Student
from .models import Course, Topic, Assignment, Quiz, Notice


# ---------------- Course Form ----------------
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category', 'description', 'duration', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ---------------- Student Forms ----------------
class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'style': 'height: 120px;'
        })
    )

    class Meta:
        model = Student
        fields = ['phone', 'fees_status']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'fees_status': forms.Select(attrs={'class': 'form-control'}),
        }


class StudentUpdateForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'style': 'height: 120px;'
        })
    )

    class Meta:
        model = Student
        fields = ['phone', 'courses', 'fees_status']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'fees_status': forms.Select(attrs={'class': 'form-control'}),
        }


# ---------------- User Update ----------------
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


# ---------------- Topic Form ----------------
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'notes_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'notes_file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }


# ---------------- Assignment Form ----------------
class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ---------------- Quiz Form ----------------
class QuizForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        required=False
    )

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ---------------- Notice Form ----------------
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }