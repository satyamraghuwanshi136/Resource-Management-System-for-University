

from io import StringIO
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
from .forms import *
from Resources.models import *
from django.contrib.auth.models import User
from Mails.sendgrid_api import SendMail
from django.core.paginator import Paginator
import csv
import datetime
from .forms import SearchForm, FacultyCSV
from django.conf import settings
# Create your views here.


@permission_required('Resources.faculty_rights')
def manage(request):

    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False)})


@permission_required('Resources.faculty_rights')
def approve(request):

    if request.method == 'POST':

        if request.POST.get('buttonApprove', False) != False:

            for i in request.POST.getlist('facultychecks[]'):
                faculty = Faculty.objects.get(Email=i)
                faculty.Verified = True
                faculty.save()

                messageStatus = SendMail(i, "Account Approval Request - SGSITS Attendance System", None, "Hello, your faculty account has been approved. You can login again at <a href='" + settings.PROJECT_WEBSITE_URL + "'>" + settings.PROJECT_WEBSITE_URL + "</a>")

            return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': 'Approved Selected Faculties!', 'visiblity': 'visible', 'color': 'success', 'listFaculties': Faculty.objects.filter(Verified=False)})

        elif request.POST.get('buttonReject', False) != False:

            for i in request.POST.getlist('facultychecks[]'):
                faculty = Faculty.objects.get(Email=i)
                faculty.delete()
                User.objects.get(email=i).delete()

                messageStatus = SendMail(i, "Account Approval Request - SGSITS Attendance System", None, "Hello, your faculty account has been rejected by the admin. Visit college department for futher information.")

            return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': 'Rejected Selected Faculties!', 'visiblity': 'visible', 'color': 'success', 'listFaculties': Faculty.objects.filter(Verified=False)})

    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False)})

@permission_required('Resources.faculty_rights')
def remove(request):

    if request.method == 'POST':

        if request.POST.get('faculty_remove', False) != False:
            a = Faculty.objects.filter(FacultyCollegeID=request.POST.get('faculty_remove', False))

            if a.count() > 0:
                
                try:
                    User.objects.get(email=a.first().Email).delete()
                except:
                    pass
                
                a.delete()
                return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'Message2': 'Faculty Removed', 'visiblity2': 'visible', 'color2': 'success', 'listFaculties': Faculty.objects.filter(Verified=False)})
            else:
                return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'Message2': 'Faculty not found', 'visiblity2': 'visible', 'color2': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False)})

    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'Message2': '', 'visiblity2': 'invisible', 'color2': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False)})


@permission_required('Resources.faculty_rights')
def search(request):

    if request.method == 'POST':

        searchForm = SearchForm(request.POST)

        if searchForm.is_valid():

            if searchForm.cleaned_data['First'] != '' and searchForm.cleaned_data['Last'] != '':
                users_list = Faculty.objects.filter(First__startswith=searchForm.cleaned_data['First'], Last__startswith=searchForm.cleaned_data['Last'])

            elif searchForm.cleaned_data['First'] != '':
                users_list = Faculty.objects.filter(First__startswith=searchForm.cleaned_data['First'])

            elif searchForm.cleaned_data['Last'] != '':
                users_list = Faculty.objects.filter(Last__startswith=searchForm.cleaned_data['Last'])

            elif searchForm.cleaned_data['Email'] != '':
                users_list = Faculty.objects.filter(Email=searchForm.cleaned_data['Email'])

            elif searchForm.cleaned_data['Contact'] != '':
                users_list = Faculty.objects.filter(Contact=searchForm.cleaned_data['Contact'])

            elif searchForm.cleaned_data['FacultyCollegeID'] != '':
                users_list = Faculty.objects.filter(Enrollment=searchForm.cleaned_data['FacultyCollegeID'])
            else:
                return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm()})
                
            total = users_list.count()
            paginator = Paginator(users_list, 10)  # Show 10 contacts per page
            page = request.GET.get('page')
            users = paginator.get_page(page)

            return render(request, 'Faculty/Search.html', {'users': users, 'total': total})

    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV()})



