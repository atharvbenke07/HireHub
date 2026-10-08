from django import forms

from .models import Application


# ============================================================
# APPLICATION FORM
# ============================================================

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            'resume',
            'cover_letter',
        ]

        widgets = {
            'resume': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'cover_letter': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Write your cover letter...'
                }
            ),
        }


# ============================================================
# APPLICATION STATUS FORM
# ============================================================

class ApplicationStatusForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            'status',
        ]

        widgets = {
            'status': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }