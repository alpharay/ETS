from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from baseApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.contrib.auth.models import User
import time
import re
# Create your views here.

def processIncomingSMS(request):    # processes all sms received from mobile money providers
    time.sleep(10)
    smsleft = IncomingSMS.objects.filter(read = False)
    for sms in smsleft:
        result = re.search(r'(.*)transactionid:(.*)(\d+)\namount:(.*)(\d+)', sms.message)
        sms.transactionID = result.group(2)
        sms.amount = result.group(4)


class OutgoingSMSForm(ModelForm):
    class Meta:
        model = OutgoingSMS
        exclude = ['receiver','message','sent','created']
        
def redeemCart(request, phoneNumber, transID='blank'): # Get cart thats unpaid for
    cartRecords = Cart.objects.filter(consumerPhone = phoneNumber)
    cart2redeem = cartRecords.objects.get(paid = False)
    if transID != 'blank' and IncomingSMS.objects.get(transactionID = transID):
        cart2redeem.paid = True
        ticketsBought=Ticket.objects.filter(cart__id = cart2redeem)
        phoneNumStr= 'These tickets have been sent to: '+str(phoneNumber)+'\n'
        ticketStr=''
        for ticket in ticketsBought:
            ticketStr = str(ticket.event)+str(ticket.pin)+str(ticket.ticketType)+'\n'
        smsBody = phoneNumStr+ticketStr
        content = OutgoingSMS(receiver=phoneNumber,message=smsBody,sent=False)
        form = OutgoingSMSForm(request.POST, instance = content)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = OutgoingSMSForm(instance = content)