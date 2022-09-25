from django import forms
from django.contrib.auth.models import User
from . import models
from Resources import models as ResourcesModels


class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','isbn','author','quantity', 'category' ]
        widgets = {
            'name': forms.TextInput( {'class': 'form-control', 'placeholder': 'Full Name', 'max_length':100}),
            # !!!! Important (not really)
            #  replace TextInput to some kind of number input
            'isbn': forms.TextInput({'class': 'form-control', 'placeholder': 'Isbn'}),
            'author': forms.TextInput({'class': 'form-control', 'placeholder': 'Author'}),
            'quantity': forms.NumberInput({'class': 'form-control', 'placeholder': 'Quantity'}),
            'category': forms.Select({'class': 'form-control'})
        }


class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.filter(quantity__gt=0) ,empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn', widget=forms.Select({'class': 'form-control', 'id': 'name_and_isbn'}))
    enrollment2=forms.ModelChoiceField(queryset=ResourcesModels.Student.objects.all(),empty_label="Name and enrollment",to_field_name='Enrollment',label='Name and enrollment', widget=forms.Select({'class': 'form-control', 'id': 'name_and_enrollment'}))
    
    # widgets = {
    #         # 'name': forms.TextInput( {'class': 'form-control', 'placeholder': 'Full Name', 'max_length':100}),
    #         # # !!!! Important (not really)
    #         # #  replace TextInput to some kind of number input
    #         # 'isbn': forms.TextInput({'class': 'form-control', 'placeholder': 'Isbn'}),
    #         # 'author': forms.TextInput({'class': 'form-control', 'placeholder': 'Author'}),
    #         # 'quantity': forms.NumberInput({'class': 'form-control', 'placeholder': 'Quantity'}),
    #         # 'category': forms.Select({'class': 'form-control'})
    #     }
    