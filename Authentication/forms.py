

from django import forms


class LoginForm(forms.Form):
    # Login Form
    Username = forms.CharField(required=True, max_length=150, error_messages={'required': 'Please write your username'}, widget=forms.TextInput({'class': 'form-control form-control-user', 'placeholder': 'Username'}))
    Password = forms.CharField(required=True, max_length=64, error_messages={'required': 'Please write your password'}, widget=forms.PasswordInput({'class': 'form-control form-control-user', 'placeholder': 'Password'}))
