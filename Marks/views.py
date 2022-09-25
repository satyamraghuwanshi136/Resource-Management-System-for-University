
from django.http.response import HttpResponse
from django.shortcuts import render
from Resources.models import *
from django.contrib.auth.decorators import permission_required, login_required
from django.http import QueryDict
from django.http import JsonResponse
import csv
# Create your views here.

def manage(request):

    try:
        facultyAssigned = FacultyAssigned.objects.filter(Faculty_id = Faculty.objects.get(Email = request.user.email))
    except:
        facultyAssigned = []

    try:
        studentSubject = Subject.objects.filter(Semester_id = Student.objects.get(Email = request.user.email).Semester_id.id)
    except:
        studentSubject = []
    
    return render(request, 'Marks/Manage.html', {'FacultyAssigned': facultyAssigned, 'StudentSubject': studentSubject, 'Departments': Department.objects.all()})

@permission_required('Resources.marks_rights')
def cwTake(request):

    subjectObject = Subject.objects.get(id = request.GET.get('subject', 0))
    semester = Semester.objects.get(id = subjectObject.Semester_id.id)
    

    finalList = []
    theory = 0
    lab = 0

    id = 0
    name = ""
    enrollment = ""
    m1 = 0
    m1t = DEFAULT_MidTerm1Total
    m2 = 0
    m2t = DEFAULT_MidTerm2Total
    subjectid = subjectObject.id


    for student in Student.objects.filter(Semester_id = semester):

        id = student.id
        name = student.First + " " + student.Last
        enrollment = student.Enrollment
        
        if Marks.objects.filter(Student_id = student, Subject_id = subjectObject).count() > 0:
            m1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm1
            m1t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm1Total
            m2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm2
            m2t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm2Total
        else:
            m1 = 0
            m1t = DEFAULT_MidTerm1Total
            m2 = 0
            m2t = DEFAULT_MidTerm2Total

        theory = 0
        lab = 0

        for i in Attendence.objects.filter(Student_id = student, Subject_id = subjectObject):
            if i.Theory_Lectures == True:
                theory = theory + 1
            if i.Lab_Lectures == True:
                lab = lab + 1

        att = round((((theory + lab) / (int(subjectObject.Theory_Lectures) + int(subjectObject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10
        total = str(int(m1) + int(m2) + float(att)) + "/" + str(int(m1t) + int(m2t) + 10)

        finalDict = {'id': id, 'name': name, 'enrollment': enrollment, 'm1': m1, 'm1t': m1t, 'm2': m2, 'm2t': m2t, 'subjectid': subjectid, 'att': att, 'total': total}
        finalList.append(finalDict)
    
    return render(request, 'Marks/CWTake.html', {'StudentList': finalList, 'total': len(finalList), 'Subject': subjectObject})


@permission_required('Resources.marks_rights')
def swTake(request):
    
    subjectObject = Subject.objects.get(id = request.GET.get('subject', 0))
    semester = Semester.objects.get(id = subjectObject.Semester_id.id)

    finalList = []
    theory = 0
    lab = 0

    id = 0
    name = ""
    enrollment = ""
    v1 = 0
    v1t = DEFAULT_Viva1Total
    v2 = 0
    v2t = DEFAULT_Viva2Total
    q1 = 0
    q1t = DEFAULT_Quiz1Total
    q2 = 0
    q2t = DEFAULT_Quiz2Total
    subjectid = subjectObject.id


    for student in Student.objects.filter(Semester_id = semester):

        id = student.id
        name = student.First + " " + student.Last
        enrollment = student.Enrollment

        if Marks.objects.filter(Student_id = student, Subject_id = subjectObject).count() > 0:
            v1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva1
            v1t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva1Total
            v2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva2
            v2t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva2Total
            q1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz1
            q1t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz1Total
            q2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz2
            q2t = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz2Total
        else:
            v1 = 0
            v1t = DEFAULT_Viva1Total
            v2 = 0
            v2t = DEFAULT_Viva2Total
            q1 = 0
            q1t = DEFAULT_Quiz1Total
            q2 = 0
            q2t = DEFAULT_Quiz2Total

        theory = 0
        lab = 0
        
        for i in Attendence.objects.filter(Student_id = student, Subject_id = subjectObject):
            if i.Theory_Lectures == True:
                theory = theory + 1
            if i.Lab_Lectures == True:
                lab = lab + 1

        att = round((((theory + lab) / (int(subjectObject.Theory_Lectures) + int(subjectObject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10
        total = str(int(v1) + int(v2) + int(q1) + int(q2) + float(att)) + "/" + str(int(v1t) + int(v2t) + int(q1t) + int(q2t) + 10)

        finalDict = {'id': id, 'name': name, 'enrollment': enrollment, 'v1': v1, 'v2': v2, 'q1': q1, 'q2': q2, 'v1t': v1t, 'v2t': v2t, 'q1t': q1t, 'q2t': q2t, 'subjectid': subjectid, 'att': att, 'total': total}
        finalList.append(finalDict)
    
    return render(request, 'Marks/SWTake.html', {'StudentList': finalList, 'total': len(finalList), 'Subject': subjectObject})


@permission_required('Resources.marks_rights')
def cwTakeUpdate(request):
    
    if request.method == 'POST':

        body = QueryDict(request.body)
        studentID = body.get('studentID')
        subjectID = body.get('subjectID')
        mid1 = body.get('mid1')
        mid2 = body.get('mid2')

        studentInstance = Student.objects.get(id = studentID)
        subjectInstance = Subject.objects.get(id = subjectID)

        if Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).count() > 0:
            m = Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).first()
            m.MidTerm1 = mid1
            m.MidTerm2 = mid2
            m.save()
        else:
            Marks(Student_id = studentInstance, Subject_id = subjectInstance, MidTerm1 = mid1, MidTerm2 = mid2, Viva1 = 0, Viva2 = 0, Quiz1 = 0, Quiz2 = 0).save()

        data = {'Success': ''}
        return JsonResponse(data)

    data = {'Error': ''}
    return JsonResponse(data)


@permission_required('Resources.marks_rights')
def swTakeUpdate(request):
    
    if request.method == 'POST':

        body = QueryDict(request.body)
        studentID = body.get('studentID')
        subjectID = body.get('subjectID')
        viva1 = body.get('viva1')
        viva2 = body.get('viva2')
        quiz1 = body.get('quiz1')
        quiz2 = body.get('quiz2')

        studentInstance = Student.objects.get(id = studentID)
        subjectInstance = Subject.objects.get(id = subjectID)

        if Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).count() > 0:
            m = Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).first()
            m.Viva1 = viva1
            m.Viva2 = viva2
            m.Quiz1 = quiz1
            m.Quiz2 = quiz2
            m.save()
        else:
            Marks(Student_id = studentInstance, Subject_id = subjectInstance, MidTerm1 = 0, MidTerm2 = 0, Viva1 = viva1, Viva2 = viva2, Quiz1 = quiz1, Quiz2 = quiz2).save()

        data = {'Success': ''}
        return JsonResponse(data)

    data = {'Error': ''}
    return JsonResponse(data)


@login_required
def cwViewStudent(request):

    subjectInstance = Subject.objects.get(id = request.GET.get('subject', 0))
    studentInstance = Student.objects.get(Email = request.user.email)

    theory = 0
    lab = 0

    id = 0
    name = ""
    enrollment = ""
    m1 = 0
    m1t = DEFAULT_MidTerm1Total
    m2 = 0
    m2t = DEFAULT_MidTerm2Total
    subjectid = subjectInstance.id

    id = studentInstance.id
    name = studentInstance.First + " " + studentInstance.Last
    enrollment = studentInstance.Enrollment

    if Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).count() > 0:
        m1 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).MidTerm1
        m1t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).MidTerm1Total
        m2 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).MidTerm2
        m2t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).MidTerm2Total


    for i in Attendence.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance):
        if i.Theory_Lectures == True:
            theory = theory + 1
        if i.Lab_Lectures == True:
            lab = lab + 1

    att = round((((theory + lab) / (int(subjectInstance.Theory_Lectures) + int(subjectInstance.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10
    total = str(int(m1) + int(m2) + float(att)) + "/" + str(int(m1t) + int(m2t) + 10)

    finalDict = {'id': id, 'name': name, 'enrollment': enrollment, 'm1': m1, 'm1t': m1t, 'm2': m2, 'm2t': m2t, 'subjectid': subjectid, 'att': att, 'total': total}
    
    return render(request, 'Marks/CWViewStudent.html', {'MarksDetails': finalDict})


@login_required
def swViewStudent(request):

    subjectInstance = Subject.objects.get(id = request.GET.get('subject', 0))
    studentInstance = Student.objects.get(Email = request.user.email)

    theory = 0
    lab = 0

    id = 0
    name = ""
    enrollment = ""
    v1 = 0
    v1t = DEFAULT_Viva1Total
    v2 = 0
    v2t = DEFAULT_Viva2Total
    q1 = 0
    q1t = DEFAULT_Quiz1Total
    q2 = 0
    q2t = DEFAULT_Quiz2Total
    subjectid = subjectInstance.id

    id = studentInstance.id
    name = studentInstance.First + " " + studentInstance.Last
    enrollment = studentInstance.Enrollment

    if Marks.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance).count() > 0:
        v1 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Viva1
        v1t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Viva1Total
        v2 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Viva2
        v2t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Viva2Total
        q1 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Quiz1
        q1t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Quiz1Total
        q2 = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Quiz2
        q2t = Marks.objects.get(Student_id = studentInstance, Subject_id = subjectInstance).Quiz2Total


    for i in Attendence.objects.filter(Student_id = studentInstance, Subject_id = subjectInstance):
        if i.Theory_Lectures == True:
            theory = theory + 1
        if i.Lab_Lectures == True:
            lab = lab + 1

    att = round((((theory + lab) / (int(subjectInstance.Theory_Lectures) + int(subjectInstance.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10
    total = str(int(v1) + int(v2) + int(q1) + int(q2) + float(att)) + "/" + str(int(v1t) + int(v2t) + int(q1t) + int(q2t) + 10)

    finalDict = {'id': id, 'name': name, 'enrollment': enrollment, 'v1': v1, 'v2': v2, 'q1': q1, 'q2': q2, 'v1t': v1t, 'v2t': v2t, 'q1t': q1t, 'q2t': q2t, 'subjectid': subjectid, 'att': att, 'total': total}
    
    return render(request, 'Marks/SWViewStudent.html', {'MarksDetails': finalDict})


@permission_required('Resources.marks_view_rights')
def viewMarks(request):
    
    semesterInstance = Semester.objects.get(id = request.POST.get('semester4', 0))

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

        for subject in subjectInstance:

            theory = 0
            lab = 0

            for i in Attendence.objects.filter(Student_id = student, Subject_id = subject):
                if i.Theory_Lectures == True:
                    theory = theory + 1
                if i.Lab_Lectures == True:
                    lab = lab + 1

            att = round((((theory + lab) / (int(subject.Theory_Lectures) + int(subject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10

            cwDefaultTotal = (int(DEFAULT_MidTerm1Total) + int(DEFAULT_MidTerm2Total) + 10)
            swDefaultTotal = (int(DEFAULT_Viva1Total) + int(DEFAULT_Viva2Total) + int(DEFAULT_Quiz1Total) + int(DEFAULT_Quiz2Total) + 10)

            m = Marks.objects.filter(Student_id = student, Subject_id = subject)

            if m.count() > 0:
                m1 = m.first().MidTerm1
                m2 = m.first().MidTerm2
                v1 = m.first().Viva1
                v2 = m.first().Viva2
                q1 = m.first().Quiz1
                q2 = m.first().Quiz2

                cwTotal = (int(m1) + int(m2) + int(att))
                swTotal = (int(v1) + int(v2) + int(q1) + int(q2) + int(att))

                marksList.append({'Name': str(student.First) + " " + str(student.Last), 'Enrollment': student.Enrollment, 'Mid1': m.first().MidTerm1, 'MidTerm1Total': m.first().MidTerm1Total, 'MidTerm2': m.first().MidTerm2, 'MidTerm2Total': m.first().MidTerm2Total, 'Viva1': m.first().Viva1, 'Viva1Total': m.first().Viva1Total, 'Viva2': m.first().Viva2, 'Viva2Total': m.first().Viva2Total, 'Quiz1': m.first().Quiz1, 'Quiz1Total': m.first().Quiz1Total, 'Quiz2': m.first().Quiz2, 'Quiz2Total': m.first().Quiz2Total, 'Attendance': att, 'CWTotal': cwTotal, 'CWDefaultTotal': cwDefaultTotal, 'SWTotal': swTotal, 'SWDefaultTotal': swDefaultTotal})
            else:
                marksList.append({'Name': str(student.First) + " " + str(student.Last), 'Enrollment': student.Enrollment, 'Mid1': 0, 'MidTerm1Total': DEFAULT_MidTerm1Total, 'MidTerm2': 0, 'MidTerm2Total': DEFAULT_MidTerm2Total, 'Viva1': 0, 'Viva1Total': DEFAULT_Viva1Total, 'Viva2': 0, 'Viva2Total': DEFAULT_Viva2Total, 'Quiz1': 0, 'Quiz1Total': DEFAULT_Quiz1Total, 'Quiz2': 0, 'Quiz2Total': DEFAULT_Quiz2Total, 'Attendance': att, 'CWTotal': 0, 'CWDefaultTotal': cwDefaultTotal, 'SWTotal': 0, 'SWDefaultTotal': swDefaultTotal}) # 0 Marks

        studentMarksList.append(marksList)
        
    return render(request, 'Marks/ViewMarks.html', {'StudentMarksList': studentMarksList, 'SubjectList': subjectList, 'CourseName': courseName, 'SemesterName': semesterInstance.Name})


@permission_required('Resources.marks_view_rights')
def viewMarksExport(request):

    semesterInstance = Semester.objects.get(id = request.POST.get('semester5', 0))

    studentListInstance = Student.objects.filter(Semester_id = semesterInstance)

    subjectInstance = Subject.objects.filter(Semester_id = semesterInstance)

    branchInstance = Branch.objects.get(id = semesterInstance.Branch_id.id)

    courseName = Course.objects.get(id = branchInstance.Course_id.id).Name

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + courseName + '_' + semesterInstance.Name + '_Semester_Marks_List' + '.csv"'

    writer = csv.writer(response)
    
    headerList = ['S.No.', 'Name', 'Enrollment']
    marksTypeHeader = [' ', ' ', ' ']
    workTypeHeader = [' ', ' ', ' ']

    subjectList = []


    for subject in subjectInstance:
        subjectList.append({'Name': subject.Name})
        headerList.append(subject.Name)
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        headerList.append(" ")
        workTypeHeader.append("Classwork Marks")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        workTypeHeader.append("Sessional Work Marks")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        workTypeHeader.append(" ")
        marksTypeHeader.append('Mid Term 1 (' + str(DEFAULT_MidTerm1Total) + ' Marks)')
        marksTypeHeader.append('Mid Term 2 (' + str(DEFAULT_MidTerm2Total) + ' Marks)')
        marksTypeHeader.append('Attendance (10 Marks)')
        marksTypeHeader.append('Total')
        marksTypeHeader.append('Viva 1 (' + str(DEFAULT_Viva1Total) + ' Marks)')
        marksTypeHeader.append('Viva 2 (' + str(DEFAULT_Viva2Total) + ' Marks)')
        marksTypeHeader.append('Quiz 1 (' + str(DEFAULT_Quiz1Total) + ' Marks)')
        marksTypeHeader.append('Quiz 2 (' + str(DEFAULT_Quiz2Total) + ' Marks)')
        marksTypeHeader.append('Attendance (10 Marks)')
        marksTypeHeader.append('Total')

    writer.writerow(headerList)
    writer.writerow(workTypeHeader)
    writer.writerow(marksTypeHeader)

    counter = 0

    for student in studentListInstance:

        counter = counter + 1

        row = []
        row.append(str(counter))
        row.append(str(student.First) + " " + str(student.Last))
        row.append(student.Enrollment)

        for subject in subjectInstance:

            theory = 0
            lab = 0

            for i in Attendence.objects.filter(Student_id = student, Subject_id = subject):
                if i.Theory_Lectures == True:
                    theory = theory + 1
                if i.Lab_Lectures == True:
                    lab = lab + 1

            att = round((((theory + lab) / (int(subject.Theory_Lectures) + int(subject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10

            cwDefaultTotal = (int(DEFAULT_MidTerm1Total) + int(DEFAULT_MidTerm2Total) + 10)
            swDefaultTotal = (int(DEFAULT_Viva1Total) + int(DEFAULT_Viva2Total) + int(DEFAULT_Quiz1Total) + int(DEFAULT_Quiz2Total) + 10)

            m = Marks.objects.filter(Student_id = student, Subject_id = subject)

            if m.count() > 0:
                m1 = m.first().MidTerm1
                m2 = m.first().MidTerm2
                v1 = m.first().Viva1
                v2 = m.first().Viva2
                q1 = m.first().Quiz1
                q2 = m.first().Quiz2

                cwTotal = (int(m1) + int(m2) + int(att))
                swTotal = (int(v1) + int(v2) + int(q1) + int(q2) + int(att))

                row.append(str(m.first().MidTerm1))
                row.append(str(m.first().MidTerm2))
                row.append(str(att))
                row.append(str(cwTotal) + "\\" + str(cwDefaultTotal))
                row.append(str(m.first().Viva1))
                row.append(str(m.first().Viva2))
                row.append(str(m.first().Quiz1))
                row.append(str(m.first().Quiz2))
                row.append(str(att))
                row.append(str(swTotal) + "\\" + str(swDefaultTotal))
            else:
                row.append(str("0"))
                row.append(str("0"))
                row.append(str(att))
                row.append("0" + "\\" + str(cwDefaultTotal))
                row.append("0")
                row.append("0")
                row.append("0")
                row.append("0")
                row.append(str(att))
                row.append("0" + "\\" + str(swDefaultTotal))

        writer.writerow(row)

    return response

@permission_required('Resources.marks_rights')
def chartView(request):

    subjectObject = Subject.objects.get(id = request.GET.get('subject', 0))
    semester = Semester.objects.get(id = subjectObject.Semester_id.id)
   
    theory = 0
    lab = 0

    m1 = 0
    m2 = 0

    ac1 = 0
    ac2 = 0
    ac3 = 0
    ac4 = 0
    ac5 = 0
    ac6 = 0
    ac7 = 0
    ac8 = 0
    ac9 = 0
    ac10 = 0

    bc1 = 0
    bc2 = 0
    bc3 = 0
    bc4 = 0
    bc5 = 0
    bc6 = 0
    bc7 = 0
    bc8 = 0
    bc9 = 0
    bc10 = 0


    for student in Student.objects.filter(Semester_id = semester):

        if Marks.objects.filter(Student_id = student, Subject_id = subjectObject).count() > 0:
            m1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm1
            m2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).MidTerm2
        else:
            m1 = 0
            m2 = 0

        theory = 0
        lab = 0

        for i in Attendence.objects.filter(Student_id = student, Subject_id = subjectObject):
            if i.Theory_Lectures == True:
                theory = theory + 1
            if i.Lab_Lectures == True:
                lab = lab + 1

        att = round((((theory + lab) / (int(subjectObject.Theory_Lectures) + int(subjectObject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10

        actotal = int(int(m1) + int(m2) + float(att))

        bctotal = 0


        if int(m1) >  int(m2):
            bctotal = int(int(m1) + int(m1) + float(att))
        else:
            bctotal = int(int(m2) + int(m2) + float(att))
        

        if actotal >= 28 and actotal <= 30:
            ac10 = ac10 + 1
        elif actotal >= 25 and actotal <= 27:
            ac9 = ac9 + 1
        elif actotal >= 22 and actotal <= 24:
            ac8 = ac8 + 1
        elif actotal >= 19 and actotal <= 21:
            ac7 = ac7 + 1
        elif actotal >= 16 and actotal <= 18:
            ac6 = ac6 + 1
        elif actotal >= 13 and actotal <= 15:
            ac5 = ac5 + 1
        elif actotal >= 10 and actotal <= 12:
            ac4 = ac4 + 1
        elif actotal >= 7 and actotal <= 9:
            ac3 = ac3 + 1
        elif actotal >= 4 and actotal <= 6:
            ac2 = ac2 + 1
        elif actotal >= 1 and actotal <= 3:
            ac1 = ac1 + 1

        if bctotal >= 28 and bctotal <= 30:
            bc10 = bc10 + 1
        elif bctotal >= 25 and bctotal <= 27:
            bc9 = bc9 + 1
        elif bctotal >= 22 and bctotal <= 24:
            bc8 = bc8 + 1
        elif bctotal >= 19 and bctotal <= 21:
            bc7 = bc7 + 1
        elif bctotal >= 16 and bctotal <= 18:
            bc6 = bc6 + 1
        elif bctotal >= 13 and bctotal <= 15:
            bc5 = bc5 + 1
        elif bctotal >= 10 and bctotal <= 12:
            bc4 = bc4 + 1
        elif bctotal >= 7 and bctotal <= 9:
            bc3 = bc3 + 1
        elif bctotal >= 4 and bctotal <= 6:
            bc2 = bc2 + 1
        elif bctotal >= 1 and bctotal <= 3:
            bc1 = bc1 + 1

    av = str(ac1) + ', ' + str(ac2) + ', ' + str(ac3) + ', ' + str(ac4) + ', ' + str(ac5) + ', ' + str(ac6) + ', ' + str(ac7) + ', ' + str(ac8) + ', ' + str(ac9) + ', ' + str(ac10)
    bo = str(bc1) + ', ' + str(bc2) + ', ' + str(bc3) + ', ' + str(bc4) + ', ' + str(bc5) + ', ' + str(bc6) + ', ' + str(bc7) + ', ' + str(bc8) + ', ' + str(bc9) + ', ' + str(bc10)

    return render(request, 'Marks/Chart.html', {'ClassworkAverage': av, 'ClassworkBest': bo})


@permission_required('Resources.marks_rights')
def swChartView(request):

    subjectObject = Subject.objects.get(id = request.GET.get('subject', 0))
    semester = Semester.objects.get(id = subjectObject.Semester_id.id)
   
    theory = 0
    lab = 0

    v1 = 0
    v2 = 0
    q1 = 0
    q2 = 0

    ac1 = 0
    ac2 = 0
    ac3 = 0
    ac4 = 0
    ac5 = 0
    ac6 = 0
    ac7 = 0
    ac8 = 0
    ac9 = 0
    ac10 = 0

    bc1 = 0
    bc2 = 0
    bc3 = 0
    bc4 = 0
    bc5 = 0
    bc6 = 0
    bc7 = 0
    bc8 = 0
    bc9 = 0
    bc10 = 0

    for student in Student.objects.filter(Semester_id = semester):

        if Marks.objects.filter(Student_id = student, Subject_id = subjectObject).count() > 0:
            v1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva1
            v2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Viva2
            q1 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz1
            q2 = Marks.objects.get(Student_id = student, Subject_id = subjectObject).Quiz2
        else:
            v1 = 0
            v2 = 0
            q1 = 0
            q2 = 0

        theory = 0
        lab = 0
        
        for i in Attendence.objects.filter(Student_id = student, Subject_id = subjectObject):
            if i.Theory_Lectures == True:
                theory = theory + 1
            if i.Lab_Lectures == True:
                lab = lab + 1

        att = round((((theory + lab) / (int(subjectObject.Theory_Lectures) + int(subjectObject.Lab_Lectures))) * 10), 2) # Divide by 10 to get point in range of 1 to 10

        actotal = int(int(int(v1) + int(v2) + int(q1) + int(q2) + float(att)) - 10)

        if actotal <= 0:
            actotal = 0

        bctotal = 0
        viva = 0
        quiz = 0

        if int(v1) > int(v2):
            viva = int(int(v1) + int(v1))
        else:
            viva = int(int(v2) + int(v2))

        if int(q1) > int(q2):
            quiz = int(int(q1) + int(q1))
        else:
            quiz = int(int(q2) + int(q2))

        
        bctotal = int((viva + quiz + float(att)) - 10)

        if bctotal <= 0:
            bctotal = 0


        if actotal >= 37 and actotal <= 40:
            ac10 = ac10 + 1
        elif actotal >= 33 and actotal <= 36:
            ac9 = ac9 + 1
        elif actotal >= 29 and actotal <= 32:
            ac8 = ac8 + 1
        elif actotal >= 25 and actotal <= 28:
            ac7 = ac7 + 1
        elif actotal >= 21 and actotal <= 24:
            ac6 = ac6 + 1
        elif actotal >= 17 and actotal <= 20:
            ac5 = ac5 + 1
        elif actotal >= 13 and actotal <= 16:
            ac4 = ac4 + 1
        elif actotal >= 9 and actotal <= 12:
            ac3 = ac3 + 1
        elif actotal >= 5 and actotal <= 8:
            ac2 = ac2 + 1
        elif actotal >= 1 and actotal <= 4:
            ac1 = ac1 + 1


        if bctotal >= 37 and bctotal <= 40:
            bc10 = bc10 + 1
        elif bctotal >= 33 and bctotal <= 36:
            bc9 = bc9 + 1
        elif bctotal >= 29 and bctotal <= 32:
            bc8 = bc8 + 1
        elif bctotal >= 25 and bctotal <= 28:
            bc7 = bc7 + 1
        elif bctotal >= 21 and bctotal <= 24:
            bc6 = bc6 + 1
        elif bctotal >= 17 and bctotal <= 20:
            bc5 = bc5 + 1
        elif bctotal >= 13 and bctotal <= 16:
            bc4 = bc4 + 1
        elif bctotal >= 9 and bctotal <= 12:
            bc3 = bc3 + 1
        elif bctotal >= 5 and bctotal <= 8:
            bc2 = bc2 + 1
        elif bctotal >= 1 and bctotal <= 4:
            bc1 = bc1 + 1

    av = str(ac1) + ', ' + str(ac2) + ', ' + str(ac3) + ', ' + str(ac4) + ', ' + str(ac5) + ', ' + str(ac6) + ', ' + str(ac7) + ', ' + str(ac8) + ', ' + str(ac9) + ', ' + str(ac10)
    bo = str(bc1) + ', ' + str(bc2) + ', ' + str(bc3) + ', ' + str(bc4) + ', ' + str(bc5) + ', ' + str(bc6) + ', ' + str(bc7) + ', ' + str(bc8) + ', ' + str(bc9) + ', ' + str(bc10)
    
    return render(request, 'Marks/SWChart.html', {'SessionalAverage': av, 'SessionalBest': bo})