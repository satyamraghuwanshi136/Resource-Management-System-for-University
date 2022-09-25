

from django.contrib.auth import decorators
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls.base import reverse_lazy
from Resources.models import *
from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpResponse
import datetime


def getStudentSubjects(studentEmail):

    studentSubject = []

    try:
        studentSubject = Subject.objects.filter(Semester_id = Student.objects.get(Email = studentEmail).Semester_id.id)
    except:
        studentSubject = []

    return studentSubject

def getFacultySubjects(facultyEmail):

    facultySubject = []

    try:
        facultySubject = FacultyAssigned.objects.filter(Faculty_id = Faculty.objects.get(Email = facultyEmail))
    except:
        facultySubject = []

    return facultySubject

@login_required
def manage(request):

    return render(request, 'Attendance/Manage.html', {'FacultyAssigned': getFacultySubjects(request.user.email), 'StudentSubject': getStudentSubjects(request.user.email), 'Departments': Department.objects.all()})


@permission_required('Resources.attendance_rights')
def viewAttendance(request):

    if request.method == 'POST':
        
        subjectInstance = Subject.objects.get(id = request.POST.get('subjectselect', 0))

        studentList = Student.objects.filter(Semester_id = subjectInstance.Semester_id.id)

        attendanceDate =  datetime.datetime.strptime(str(request.POST.get('ViewDate', '1970-01-01')), '%Y-%m-%d')

        attendanceType = request.POST.get('type', '')

        if attendanceType == '':
            if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Theory_Lectures = True).count() > 0:
                if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Lab_Lectures = True).count() > 0:
                    return HttpResponseRedirect(str(reverse_lazy('Attendance:Multiple')) + '?subject=' + request.POST.get('subjectselect', 0) + '&date=' + str(request.POST.get('ViewDate', '1970-01-01')))

        finalList = []
        absentcount = 0
        presentcount = 0
        attTypeUpdate = attendanceType

        for student in studentList:

            if attendanceType == 'Theory':
                
                try:
                    attendenceInstance = Attendence.objects.get(Student_id = student, Subject_id = subjectInstance, Timestamp = attendanceDate, Theory_Lectures = True)

                    finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': 'Theory', 'Attendance': 'Present'})
                     
                    presentcount = presentcount + 1
                except:
                    finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': '-', 'Attendance': 'Absent'})
                    absentcount = absentcount + 1

            elif attendanceType == 'Lab':
                
                try:
                    attendenceInstance = Attendence.objects.get(Student_id = student, Subject_id = subjectInstance, Timestamp = attendanceDate, Lab_Lectures = True)

                    finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': 'Lab', 'Attendance': 'Present'})
                        
                    presentcount = presentcount + 1
                except:
                    finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': '-', 'Attendance': 'Absent'})
                    absentcount = absentcount + 1

            else:

                try:
                    attendenceInstance = Attendence.objects.get(Student_id = student, Subject_id = subjectInstance, Timestamp = attendanceDate)

                    if attendenceInstance.Theory_Lectures == True:
                        finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': 'Theory', 'Attendance': 'Present'})
                        presentcount = presentcount + 1
                        attTypeUpdate = 'Theory'
                    elif attendenceInstance.Lab_Lectures == True:
                        finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': 'Lab', 'Attendance': 'Present'})
                        presentcount = presentcount + 1
                        attTypeUpdate = 'Theory'
                    else:
                        finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': '-', 'Attendance': 'Absent'})
                        absentcount = absentcount + 1

                except:
                    finalList.append({'id': student.id, 'Name': str(student.First) + ' ' + str(student.Last), 'Enrollment': student.Enrollment, 'LectureType': '-', 'Attendance': 'Absent'})
                    absentcount = absentcount + 1

        return render(request, 'Attendance/View.html', {'subjectInstance': subjectInstance, 'AttType': attTypeUpdate, 'Date': request.POST.get('ViewDate', '1970-01-01'), 'finalList': finalList, 'total': len(finalList), 'presentcount': presentcount, 'absentcount': absentcount})

    return render(request, 'Attendance/Manage.html', {'StudentSubject': getStudentSubjects(request.user.email), 'Departments': Department.objects.all()})


@permission_required('Resources.attendance_rights')
def take(request):

    if request.method == 'GET':

        studentList = Student.objects.filter(Semester_id = Subject.objects.get(id = request.GET.get('subject', 0)).Semester_id.id)

        return render(request, 'Attendance/Take.html', {'StudentListLength': len(studentList), 'StudentList': studentList, 'subjectField': request.GET.get('subject', 0), 'subjectName': Subject.objects.get(id = request.GET.get('subject', 0)).Name})

    return render(request, 'Attendance/Manage.html', {'StudentSubject': getStudentSubjects(request.user.email), 'Departments': Department.objects.all()})

@permission_required('Resources.attendance_rights')
def takeSuccess(request):

    if request.method == 'POST':

        studentList = request.POST.getlist('studentchecks[]')

        subjectID = request.POST.get('attendanceSubject', 0)

        semesterInstance = Semester.objects.get(id = Subject.objects.get(id = subjectID).Semester_id.id)

        studentModelList = Student.objects.filter(Semester_id = semesterInstance)

        attendanceDate = datetime.datetime.strptime(str(request.POST.get('AttendanceDate', '1970-01-01')), '%Y-%m-%d')

        attendanceType = ''

        if request.POST.get('attendanceType', False) == '1':
            attendanceType = 'Theory Lecture'
        elif request.POST.get('attendanceType', False) == '2':
            attendanceType = 'Lab Lecture'

        for student in studentModelList:

            if student.Email in studentList:
                if attendanceType == 'Theory Lecture':

                    a = Attendence.objects.filter(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Timestamp = attendanceDate)
                    if a.count() > 0:
                        cs = a.first()
                        cs.Theory_Lectures = True
                        cs.save()
                    else:
                        Attendence(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Theory_Lectures = True, Timestamp = attendanceDate).save()

                else:
                    a = Attendence.objects.filter(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Timestamp = attendanceDate)
                    if a.count() > 0:
                        cs = a.first()
                        cs.Lab_Lectures = True
                        cs.save()
                    else:
                        Attendence(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Lab_Lectures = True, Timestamp = attendanceDate).save()
            else:
                a = Attendence.objects.filter(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Timestamp = attendanceDate)
                if a.count() > 0:
                    pass
                else:
                    Attendence(Student_id=Student.objects.get(Email = student.Email), Subject_id=Subject.objects.get(id = subjectID), Timestamp = attendanceDate).save()

        return render(request, 'Attendance/TakeSuccess.html', {'present': len(studentList), 'type': attendanceType, 'attdate': attendanceDate, 'attsubject': Subject.objects.get(id = subjectID).Name})

    return HttpResponse(status=403)


@login_required
def viewAttendanceStudent(request):
    
    if request.method == 'GET':

        subjectInstance = Subject.objects.get(id = request.GET.get('subject', 0))

        studentInstance = Student.objects.get(Email = request.user.email)

        attendance = Attendence.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance)

        theoryTotal = 0
        labTotal = 0

        if attendance.count() > 0:

            for att in attendance:
                if att.Theory_Lectures == True:
                    theoryTotal = theoryTotal + 1
                elif att.Lab_Lectures == True:
                    labTotal = labTotal + 1

        return render(request, 'Attendance/ViewStudent.html', {'Theory': theoryTotal, 'Lab': labTotal, 'SubjectInstance': subjectInstance, 'StudentInstance': studentInstance})
    
    return HttpResponse(status=403)


@permission_required('Resources.attendance_rights')
def multiple(request):

    if request.method == 'GET':

        subjectInstance = Subject.objects.get(id = request.GET.get('subject', 0))

        attendanceDate =  datetime.datetime.strptime(str(request.GET.get('date', '1970-01-01')), '%Y-%m-%d')

        if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Theory_Lectures = True).count() > 0:
            if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Lab_Lectures = True).count() > 0:
                return render(request, 'Attendance/Multiple.html', {'subject': subjectInstance.id, 'date': str(request.GET.get('date', '1970-01-01'))})
            
    return HttpResponse(status=403)


@permission_required('Resources.attendance_rights')
def checkMultiple(request):
    
    data = {'Success': ''}

    if request.method == 'POST':

        subjectInstance = Subject.objects.get(id = request.POST.get('currentSubject', 0))

        attendanceDate =  datetime.datetime.strptime(str(request.POST.get('currentDate', '1970-01-01')), '%Y-%m-%d')

        lectureType = request.POST.get('currentLecture', '')

        if lectureType == 'Theory':
            if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Theory_Lectures = True).count() > 0:
                data = {'Error': ''}
        else:
            if Attendence.objects.filter(Subject_id = subjectInstance, Timestamp = attendanceDate, Lab_Lectures = True).count() > 0:
                data = {'Error': ''}

    return JsonResponse(data)



