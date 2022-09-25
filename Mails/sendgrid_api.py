

import sendgrid
import os
import base64
from sendgrid.helpers.mail import *
from Resources.models import SendGridAPIKey
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileType, FileName, Disposition)
from django.conf import settings


def SendMail(to, subjectLine, file, body):

    tolist = []

    for e in str(to).split(","):
        tolist.append(e.strip())

    message = Mail(from_email=settings.DEFAULT_FROM_EMAIL, to_emails=tolist, subject=subjectLine, html_content=body)

    if file != None:
        data = file.read()
        encoded_file = base64.b64encode(data).decode()
        attachedFile = Attachment(FileContent(encoded_file), FileName(file.name), FileType(file.content_type), Disposition('attachment'))
        message.attachment = attachedFile

    sg = sendgrid.SendGridAPIClient(api_key=SendGridAPIKey.objects.all()[0].Key)
    response = sg.send(message)
    return response
