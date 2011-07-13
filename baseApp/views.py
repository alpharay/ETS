# Create your views here.
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django import forms

class CartForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class AddButton(forms.Form):
    pass
    

def home(request):
    t = loader.get_template('baseApp/welcome.html')
    c = Context(dict())
    return HttpResponse(t.render(c))
    
def categories_list(request):
#    return HttpResponse('am here')
    category_list = EventCategory.objects.all()
    return render_to_response('baseApp/categoryView.html', {'category_list':category_list})

#def names_list(request):
#    name_list = Event.objects.all()
#    return render_to_response('baseApp/nameView.html', {'name_list':name_list})

#def venues_list(request):
#    venue_list = Event.objects.filter()
#    return render_to_response('baseApp/venueView.html', {'venue_list':venue_list})

#class EventForm(ModelForm):
#	class Meta:
#		model=Event
#		exclude=['post','author']
def view_map(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    return render_to_response('baseApp/map.html', {'event_details':event})
       

def cart_list(request,id):
    if id:        
        cart = Ticket.objects.filter(Cart__id=id)
        return render_to_response('baseApp/cart.html', {'cart':cart})
    else:
        return HttpResponse('<div align="center"><h5>Cart is empty</h5></div>')

	
def events_list(request,id):
    event_list = Event.objects.filter(category__id=id)
    return render_to_response('baseApp/eventList.html', {'events':event_list})

@csrf_exempt
def event_detail(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    
    if request.method == 'POST':
        for type in ticketsType:
            if request.POST.get(type.name, False):
                return HttpResponse(request.POST['qty'+type.name])
    else:
        form = AddButton()
        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType})