from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.http import HttpResponse
import time
import random
# Create your views here.

def course(request):

    if request.method == 'POST':

        domain_name = request.POST.get('depart', '')

        objectInstance = Department.objects.filter(id=domain_name).first()

        search_qs = Course.objects.filter(Department_id=objectInstance)

        data = {}

        if search_qs.count() > 0:

            for i in search_qs.values_list('id', 'Name'):
                data.update({i[0]: i[1]})

        else:
            data = {'0': '--no courses found--'}

    else:

        data = {'0': '--no courses found--'}

    return JsonResponse(data)


def branch(request):

    if request.method == 'POST':

        domain_name = request.POST.get('course', '')

        objectInstance = Course.objects.filter(id=domain_name).first()

        search_qs = Branch.objects.filter(Course_id=objectInstance)

        data = {}

        if search_qs.count() > 0:

            for i in search_qs.values_list('id', 'Name'):
                data.update({i[0]: i[1]})

        else:
            data = {'0': '--no branch found--'}

    else:

        data = {'0': '--no branch found--'}

    return JsonResponse(data)


def semester(request):

    if request.method == 'POST':

        domain_name = request.POST.get('branch', '')

        objectInstance = Branch.objects.filter(id=domain_name).first()

        search_qs = Semester.objects.filter(Branch_id=objectInstance)

        data = {}

        if search_qs.count() > 0:

            for i in search_qs.values_list('id', 'Name'):
                data.update({i[0]: i[1]})

        else:
            data = {'0': '--no semester found--'}

    else:

        data = {'0': '--no semester found--'}

    return JsonResponse(data)


def subject(request):

    if request.method == 'POST':

        domain_name = request.POST.get('semester', '')

        objectInstance = Semester.objects.filter(id=domain_name).first()

        search_qs = Subject.objects.filter(Semester_id=objectInstance)

        data = {}

        if search_qs.count() > 0:

            for i in search_qs.values_list('id', 'Name', 'Theory_Lectures', 'Lab_Lectures'):
                data.update({i[0]: str(i[1]) + ' [Theory Lecture: ' + str(i[2]) + ', Lab Lecture: ' + str(i[3]) + ']'})

        else:
            data = {'0': '--no subject found--'}

    else:

        data = {'0': '--no subject found--'}

    return JsonResponse(data)


def benchmarkTesting(request, pk):
    
    students = Student.objects.filter(Semester_id = Semester.objects.get(id = pk))
    return HttpResponse('<br/>'.join(student.Enrollment for student in students))


def handler400(request, exception):
    return render(request, 'Resources/400.html', status=400)

def handler403(request, exception):
    return render(request, 'Resources/403.html', status=403)

def handler404(request, exception):
    return render(request, 'Resources/404.html', status=404)
    
def handler500(request):
    return render(request, 'Resources/500.html', status=500)