@permission_required('Resources.attendance_view_rights')
def generateReport(request):

    if request.method == 'POST':

        semesterInstance = Semester.objects.get(id = request.POST.get('semester2', 0))

        fromDate =  datetime.datetime.strptime(str(request.POST.get('ViewDateFrom', '1970-01-01')), '%Y-%m-%d')

        toDate =  datetime.datetime.strptime(str(request.POST.get('ViewDateTo', '1970-01-01')), '%Y-%m-%d')

        reportType = int(request.POST.get('reportType', 0))

        ShortlistPercentage = int(request.POST.get('ShortlistPercentage', 0))

        shortlistType = int(request.POST.get('shortlistType', 0))




        studentListInstance = Student.objects.filter(Semester_id = semesterInstance)

        subjectInstance = Subject.objects.filter(Semester_id = semesterInstance)

        branchInstance = Branch.objects.get(id = semesterInstance.Branch_id.id)

        courseName = Course.objects.get(id = branchInstance.Course_id.id).Name



        subjectList = []
        marksList = []
        studentMarksList = []

        for subject in subjectInstance:
            subjectList.append({'Name': subject.Name})


        for student in studentListInstance:

            marksList = []
            shortlisted = False

            for subject in subjectInstance:

                theory = 0
                lab = 0
                
                attendanceInstance = Attendence.objects.filter(Student_id = student, Subject_id = subject, Timestamp__range=[fromDate, toDate])

                theoryTotal = attendanceInstance.count()
                labTotal = attendanceInstance.count()

                if reportType == 2:
                    theoryTotal = subject.Theory_Lectures
                    labTotal = subject.Lab_Lectures


                for i in attendanceInstance:
                    if i.Theory_Lectures == True:
                        theory = theory + 1
                    if i.Lab_Lectures == True:
                        lab = lab + 1

                att = round((((theory + lab) / (theoryTotal + labTotal)) * 100), 2)

                theoryPercentage = round(((theory / theoryTotal) * 100), 2)
                labPercentage = round(((lab / labTotal) * 100), 2)

                marksList.append({'Email': student.Email, 'Name': str(student.First) + " " + str(student.Last), 'Enrollment': student.Enrollment, 'Attendance': att, 'theory': theory, 'lab': lab, 'theoryTotal': theoryTotal, 'labTotal': labTotal, 'theoryPercentage': theoryPercentage, 'labPercentage': labPercentage})
                
            if shortlistType == 2:
                for eachsubject in marksList:
                    if eachsubject['theoryPercentage'] < ShortlistPercentage or eachsubject['labPercentage'] < ShortlistPercentage:
                        shortlisted = True
                        break

                if shortlisted:
                    studentMarksList.append(marksList)
            else:
                studentMarksList.append(marksList)

        return render(request, 'Attendance/Report.html', {'ShortlistPercentage': ShortlistPercentage,'shortlistType': shortlistType, 'StudentMarksList': studentMarksList, 'SubjectList': subjectList, 'CourseName': courseName, 'SemesterName': semesterInstance.Name})

    return HttpResponse(status=403)

@permission_required('Resources.attendance_rights')
def updateAttendance(request):

    data = {'Error': ''}
    
    if request.method == 'POST':
        currentSubject = request.POST.get('currentSubject', 0)
        currentStudent = request.POST.get('currentStudent', 0)
        currentDate = datetime.datetime.strptime(str(request.POST.get('currentDate', '1970-01-01')), '%Y-%m-%d')
        currentLecture = request.POST.get('currentLecture', '')
        operationType = request.POST.get('operationType', '')

        subjectInstance = Subject.objects.get(id = currentSubject)
        studentInstance = Student.objects.get(id = currentStudent)

        try:

            a = Attendence.objects.get(Student_id = studentInstance, Subject_id = subjectInstance, Timestamp = currentDate)
            
            if currentLecture == 'Theory':

                if operationType == 'Present':
                    a.Theory_Lectures = True
                else:
                    a.Theory_Lectures = False

            else:
                
                if operationType == 'Present':
                    a.Lab_Lectures = True
                else:
                    a.Lab_Lectures = False

            a.save()

            data = {'Success': ''}
        except:
            data = {'Error': ''}

    return JsonResponse(data)