

from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from Resources import models as resourceModels
from Resources.models import *
from django.http import QueryDict
from django.http import JsonResponse
# Create your views here.


@permission_required('Resources.department_course_rights')
def manage(request):

    return render(request, 'Department/Manage.html', {'Departments': resourceModels.Department.objects.all()})



@permission_required('Resources.department_course_rights')
def handleModel(request):

    data = {'0': 'Failed'}

    if request.method == 'PUT':

        add = QueryDict(request.body) # Getting body fields

        add_resource_text = add.get('resource')

        # Add Department
        if add_resource_text == 'Department':
            exist = False
            for singleInstance in Department.objects.all():
                if str(singleInstance.Name).lower() == str(add.get('departtext')).lower(): # Compare all department text by looping
                    exist = True # setting trigger to True
                    data = {'Error': ''}
                    break
            
            if not exist:
                Department(Name=add.get('departtext')).save() # saving department only if trigger is still False
                data = {'Success': ''}

        # Add Course
        if add_resource_text == 'Course':
            objectInstance = Department.objects.filter(id=add.get('referenceFieldValue')).first()
            exist = False
            for singleInstance in Course.objects.filter(Department_id=objectInstance):
                if str(singleInstance.Name).lower() == str(add.get('departtext')).lower(): # Compare all courses text by looping
                    exist = True # setting trigger to True
                    data = {'Error': ''}
                    break

            if not exist:
                Course(Name=add.get('departtext'), Department_id=objectInstance).save() # saving course only if trigger is still False
                data = {'Success': ''}

        # Add Branch
        if add_resource_text == 'Branch':
            objectInstance = Course.objects.filter(id=add.get('referenceFieldValue')).first()
            exist = False
            for singleInstance in Branch.objects.filter(Course_id=objectInstance):
                if str(singleInstance.Name).lower() == str(add.get('departtext')).lower():
                    exist = True
                    data = {'Error': ''}
                    break

            if not exist:
                Branch(Name=add.get('departtext'), Course_id=objectInstance).save()
                data = {'Success': ''}

        # Add Semester
        if add_resource_text == 'Semester':
            objectInstance = Branch.objects.filter(id=add.get('referenceFieldValue')).first()
            exist = False
            for singleInstance in Semester.objects.filter(Branch_id=objectInstance):
                if str(singleInstance.Name).lower() == str(add.get('departtext')).lower():
                    exist = True
                    data = {'Error': ''}
                    break

            if not exist:
                Semester(Name=add.get('departtext'), Branch_id=objectInstance).save()
                data = {'Success': ''}

        # Add Subject
        if add_resource_text == 'Subject':
            objectInstance = Semester.objects.filter(id=add.get('semesterReferenceVariable')).first()
            exist = False
            for singleInstance in Subject.objects.filter(Semester_id=objectInstance):
                if str(singleInstance.Name).lower() == str(add.get('subjectTextVariable')).lower():
                    exist = True
                    data = {'Error': ''}
                    break

            if not exist:
                Subject(Name=add.get('subjectTextVariable'), Theory_Lectures=add.get('subjectTheoryVariable'), Lab_Lectures=add.get('subjectLabVariable'), Semester_id=objectInstance).save()
                data = {'Success': ''}
        




    if request.method == 'POST':

        update_resource_text = request.POST.get('resource', '')

        # Update Department
        if update_resource_text == 'Department':
            depart_id = request.POST.get('id', '')
            depart_text = request.POST.get('departtext', '')
            search_qs = Department.objects.filter(id=depart_id)

            if str(search_qs.first().Name).lower() == str(depart_text).lower():
                data = {'Error': ''}
            else:
                search_qs.update(Name=depart_text)
                data = {'Success': ''}

        # Update Course
        if update_resource_text == 'Course':
            depart_id = request.POST.get('id', '')
            depart_text = request.POST.get('departtext', '')
            search_qs = Course.objects.filter(id=depart_id)

            if str(search_qs.first().Name).lower() == str(depart_text).lower():
                data = {'Error': ''}
            else:
                search_qs.update(Name=depart_text)
                data = {'Success': ''}

        # Update Branch
        if update_resource_text == 'Branch':
            depart_id = request.POST.get('id', '')
            depart_text = request.POST.get('departtext', '')
            search_qs = Branch.objects.filter(id=depart_id)
            
            if str(search_qs.first().Name).lower() == str(depart_text).lower():
                data = {'Error': ''}
            else:
                search_qs.update(Name=depart_text)
                data = {'Success': ''}

        # Update Semester
        if update_resource_text == 'Semester':
            depart_id = request.POST.get('id', '')
            depart_text = request.POST.get('departtext', '')
            search_qs = Semester.objects.filter(id=depart_id)
            
            if str(search_qs.first().Name).lower() == str(depart_text).lower():
                data = {'Error': ''}
            else:
                search_qs.update(Name=depart_text)
                data = {'Success': ''}

        # Update Subject
        if update_resource_text == 'Subject':
            depart_id = request.POST.get('subjectReferenceVariable', '')
            search_qs = resourceModels.Subject.objects.filter(id=depart_id)

            if str(search_qs.first().Name).lower() == str(request.POST.get('subjectTextVariable')).lower():
                if int(request.POST.get('subjectTheoryVariable')) == int(search_qs.first().Theory_Lectures):
                    if int(request.POST.get('subjectLabVariable')) == int(search_qs.first().Lab_Lectures):
                        data = {'Error': ''}
                    else:
                        search_qs.update(Name=request.POST.get('subjectTextVariable'), Theory_Lectures=request.POST.get('subjectTheoryVariable'), Lab_Lectures=request.POST.get('subjectLabVariable'))
                        data = {'Success': ''}
                else:
                    search_qs.update(Name=request.POST.get('subjectTextVariable'), Theory_Lectures=request.POST.get('subjectTheoryVariable'), Lab_Lectures=request.POST.get('subjectLabVariable'))
                    data = {'Success': ''}
            else:
                search_qs.update(Name=request.POST.get('subjectTextVariable'), Theory_Lectures=request.POST.get('subjectTheoryVariable'), Lab_Lectures=request.POST.get('subjectLabVariable'))
                data = {'Success': ''}
            




    if request.method == 'DELETE':

        delete = QueryDict(request.body)

        delete_resource_text = delete.get('resource')

        if delete_resource_text == 'Department':
            depart_id = delete.get('id')
            search_qs = resourceModels.Department.objects.filter(id=depart_id)
            search_qs.delete()

        if delete_resource_text == 'Course':
            depart_id = delete.get('id')
            search_qs = resourceModels.Course.objects.filter(id=depart_id)
            search_qs.delete()

        if delete_resource_text == 'Branch':
            depart_id = delete.get('id')
            search_qs = resourceModels.Branch.objects.filter(id=depart_id)
            search_qs.delete()

        if delete_resource_text == 'Semester':
            depart_id = delete.get('id')
            search_qs = resourceModels.Semester.objects.filter(id=depart_id)
            search_qs.delete()

        if delete_resource_text == 'Subject':
            depart_id = delete.get('subjectReferenceVariable')
            search_qs = resourceModels.Subject.objects.filter(id=depart_id)
            search_qs.delete()

        data = {'Success': ''}

    return JsonResponse(data)
