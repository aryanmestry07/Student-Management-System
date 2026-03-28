# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from student.models import Student
from .models import Course, Topic, Assignment, Quiz ,Notice


# ---------------- Course Form ----------------
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category', 'description', 'duration', 'price']


# ---------------- Student Forms ----------------
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'courses']  # only Student fields
        widgets = {
            'courses': forms.CheckboxSelectMultiple
        }


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phone', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


# ---------------- Topic Form ----------------
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']


# ---------------- Assignment Form ----------------
class AssignmentForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date']


# ---------------- Quiz Form ----------------
class QuizForm(forms.ModelForm):
    # Optional: add a date field for quiz deadline
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    class Meta:
        model = Quiz
        fields = ['title', 'description', 'deadline']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'is_active']