@permission_required('Resources.faculty_rights')
def facultyAdd(request):

    Form = FacultyCSV()

    counter = 0
    successList = []
    enrollmentFailedList = []
    emailFailedList = []

    if request.method == 'POST':

        Form = FacultyCSV(request.POST, request.FILES)

        if Form.is_valid():

            file_object = request.FILES.get('CSV', None)
            file = file_object.read().decode('utf-8')
            csv_data = csv.reader(StringIO(file), delimiter=',')

            for row in csv_data:
                if counter != 0:

                    if Faculty.objects.filter(FacultyCollegeID = str(row[3])).count() > 0:
                        enrollmentFailedList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0])) # Enrollment Exist
                    else:
                        if Faculty.objects.filter(Email = str(row[0])).count() > 0:
                            emailFailedList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0])) # Email Exist
                        else:
                            date_time_obj = datetime.datetime.strptime(str(row[7]), '%d-%m-%Y') # Date of Birth
                            date_time_obj2 = datetime.datetime.strptime(str(row[4]), '%d-%m-%Y') # Date of Joining

                            Faculty(First = str(row[1]), Last = str(row[2]), Email = str(row[0]), FacultyCollegeID = str(row[3]), Contact = str(row[8]), DOB = date_time_obj.date(), JoiningDate = date_time_obj2.date(), Address = str(row[9]), Post = str(row[5]), Qualification = str(row[6]), Verified = True).save()
                            successList.append(str(row[1]) + " " + str(row[2]) + " - " + str(row[3]) + " - " + str(row[0]))

                counter = counter + 1


    return render(request, 'Faculty/Accounts.html', {'successList': successList, 'lensuccessList': len(successList), 'enrollmentFailedList': enrollmentFailedList, 'lenenrollmentFailedList': len(enrollmentFailedList), 'emailFailedList': emailFailedList, 'lenemailFailedList': len(emailFailedList), 'TotalCandidates': (int(counter) - 1)})


@permission_required('Resources.faculty_rights')
def facultyAssign(request):

    if request.method == 'POST':

        if request.POST.get('Button_Assign', False) != False:

            if request.POST.get('faculty_assign_employee', '') != '':
                a = Faculty.objects.filter(FacultyCollegeID=request.POST.get('faculty_assign_employee', ''))

                if a.count() > 0:
                    FacultyAssigned(Faculty_id = a.first(), Subject_id = Subject.objects.get(id = request.POST.get('subject5', ''))).save()
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject Assigned Successfully', 'visiblity8': 'visible', 'color8': 'success'})
                else:
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Employee ID not found', 'visiblity8': 'visible', 'color8': 'danger'})

            elif request.POST.get('faculty_assign_email', '') != '':
                a = Faculty.objects.filter(Email = request.POST.get('faculty_assign_email', ''))

                if a.count() > 0:
                    FacultyAssigned(Faculty_id = a.first(), Subject_id = Subject.objects.get(id = request.POST.get('subject5', ''))).save()
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject Assigned Successfully', 'visiblity8': 'visible', 'color8': 'success'})
                else:
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Faculty Email not found', 'visiblity8': 'visible', 'color8': 'danger'})
        else:

            if request.POST.get('faculty_assign_employee', '') != '':
                a = Faculty.objects.filter(FacultyCollegeID=request.POST.get('faculty_assign_employee', ''))

                if a.count() > 0:
                    f = FacultyAssigned.objects.filter(Faculty_id = a.first(), Subject_id = Subject.objects.get(id = request.POST.get('subject5', '')))
                    if f.count() > 0:
                        f.first().delete()
                        return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject Dismissed Successfully', 'visiblity8': 'visible', 'color8': 'success'})
                    else:
                        return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject is not assigned to this faculty', 'visiblity8': 'visible', 'color8': 'danger'})
                else:
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Employee ID not found', 'visiblity8': 'visible', 'color8': 'danger'})

            elif request.POST.get('faculty_assign_email', '') != '':
                a = Faculty.objects.filter(Email = request.POST.get('faculty_assign_email', ''))

                if a.count() > 0:
                    f = FacultyAssigned.objects.filter(Faculty_id = a.first(), Subject_id = Subject.objects.get(id = request.POST.get('subject5', '')))
                    if f.count() > 0:
                        f.first().delete()
                        return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject Dismissed Successfully', 'visiblity8': 'visible', 'color8': 'success'})
                    else:
                        return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Subject is not assigned to this faculty', 'visiblity8': 'visible', 'color8': 'danger'})
                else:
                    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': 'Faculty Email not found', 'visiblity8': 'visible', 'color8': 'danger'})
       
    return render(request, 'Faculty/Manage.html', {'Departments': Department.objects.all(), 'Search': SearchForm(), 'FacultyCSV': FacultyCSV(), 'Message': '', 'visiblity': 'invisible', 'color': 'danger', 'listFaculties': Faculty.objects.filter(Verified=False), 'Message8': '', 'visiblity8': 'invisible', 'color8': 'danger'})
