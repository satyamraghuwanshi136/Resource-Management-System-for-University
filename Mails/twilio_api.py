
import os
from twilio.rest import Client
from Resources.models import TwilioAPIKey
import json


def SendSMS(numbers, body):

    numberlist = []

    for e in str(numbers).split(","):
        numberlist.append("+91" + str(e.strip()))

    account_sid = str(TwilioAPIKey.objects.all()[0].SID)
    auth_token = str(TwilioAPIKey.objects.all()[0].Token)
    notify_service_sid = str(TwilioAPIKey.objects.all()[0].Notify)

    client = Client(account_sid, auth_token)

    bindings = list(map(lambda number: json.dumps({'binding_type': 'sms', 'address': number}), numberlist))
    print("=====> To Bindings :>", bindings, "<: =====")
    notification = client.notify.services(notify_service_sid).notifications.create(
        to_binding=bindings,
        body=body
    )
    print(notification.body)