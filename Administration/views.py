

from django.http import response, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from .forms import SendGridAPIForm, PermissionForm, TwilioAPIForm, StudentSetup, FacultySetup, StudentUpdate, FacultyUpdate
from django.contrib.auth.models import User
from Resources.models import SendGridAPIKey, TwilioAPIKey
from django.contrib.auth.models import Permission
from Resources.models import *
from django.urls import reverse
from django.contrib.auth import logout
import base64

@permission_required('Resources.student_rights')
def Inventory_Manage(request):
    return render(request, 'Administration/Inventory_Manage.html')

def userTypeIdentify(userEmail):

    if Student.objects.filter(Email = userEmail).count() > 0:
        return 0
    elif Faculty.objects.filter(Email = userEmail).count() > 0:
        return 1
    else:
        return 2

def initialStudent(userEmail):
    
    form = StudentUpdate()

    try:
        form = StudentUpdate(initial={'First': Student.objects.get(Email = userEmail).First, 'Last': Student.objects.get(Email = userEmail).Last, 'Contact': Student.objects.get(Email = userEmail).Contact, 'Category': Student.objects.get(Email = userEmail).Category, 'DOB': Student.objects.get(Email = userEmail).DOB, 'Address': Student.objects.get(Email = userEmail).Address})
    except:
        pass

    return form

def initialFaculty(userEmail):
    
    form = FacultyUpdate()

    try:
        form = FacultyUpdate(initial={'First': Faculty.objects.get(Email = userEmail).First, 'Last': Faculty.objects.get(Email = userEmail).Last, 'Contact': Faculty.objects.get(Email = userEmail).Contact, 'Post': Faculty.objects.get(Email = userEmail).Post, 'Qualification': Faculty.objects.get(Email = userEmail).Qualification, 'Joining': Faculty.objects.get(Email = userEmail).JoiningDate, 'DOB': Faculty.objects.get(Email = userEmail).DOB, 'Address': Faculty.objects.get(Email = userEmail).Address})
    except:
        pass

    return form

@login_required()
def dashboard(request):

    if Faculty.objects.filter(Email=request.user.email).count() > 0:
        if Faculty.objects.filter(Email=request.user.email).first().Verified == False:
            return redirect(reverse('Administration:Verification'))
        else:
            
            u = User.objects.get(email = request.user.email)
            try:
                permission = Permission.objects.get(name='Manage Attendance')
                u.user_permissions.add(permission)
            except:
                pass
            try:
                permission = Permission.objects.get(name='Manage Marks')
                u.user_permissions.add(permission)
            except:
                pass

            return render(request, 'Administration/Dashboard.html', {})

    elif Student.objects.filter(Email=request.user.email).count() > 0:
        return render(request, 'Administration/Dashboard.html', {})

    elif User.objects.get(username=request.user.username).is_superuser == 1:
        return render(request, 'Administration/Dashboard.html', {})

    else:
        return redirect(reverse('Administration:Setup'))


@login_required()
def profile(request):

    apiform = SendGridAPIForm()
    permissionForm = PermissionForm()
    twilioForm = TwilioAPIForm()

    return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm, 'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': '', 'Message2': '', 'Visiblity2': 'invisible', 'color2': 'success'})

@permission_required('Resources.api_rights')
def twilioAPI(request):
    
    permissionForm = PermissionForm()
    apiform = SendGridAPIForm()

    if request.method == 'POST':

        twilioForm = TwilioAPIForm(request.POST)

        if twilioForm.is_valid():

            TwilioAPIKey.objects.all().delete()
            TwilioAPIKey(SID=twilioForm.cleaned_data['SID'], Token=twilioForm.cleaned_data['Token'], Notify=twilioForm.cleaned_data['Notify']).save()

            return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': 'API Updated!', 'Visiblity6': 'visible', 'color6': 'success', 'twilioForm': twilioForm, 'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': '', 'Message2': 'Changed Successfully!', 'Visiblity2': 'invisible', 'color2': 'success'})

    twilioForm = TwilioAPIForm()

    return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm,'Departments': Department.objects.all(),'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': '', 'Message2': '', 'Visiblity2': 'invisible', 'color2': 'success'})


@permission_required('Resources.api_rights')
def apiProfile(request):

    permissionForm = PermissionForm()
    twilioForm = TwilioAPIForm()

    if request.method == 'POST':

        apiform = SendGridAPIForm(request.POST)

        if apiform.is_valid():

            SendGridAPIKey.objects.all().delete()
            SendGridAPIKey(Key=apiform.cleaned_data['Key']).save()

            return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm,'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': '', 'Message2': 'Changed Successfully!', 'Visiblity2': 'visible', 'color2': 'success'})

    apiform = SendGridAPIForm()

    return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm,'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': '', 'Message2': '', 'Visiblity2': 'invisible', 'color2': 'success'})


@permission_required('Resources.permission_rights')
def permissionForm(request):

    apiform = SendGridAPIForm()
    twilioForm = TwilioAPIForm()

    invalidEmails = []

    if request.method == 'POST':

        permissionForm = PermissionForm(request.POST)

        if permissionForm.is_valid():

            for e in str(permissionForm.cleaned_data['FacultyEmail']).split(","):

                skip = False

                try:
                    u = User.objects.get(email=e.strip(" "))
                except:
                    invalidEmails.append(e.strip(" "))
                    skip = True

                if skip == False:
                    if permissionForm.cleaned_data['Department'] == True:
                        permission = Permission.objects.get(name='Manage Department and Courses')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Manage Department and Courses')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Faculty'] == True:
                        permission = Permission.objects.get(name='Manage Faculties')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Manage Faculties')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Student'] == True:
                        permission = Permission.objects.get(name='Manage Students')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Manage Students')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Attendance'] == True:
                        permission = Permission.objects.get(name='Manage Attendance')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Manage Attendance')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['ViewAttendance'] == True:
                        permission = Permission.objects.get(name='View Attendance')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='View Attendance')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Marks'] == True:
                        permission = Permission.objects.get(name='Manage Marks')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Manage Marks')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['ViewMarks'] == True:
                        permission = Permission.objects.get(name='View Marks')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='View Marks')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Emails'] == True:
                        permission = Permission.objects.get(name='Send Emails')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Send Emails')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['SMS'] == True:
                        permission = Permission.objects.get(name='Send SMS')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Send SMS')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['API'] == True:
                        permission = Permission.objects.get(name='Add Send Grid and Twilio API Key')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Add Send Grid and Twilio API Key')
                        u.user_permissions.remove(permission)

                    if permissionForm.cleaned_data['Permission'] == True:
                        permission = Permission.objects.get(name='Grant Permissions')
                        u.user_permissions.add(permission)
                    else:
                        permission = Permission.objects.get(name='Grant Permissions')
                        u.user_permissions.remove(permission)

            return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm, 'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': 'Permissions Updated!', 'Visiblity': 'visible', 'color': 'success', 'invalidEmails': invalidEmails if len(invalidEmails) > 0 else '', 'Message2': '', 'Visiblity2': 'invisible', 'color2': 'success'})

    permissionForm = PermissionForm()

    return render(request, 'Administration/Profile.html', {'usertype': userTypeIdentify(request.user.email), 'studentForm': initialStudent(request.user.email), 'facultyForm': initialFaculty(request.user.email), 'Message6': '', 'Visiblity6': 'invisible', 'color6': 'danger', 'twilioForm': twilioForm, 'Departments': Department.objects.all(), 'apiform': apiform, 'permissionForm': permissionForm, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'invalidEmails': invalidEmails, 'Message2': '', 'Visiblity2': 'invisible', 'color2': 'success'})


def verification(request):

    u = User.objects.get(username=request.user.username)

    first = u.first_name
    last = u.last_name
    email = u.email
    facultyid = Faculty.objects.filter(Email=request.user.email).first().FacultyCollegeID

    logout(request)

    return render(request, 'Administration/Verification.html', {'first': first, 'last': last, 'email': email, 'facultyid': facultyid})


@login_required
def setup(request):

    u = User.objects.get(username=request.user.username)
    studentForm = StudentSetup()
    facultyForm = FacultySetup()

    if request.method == 'POST':

        checkFaculty = request.POST.get('isFaculty', '')
        checkStudent = request.POST.get('isStudent', '')

        if checkFaculty == 'True':

            updateInfo = User.objects.filter(username=request.user.username)

            facultyForm = FacultySetup(request.POST, request.FILES)

            if facultyForm.is_valid():
                updateInfo.update(first_name=facultyForm.cleaned_data['First'], last_name=facultyForm.cleaned_data['Last'])

                if not Faculty.objects.filter(Email=request.user.email).count() > 0 and not Faculty.objects.filter(FacultyCollegeID=facultyForm.cleaned_data['EmployeeID']).count() > 0:

                    # File
                    data = request.FILES['Photo'].read()
                    encoded_file = base64.b64encode(data).decode()

                    Faculty(First = facultyForm.cleaned_data['First'], Last = facultyForm.cleaned_data['Last'], Email = request.user.email, Post = facultyForm.cleaned_data['Post'], Qualification = facultyForm.cleaned_data['Qualification'], FacultyCollegeID = facultyForm.cleaned_data['EmployeeID'], Contact = facultyForm.cleaned_data['Contact'], Address = facultyForm.cleaned_data['Address'], Photo = encoded_file, DOB = facultyForm.cleaned_data['DOB'], JoiningDate = facultyForm.cleaned_data['Joining'], Verified = False).save()

                    #emailPermission = Permission.objects.get(name='Send Emails')
                    manageMarks = Permission.objects.get(name='Manage Marks')
                    #viewMarks = Permission.objects.get(name='View Marks')
                    attendancePermission = Permission.objects.get(name='Manage Attendance')
                    #attendanceViewPermission = Permission.objects.get(name='View Attendance')

                    #updateInfo.first().user_permissions.add(emailPermission)
                    updateInfo.first().user_permissions.add(attendancePermission)
                    #updateInfo.first().user_permissions.add(attendanceViewPermission)
                    updateInfo.first().user_permissions.add(manageMarks)
                    #updateInfo.first().user_permissions.add(viewMarks)

                    return redirect(reverse('Administration:Dashboard'))

        elif checkStudent == 'True':

            updateInfo = User.objects.filter(username=request.user.username)

            studentForm = StudentSetup(request.POST, request.FILES)

            if studentForm.is_valid():
                updateInfo.update(first_name=studentForm.cleaned_data['First'], last_name=studentForm.cleaned_data['Last'])

                if not Student.objects.filter(Email=request.user.email).count() > 0 and not Student.objects.filter(Enrollment=studentForm.cleaned_data['Enrollment']).count() > 0:

                    # File
                    data = request.FILES['Photo'].read()
                    encoded_file = base64.b64encode(data).decode()

                    Student(First = studentForm.cleaned_data['First'], Last = studentForm.cleaned_data['Last'], Email = request.user.email, Enrollment = studentForm.cleaned_data['Enrollment'], Contact = studentForm.cleaned_data['Contact'], DOB = studentForm.cleaned_data['DOB'], Category = studentForm.cleaned_data['Category'], Address = studentForm.cleaned_data['Address'], Photo = encoded_file, Department_id = Department.objects.get(id = request.POST.get('department4', '')), Course_id = Course.objects.get(id = request.POST.get('course4', '')), Branch_id = Branch.objects.get(id = request.POST.get('branch4', '')), Semester_id = Semester.objects.get(id = request.POST.get('semester4', ''))).save()
                    
                    '''
                    attendanceViewPermission = Permission.objects.get(name='View Attendance')
                    viewMarks = Permission.objects.get(name='View Marks')
                    updateInfo.first().user_permissions.add(attendanceViewPermission)
                    updateInfo.first().user_permissions.add(viewMarks)
                    '''
                    
                    return redirect(reverse('Administration:Dashboard'))

        else:
            return render(request, 'Administration/Setup.html', {'Departments': Department.objects.all(), 'Visiblity': 'visible'})

    return render(request, 'Administration/Setup.html', {'StudentForm': studentForm, 'FacultyForm': facultyForm, 'Departments': Department.objects.all(), 'Visiblity': 'invisible'})

