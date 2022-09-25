from datetime import datetime,date
from apscheduler.schedulers.background import BackgroundScheduler
from Library import models  
from Resources import models as ResourcesModels
from django.core.mail import send_mail
import os
from twilio.rest import Client

def jobb():
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        bookName = models.Book.objects.filter(isbn=ib.isbn)[0].name
        # print(getattr(ib,'issuedate'))
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-getattr(ib,'issuedate'))
        d=getattr(days,'days')
        fine=0
        if d == 25:
            students= ResourcesModels.Student.objects.filter(Enrollment=ib.enrollment)

            #------- SENDING EMAIL --------#
            send_mail(
                'Return Issused Book Before The Due Date',
                'You are requested to return issused book before the due date',
                'satyamraghuwanshi07@gmail.com',
                [students[0].Email]
            )
            
            print('Sent.....')

            #------- SENDING SMS --------#

            account_sid = 'AC86f9e664457ecbbcf7fcb90edceea353'
            auth_token = '4f73ce2a4253c24762b7ec4f1ef06646'
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body="Dear," + students[0].First + students[0].Last +"Please Return the book \""+ bookName +"\" before " + str(ib.expirydate) + "\n From Library SGSITS,Indore.",
                                from_='+15807224503',
                                to= '+91' + students[0].Contact
                            )
            print('SMS Sent.....')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobb, 'interval', days=1)
    scheduler.start()