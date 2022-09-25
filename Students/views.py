from io import StringIO
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User
from .forms import SearchForm, StudentCSV
from Resources.models import *
from django.core.paginator import Paginator
from django.urls import reverse
import csv
import datetime
# Create your views here.


@permission_required('Resources.student_rights')
def manage(request):

    return render(request, 'Students/Manage.html', {'Search': SearchForm(), 'StudentCSV': StudentCSV(), 'Departments': Department.objects.all()})


@permission_required('Resources.student_rights')
def search(request):

    if request.method == 'POST':

        searchForm = SearchForm(request.POST)

        if searchForm.is_valid():

            if searchForm.cleaned_data['First'] != '' and searchForm.cleaned_data['Last'] != '':
                users_list = Student.objects.filter(First__startswith=searchForm.cleaned_data['First'], Last__startswith=searchForm.cleaned_data['Last'])

            elif searchForm.cleaned_data['First'] != '':
                users_list = Student.objects.filter(First__startswith=searchForm.cleaned_data['First'])

            elif searchForm.cleaned_data['Last'] != '':
                users_list = Student.objects.filter(Last__startswith=searchForm.cleaned_data['Last'])

            elif searchForm.cleaned_data['Email'] != '':
                users_list = Student.objects.filter(Email=searchForm.cleaned_data['Email'])

            elif searchForm.cleaned_data['Contact'] != '':
                users_list = Student.objects.filter(Contact=searchForm.cleaned_data['Contact'])

            elif searchForm.cleaned_data['Enrollment'] != '':
                users_list = Student.objects.filter(Enrollment=searchForm.cleaned_data['Enrollment'])
            else:
                return render(request, 'Students/Manage.html', {'Search': SearchForm()})
                
            total = users_list.count()
            paginator = Paginator(users_list, 10)  # Show 10 contacts per page
            page = request.GET.get('page')
            users = paginator.get_page(page)

            return render(request, 'Students/Search.html', {'users': users, 'total': total})

    return render(request, 'Students/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'StudentCSV': StudentCSV()})


@permission_required('Resources.student_rights')
def remove(request):

    if request.method == 'POST':

        if request.POST.get('student_remove', False) != False:
            s = Student.objects.filter(Enrollment=request.POST.get('student_remove', False))

            if s.count() > 0:
                
                try:
                    User.objects.get(email=s.first().Email).delete()
                except:
                    pass

                s.delete()
                return render(request, 'Students/Manage.html', {'Departments': Department.objects.all(), 'Message': 'Student Account/Details Removed!', 'visiblity': 'visible', 'color': 'success', 'Search': SearchForm(), 'StudentCSV': StudentCSV()})
            else:
                return render(request, 'Students/Manage.html', {'Departments': Department.objects.all(), 'Message': 'Student not found', 'visiblity': 'visible', 'color': 'danger', 'Search': SearchForm(), 'StudentCSV': StudentCSV()})

    return render(request, 'Students/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'StudentCSV': StudentCSV()})


@permission_required('Resources.student_rights')
def studentAdd(request):

    Form = StudentCSV()

    counter = 0
    successList = []
    enrollmentFailedList = []
    emailFailedList = []

    if request.method == 'POST':

        Form = StudentCSV(request.POST, request.FILES)

        if Form.is_valid():

            file_object = request.FILES.get('CSV', None)
            file = file_object.read().decode('utf-8')
            csv_data = csv.reader(StringIO(file), delimiter=',')

            for row in csv_data:
                if counter != 0:

                    if Student.objects.filter(Enrollment = str(row[3])).count() > 0:
                        enrollmentFailedList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0])) # Enrollment Exist
                    else:
                        if Student.objects.filter(Email = str(row[0])).count() > 0:
                            emailFailedList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0])) # Email Exist
                        else:
                            department = Department.objects.get(Name = str(row[8]))
                            course = Course.objects.get(Name = str(row[9]), Department_id = department)
                            branch = Branch.objects.get(Name = str(row[10]), Course_id = course)
                            semester = Semester.objects.get(Name = str(row[11]), Branch_id = branch)

                            date_time_obj = datetime.datetime.strptime(str(row[4]), '%d-%m-%Y')

                            Student(First = str(row[1]), Last = str(row[2]), Email = str(row[0]), Enrollment = str(row[3]), Contact = str(row[6]), DOB = date_time_obj.date(), Category = str(row[5]), Address = str(row[7]), Department_id = department, Course_id = course, Branch_id = branch, Semester_id = semester).save()
                            successList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0]))

                counter = counter + 1


    return render(request, 'Students/Accounts.html', {'successList': successList, 'lensuccessList': len(successList), 'enrollmentFailedList': enrollmentFailedList, 'lenenrollmentFailedList': len(enrollmentFailedList), 'emailFailedList': emailFailedList, 'lenemailFailedList': len(emailFailedList), 'TotalCandidates': (int(counter) - 1)})


@permission_required('Resources.student_rights')
def changeSemester(request):

    if request.method == 'POST':

        semesterSource = Semester.objects.get(id = request.POST.get('semester4', 0))
        semesterDestination = Semester.objects.get(id = request.POST.get('semester5', 0))

        sourceStudent = Student.objects.filter(Semester_id = semesterSource)

        branchSource = Branch.objects.get(id = semesterSource.Branch_id.id)
        courseSource = Course.objects.get(id = branchSource.Course_id.id)
        departmentSource = Department.objects.get(id = courseSource.Department_id.id)

        branchDestination = Branch.objects.get(id = semesterDestination.Branch_id.id)
        courseDestination = Course.objects.get(id = branchDestination.Course_id.id)
        departmentDestination = Department.objects.get(id = courseDestination.Department_id.id)

        for student in sourceStudent:
            student.Department_id = departmentDestination
            student.Course_id = courseDestination
            student.Branch_id = branchDestination
            student.Semester_id = semesterDestination
            student.save()

    return render(request, 'Students/Change.html', {'TotalCandidates': len(sourceStudent), 'sd': departmentSource.Name, 'sc': courseSource.Name, 'sb': branchSource.Name, 'ss': semesterSource.Name, 'dd': departmentDestination.Name, 'dc': courseDestination.Name, 'db': branchDestination.Name, 'ds': semesterDestination.Name})
    