@login_required
def checkEnroll(request):

    if Student.objects.filter(Enrollment = request.GET.get('Enroll', 0)).count() > 0:
        return JsonResponse({'Error': 'Exist'}, safe=False)
    else:
        return JsonResponse({'Success': 'Not Exist'}, safe=False)

@login_required
def checkEmployee(request):

    if Faculty.objects.filter(FacultyCollegeID = request.GET.get('Employee', 0)).count() > 0:
        return JsonResponse({'Error': 'Exist'}, safe=False)
    else:
        return JsonResponse({'Success': 'Not Exist'}, safe=False)


@login_required
def updateStudent(request):

    if request.method == 'POST':

        studentForm = StudentUpdate(request.POST, request.FILES)

        if studentForm.is_valid():

            student = Student.objects.get(Email = request.user.email)

            if studentForm.cleaned_data.get('First', '') != '':
                student.First = studentForm.cleaned_data['First']
            if studentForm.cleaned_data.get('Last', '') != '':
                student.Last = studentForm.cleaned_data['Last']
            if studentForm.cleaned_data.get('Contact', '') != '':
                student.Contact = studentForm.cleaned_data['Contact']
            if studentForm.cleaned_data.get('DOB', '') != '':
                student.DOB = studentForm.cleaned_data['DOB']
            if studentForm.cleaned_data.get('Category', '') != '':
                student.Category = studentForm.cleaned_data['Category']
            if studentForm.cleaned_data.get('Address', '') != '':
                student.Address = studentForm.cleaned_data['Address']
            if request.FILES.get('Photo', None) != None:
                data = request.FILES['Photo'].read()
                encoded_file = base64.b64encode(data).decode()
                student.Photo = encoded_file

            student.save()
            
    return redirect(reverse('Administration:Profile'))

@login_required
def updateFaculty(request):

    if request.method == 'POST':

        facultyForm = FacultyUpdate(request.POST, request.FILES)

        if facultyForm.is_valid():
            
            faculty = Faculty.objects.get(Email = request.user.email)

            if facultyForm.cleaned_data.get('First', '') != '':
                faculty.First = facultyForm.cleaned_data['First']
            if facultyForm.cleaned_data.get('Last', '') != '':
                faculty.Last = facultyForm.cleaned_data['Last']
            if facultyForm.cleaned_data.get('Post', '') != '':
                faculty.Post = facultyForm.cleaned_data['Post']
            if facultyForm.cleaned_data.get('Qualification', '') != '':
                faculty.Qualification = facultyForm.cleaned_data['Qualification']
            if facultyForm.cleaned_data.get('Contact', '') != '':
                faculty.Contact = facultyForm.cleaned_data['Contact']
            if facultyForm.cleaned_data.get('Address', '') != '':
                faculty.Address = facultyForm.cleaned_data['Address']
            if facultyForm.cleaned_data.get('DOB', '') != '':
                faculty.DOB = facultyForm.cleaned_data['DOB']
            if facultyForm.cleaned_data.get('Joining', '') != '':
                faculty.JoiningDate = facultyForm.cleaned_data['Joining']
            if request.FILES.get('Photo', None) != None:
                data = request.FILES['Photo'].read()
                encoded_file = base64.b64encode(data).decode()
                faculty.Photo = encoded_file

            faculty.save()
        
    return redirect(reverse('Administration:Profile'))