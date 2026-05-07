# student/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student, Submission


class StudentSignupForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
        required=True
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
        required=True
    )

    class Meta:
        model = Student
        fields = [
            "first_name", "middle_name", "last_name",
            "phone", "birthdate", "education",
            "courses",
            "total_fees",     # ✅ NEW
            "paid_amount"     # ✅ NEW
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "birthdate": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "education": forms.TextInput(attrs={"class": "form-control"}),

            # Courses
            "courses": forms.CheckboxSelectMultiple(),

            # ✅ NEW FIELDS
            "total_fees": forms.NumberInput(attrs={"class": "form-control"}),
            "paid_amount": forms.NumberInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        # 🔥 OPTIONAL VALIDATION (VERY GOOD)
        total = cleaned_data.get("total_fees") or 0
        paid = cleaned_data.get("paid_amount") or 0

        if paid > total:
            raise forms.ValidationError("Paid amount cannot be greater than total fees.")

        return cleaned_data

class AssignmentUploadForm(forms.ModelForm):
    class Meta:
        model = Submission   # ✅ Correct model (not Assignment)
        fields = ["file"]
        widgets = {
            "file": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
