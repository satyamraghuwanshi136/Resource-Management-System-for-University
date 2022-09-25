from django import forms


class AddForm(forms.Form):
    # Department=[('Biomedical','Biomedical Engineering'),('Civil', 'Civil Engineering and Applied Mechanics'),
    # ('Cs', 'Computer Engineering'),
    # ('Electrical', 'Electrical Engineering'),
    # ('Elec1', 'Electronics and Instrumentation Engineering'),('Elec2','Electronics and Telecommunication Engineering'),('Humanities','Humanities and Social Sciences'),
    # ('Industrial','Industrial and Production Engineering'),('IT','Information Technology'),('MBA','Management Studies (MBA)'),('ME','Mechanical Engineering'),
    # (' Pharma',' Pharmacy'),(' Applied Chemistry',' Applied Chemistry and Chemical Technology'),
    # (' Applied Mathematics',' Applied Mathematics and Computational Sciences'),(' Applied Physics', "Applied Physics and Optoelectronics")]
    Department=[('Biomedical','Biomedical Engineering'),('Civil', 'Civil Engineering '),
    ('Cs', 'Computer Engineering'),
    ('Electrical', 'Electrical Engineering'),
    ('Elec1', 'Electronics '),('Humanities','Humanities and Social Sciences'),
    ('Industrial','Industrial'),('IT','Information Technology'),('MBA','Management Studies (MBA)'),('ME','Mechanical Engineering'),
    (' Pharma',' Pharmacy'),(' Applied Chemistry',' Applied Chemistry'),
    (' Applied Mathematics',' Applied Mathematics'),(' Applied Physics', "Applied Physics")]
    
    Department = forms.CharField(required=False, max_length=128, error_messages={
        'required': 'Please write your old password'}, widget=forms.Select(choices=Department,attrs={ 'rows': 2} ))
    Thesis_Name = forms.CharField(required=False, max_length=128, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Thesis Name'}))
    Description= forms.CharField(required=False, max_length=500, error_messages={
        'required': 'Please write your old password'}, widget=forms.Textarea({'class': 'form-control', 'placeholder': 'Description'}))
    Student_Name = forms.CharField(required=False, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Student Name'}))
    Enrollment = forms.CharField(required=False, max_length=64, error_messages={
        'required': 'Please write your old password'}, widget=forms.TextInput({'class': 'form-control', 'placeholder': 'Enrollment Number'}))
    # DOS = forms.DateField(required=False, max_length=10, error_messages={
    #     'required': 'Please write your old password'}, widget=forms.DateField({'class': 'form-control','placeholder': 'Date of submission'}))
    Pdf = forms.FileField(required= True, label="Thesis File", widget=forms.FileInput({'class': 'form-control', 'accept': 'text/csv'})) 