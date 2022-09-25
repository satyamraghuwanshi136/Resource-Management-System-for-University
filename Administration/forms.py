

from django import forms
from django.forms import models


CATEGORY_CHOICES = (("General","General"),("OBC","OBC"),("SC","SC"),("ST","ST"),)
POST_CHOICES = (("Professor","Professor"),("Assistant Professor","Assistant Professor"),("Lab Technician","Lab Technician"),("Associate Professor","Associate Professor"),)


class SendGridAPIForm(forms.Form):

    Key = forms.CharField(required=True, max_length=512, error_messages={'required': 'Please write your send grid API key'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'API Key'}))

class TwilioAPIForm(forms.Form):

    SID = forms.CharField(required=True, max_length=512, error_messages={'required': 'Please write your twilio API key'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Account SID Key'}))
    Token = forms.CharField(required=True, max_length=512, error_messages={'required': 'Please write your twilio API key'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Auth Token'}))
    Notify = forms.CharField(required=True, max_length=512, error_messages={'required': 'Please write your twilio API key'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Notify Service SID'}))

class PermissionForm(forms.Form):

    FacultyEmail = forms.CharField(required=True, widget=forms.TextInput({'class': 'form-control'}))
    Department = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Faculty = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Student = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Attendance = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    ViewAttendance = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Marks = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    ViewMarks = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Emails = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    SMS = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    API = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))
    Permission = forms.BooleanField(required=False, widget=forms.CheckboxInput({'class': 'form-check-input'}))

class StudentSetup(forms.Form):

    First = forms.CharField(required=True, label="First Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}))
    Last = forms.CharField(required=True, label="Last Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}))
    Enrollment = forms.CharField(required=True, label="Enrollment Number", max_length=64, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Enrollment', 'onBlur': "CheckEnroll();"}))
    Contact = forms.CharField(required=True, label="Contact (10 Digits)", max_length=10, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Phone Number'}))
    Category = forms.ChoiceField(required=True, label="Category", choices=CATEGORY_CHOICES,widget=forms.Select({'class': 'form-control'}))
    Photo = forms.FileField(required=True, label="Student Photo (jpg - 2 MB)", widget=forms.FileInput({'class': 'form-control', 'accept': 'image/jpg'}))
    DOB = forms.DateField(required=True, label="Date of Birth", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2010-12-31'}))
    Address = forms.CharField(required=True, label="Address", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Full Address'}))

class FacultySetup(forms.Form):

    First = forms.CharField(required=True, label="First Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}))
    Last = forms.CharField(required=True, label="Last Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}))
    EmployeeID = forms.CharField(required=True, label="Employee ID", max_length=64, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Employee ID', 'onBlur': "CheckEmployee();"}))
    Contact = forms.CharField(required=True, label="Contact (10 Digits)", max_length=10, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Phone Number'}))
    Post = forms.ChoiceField(required=True, label="Post", choices=POST_CHOICES, widget=forms.Select({'class': 'form-control'}))
    Qualification = forms.CharField(required=True, label="Qualifications", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Qualifications'}))
    Joining = forms.DateField(required=True, label="Date of Joining", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2021-12-31'}))
    Photo = forms.FileField(required=True, label="Faculty Photo (jpg - 2 MB)", widget=forms.FileInput({'class': 'form-control', 'accept': 'image/jpg'}))
    DOB = forms.DateField(required=True, label="Date of Birth", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2010-12-31'}))
    Address = forms.CharField(required=True, label="Address", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Full Address'}))

class StudentUpdate(forms.Form):

    First = forms.CharField(required=False, label="First Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}))
    Last = forms.CharField(required=False, label="Last Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}))
    Contact = forms.CharField(required=False, label="Contact (10 Digits)", max_length=10, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Phone Number'}))
    Category = forms.ChoiceField(required=False, label="Category", choices=CATEGORY_CHOICES,widget=forms.Select({'class': 'form-control'}))
    Photo = forms.FileField(required=False, label="Student Photo (jpg - 2 MB)", widget=forms.FileInput({'class': 'form-control', 'accept': 'image/jpg'}))
    DOB = forms.DateField(required=False, label="Date of Birth", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2010-12-31'}))
    Address = forms.CharField(required=False, label="Address", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Full Address'}))

class FacultyUpdate(forms.Form):

    First = forms.CharField(required=False, label="First Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'First Name'}))
    Last = forms.CharField(required=False, label="Last Name", max_length=150, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Last Name'}))
    Contact = forms.CharField(required=False, label="Contact (10 Digits)", max_length=10, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Phone Number'}))
    Post = forms.ChoiceField(required=True, label="Post", choices=POST_CHOICES, widget=forms.Select({'class': 'form-control'}))
    Qualification = forms.CharField(required=False, label="Qualifications", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Qualifications'}))
    Joining = forms.DateField(required=False, label="Date of Joining", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2021-12-31'}))
    Photo = forms.FileField(required=False, label="Faculty Photo (jpg - 2 MB)", widget=forms.FileInput({'class': 'form-control', 'accept': 'image/jpg'}))
    DOB = forms.DateField(required=False, label="Date of Birth", widget=forms.DateInput({'class': 'form-control', 'type': 'date', 'min': '1950-01-01', 'max':'2010-12-31'}))
    Address = forms.CharField(required=False, label="Address", max_length=1024, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Full Address'}))