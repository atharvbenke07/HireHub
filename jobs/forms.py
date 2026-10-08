from django import forms
from django.utils import timezone

from .models import Job


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = [
            'category',
            'title',
            'description',
            'location',
            'salary_min',
            'salary_max',
            'experience',
            'job_type',
            'skills',
            'deadline',
            'is_active',
        ]

        widgets = {

            'category': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Python Developer'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Pune'
                }
            ),

            'salary_min': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0'
                }
            ),

            'salary_max': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0'
                }
            ),

            'experience': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0-2 Years'
                }
            ),

            'job_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Python, Django, SQL'
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            ),
        }

    def clean_salary_min(self):

        salary_min = self.cleaned_data.get(
            'salary_min'
        )

        if salary_min < 0:
            raise forms.ValidationError(
                'Minimum salary cannot be negative.'
            )

        return salary_min

    def clean_salary_max(self):

        salary_max = self.cleaned_data.get(
            'salary_max'
        )

        if salary_max < 0:
            raise forms.ValidationError(
                'Maximum salary cannot be negative.'
            )

        return salary_max

    def clean(self):

        cleaned_data = super().clean()

        salary_min = cleaned_data.get(
            'salary_min'
        )

        salary_max = cleaned_data.get(
            'salary_max'
        )

        if (
            salary_min is not None
            and salary_max is not None
            and salary_max < salary_min
        ):
            raise forms.ValidationError(
                'Maximum salary cannot be less than minimum salary.'
            )

        return cleaned_data

def clean_deadline(self):

    deadline = self.cleaned_data.get('deadline')

    if deadline and deadline < timezone.localdate():

        raise forms.ValidationError(
            'Job deadline cannot be in the past.'
        )

    return deadline