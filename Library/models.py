from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from Resources import models as ResourcesModels

# Create your models here.
class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('Data Structure', 'Data Structure'),
        ('Computer Network', 'Computer Network'),
        ('Software Engineering', 'Software Engineering'),
        ('Database Management System', 'Database Management System'),
        ('Operating System', 'Operating System'),
        ('Information Security', 'Information Security'),
        ('Analysis and design of Algorithms','Analysis and design of Algorithms'),
        ('Machine Learning','Machine Learning'),
        ('Discrete Mathematics', 'Discrete Mathematics'),
        ('Java', 'Java'),
        ('C++', 'C++'),
        ('C', 'C'),
        ('Python', 'Python'),
        ('Android Programming', 'Android Programming'),
        ('Big Data Analytics', 'Big Data Analytics'),
        ('Data Mining & Data Warehousing', 'Data Mining & Data Warehousing'),
        ('Distributed Computing', 'Distributed Computing'),
        ('Mobile Computing', 'Mobile Computing'),
        ('Internet of Things', 'Internet of Things'),
        ('Cloud Computing', 'Cloud Computing'),
        ('Mathematics','Mathematics'),
        ]
    name=models.CharField(max_length=255)
    isbn=models.CharField(max_length=255)
    author=models.CharField(max_length=255)
    category=models.CharField(max_length=50,choices=catchoice,default='education')
    quantity=models.IntegerField()

    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'
        

def get_expiry():
    return datetime.today() + timedelta(days=30)

    
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    enrollment=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+'['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    
    def __str__(self):
        student = ResourcesModels.Student.objects.get(Enrollment=self.enrollment)
        return self.enrollment + ",  " + student.First + " " + student.Last
