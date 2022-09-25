
from django import forms


class SendForm(forms.Form):

    To = forms.CharField(required=True, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Recipient\'s Email Address'}))
    Subject = forms.CharField(required=True, max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Subject'}))
    Attachment = forms.FileField(required=False, widget=forms.FileInput({'class': 'form-control'}))
    Body = forms.CharField(required=True, widget=forms.Textarea({'class': 'form-control'}))

class SMSForm(forms.Form):

    Contact = forms.CharField(required=True, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Phone Number'}))
    Message = forms.CharField(required=True, widget=forms.Textarea({'class': 'form-control'}))