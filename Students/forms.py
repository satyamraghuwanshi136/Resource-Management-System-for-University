from django import forms


class SearchForm(forms.Form):
    First = forms.CharField(required=False, max_length=128, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}))
    Last = forms.CharField(required=False, max_length=128, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}))
    Email = forms.EmailField(required=False, error_messages={
        'required': 'Please write your old password'}, widget=forms.EmailInput({'class': 'form-control', 'placeholder': 'Email Address'}))
    Contact = forms.CharField(required=False, max_length=10, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Contact Number (10 digits)'}))
    Enrollment = forms.CharField(required=False, max_length=64, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Enrollment Number'}))

class StudentCSV(forms.Form):
    CSV = forms.FileField(required= True, label="Student Details CSV File", widget=forms.FileInput({'class': 'form-control', 'accept': 'text/csv'}))