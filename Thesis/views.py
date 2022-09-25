# from functools import _Descriptor
from io import StringIO
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from Resources.models import Department, Student
from datetime import date
from Thesis import models
from .models import Thesis


from .forms import AddForm
from django.core.paginator import Paginator
from django.urls import reverse
import csv
import datetime



# @permission_required('Resources.student_rights')
def manage(request):
    return render(request, 'Thesis/Manage.html', {'AddForm': AddForm()})

# @permission_required('Resources.student_rights')
def Search(request):
    if request.method == "POST":
        Search_thesis = request.POST.get('Thesis_Name', None)
        Search = Thesis.objects.filter(Thesis_Name__contains=Search_thesis)
        total=Search.count()
        
        if total:
            paginator = Paginator(Search, 10)  # Show 10 contacts per page
            page = request.GET.get('page')
            thesis= paginator.get_page(page)
            return render(request, 'Thesis/Search.html', {"thesis":thesis,'total':total})
        else:
            return render(request, 'Thesis/Manage.html', {'Message_Search': 'Thesis not found.', 'visiblity': 'visible', 'color': 'danger', 'AddForm': AddForm()})
    
    return render(request, 'Thesis/Manage.html',{'AddForm': AddForm()})


        
@permission_required('Resources.student_rights')
def RemoveThesis(request,tname):

    
        tdelete = models.Thesis.objects.get(Thesis_Name=tname)
        tdelete.delete()
        return render(request, 'Thesis/Manage.html', { 'Message': 'Thesis Removed!', 'visiblity': 'visible', 'color': 'success', 'AddForm': AddForm()})



def Remove(request):
    if request.method == "POST":
        Search_thesis = request.POST.get('thesis_remove', None)
        Search = Thesis.objects.filter(Thesis_Name__contains=Search_thesis)
        total=Search.count()
        
        if total:
            paginator = Paginator(Search, 10)  # Show 10 contacts per page
            page = request.GET.get('page')
            thesis= paginator.get_page(page)
            return render(request, 'Thesis/Remove.html', {"thesis":thesis,'total':total})
        else:
            return render(request, 'Thesis/Manage.html', {'Message': 'Thesis not found.', 'visiblity': 'visible', 'color': 'danger', 'AddForm': AddForm()})
    
    return render(request, 'Thesis/Manage.html',{'AddForm': AddForm()})
    


@permission_required('Resources.student_rights')
def AddThesis(request):
    # context={}
    

    
    if request.method == 'POST':
        Form=AddForm(request.POST, request.FILES)
        
        if Form.is_valid():
            Dep=Form.cleaned_data['Department']
            Tname=Form.cleaned_data['Thesis_Name']
            Des=Form.cleaned_data['Description']
            Sname=Form.cleaned_data['Student_Name']
            Enroll=Form.cleaned_data['Enrollment']
            Date=datetime.date.today()
            files=Form.cleaned_data['Pdf']
            # temp=models.Thesis(Department=Dep,Thesis_Name=Tname,Description=Des,Student_Name=Sname,Enrollment=Enroll,DOS=Date)
            # temp.save()
            Thesis(Department=Dep,Thesis_Name=Tname,Description=Des,Student_Name=Sname,Enrollment=Enroll,DOS=Date,Pdf=files).save()
            HttpResponse("File Uploaded")
            
        else:
            Form=AddForm()
            return render(request, 'Thesis/Manage.html',{'AddForm': Form})
    else:
        return render(request, 'Thesis/Manage.html',{'AddForm': AddForm()})
            

    return render(request, 'Thesis/Manage.html',{'AddForm': AddForm()} )

# @permission_required('Resources.student_rights')
# def Message(request):
#     return render(request, 'Thesis/Message.html')



@permission_required('Resources.student_rights')
def ListThesis(request):
    thesisAll=Thesis.objects.all()
    total=thesisAll.count()
    paginator = Paginator(thesisAll, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    thesis = paginator.get_page(page)
    return render(request, 'Thesis/List.html',{'thesis':thesis,'total':total})



        
        

