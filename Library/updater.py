from datetime import datetime,date
from apscheduler.schedulers.background import BackgroundScheduler
from Library import models  
from Resources import models as ResourcesModels
from django.core.mail import send_mail


def jobb():
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    print(issuedbooks)
    for ib in issuedbooks:
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0

        if d>15:
            students= ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment)
            send_mail(
                'Return Issused Book Before The Due Date',
                'You are requested to return issused book before the due date',
                'satyamraghuwanshi07@gmail.com',
                [students[0].Email]
            )
            print('sent.....')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobb, 'interval', seconds=30)
    scheduler.start()