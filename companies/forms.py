from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):

    class Meta:

        model = Company

        fields = [
            'company_name',
            'description',
            'website',
            'location',
            'logo',
        ]

        widgets = {

            'company_name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5
                }
            ),

            'website': forms.URLInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'logo': forms.FileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }