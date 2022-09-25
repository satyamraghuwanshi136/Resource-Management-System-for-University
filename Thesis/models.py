

from django.db import models

# Create your models here.
class Thesis(models.Model):

    id = models.AutoField(primary_key=True)
    Department=models.CharField(max_length=200)
    Thesis_Name = models.CharField(max_length=150)
    Description=models.CharField(max_length=500)
    Student_Name=models.CharField(max_length=200)
    Enrollment=models.CharField(max_length=100)
    DOS = models.DateField()
    Pdf = models.FileField(upload_to='doc/')
    



