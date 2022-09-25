

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .forms import SendForm, SMSForm
from .sendgrid_api import SendMail
from .twilio_api import SendSMS
from django.http import HttpResponse
from Resources.models import Student

# Create your views here.


@permission_required('Resources.email_rights')
def compose(request):

    smsForm = SMSForm()

    if request.method == 'POST':

        Form = SendForm(request.POST, request.FILES)

        if Form.is_valid():

            response = SendMail(Form.cleaned_data['To'], Form.cleaned_data['Subject'], request.FILES.get('Attachment', None), Form.cleaned_data['Body'])

            if response.status_code == 202:
                return render(request, 'Mails/Email.html', {'Form': Form, 'Message': 'Message Sent!', 'Visiblity': 'visible', 'color': 'success', 'SMSForm': smsForm})
            else:
                return render(request, 'Mails/Email.html', {'Form': Form, 'Message': 'Error Occurred!, Status Code: ' + str(response.status_code), 'Visiblity': 'visible', 'color': 'danger', 'SMSForm': smsForm})

    Form = SendForm()
    
    return render(request, 'Mails/Email.html', {'Form': Form, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'SMSForm': smsForm})

@permission_required('Resources.email_rights')
def bulk(request):
    
    Form = SendForm()
    smsForm = SMSForm()

    if request.method == 'POST':

        emailString = ''
        smsString = ''

        for emailaddress in request.POST.getlist('emailchecks[]'):
            emailString = emailString + str(emailaddress) + ', '
            smsString = smsString + str(Student.objects.filter(Email=emailaddress).first().Contact) + ', '

        emailString = emailString[:-2]
        smsString = smsString[:-2]

        Form = SendForm(initial={'To': emailString})
        smsForm = SMSForm(initial={'Contact': smsString})

    return render(request, 'Mails/Email.html', {'Form': Form, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'SMSForm': smsForm})
    

@permission_required('Resources.sms_rights')
def smsSend(request):
    
    smsForm = SMSForm()
    Form = SendForm()

    if request.method == 'POST':

        smsForm = SMSForm(request.POST)

        if smsForm.is_valid():

            SendSMS(smsForm.cleaned_data['Contact'], smsForm.cleaned_data['Message'])

            return render(request, 'Mails/Email.html', {'Form': Form, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'SMSForm': smsForm, 'Message2': 'SMS Sent!', 'Visiblity2': 'visible', 'color2': 'success'})

    return render(request, 'Mails/Email.html', {'Form': Form, 'Message': '', 'Visiblity': 'invisible', 'color': 'danger', 'SMSForm': smsForm})