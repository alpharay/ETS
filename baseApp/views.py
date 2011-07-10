# Create your views here.
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from models import Consumer, EventOrganizer,EventCategory,Event,Ticket,Cart,Payment,Suggestion,OutgoingSMS,IncomingSMS,Order
from django.views.decorators.csrf import csrf_exempt

def home(request):
    t = loader.get_template('baseApp/index.html')
    c = Context(dict())
    return HttpResponse(t.render(c))