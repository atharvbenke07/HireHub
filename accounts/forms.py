from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    )

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'phone',
            'location',
            'skills',
            'experience',
            'resume',
            'profile_picture',
        ]

        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            ),

            'experience': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'resume': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'profile_picture': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }