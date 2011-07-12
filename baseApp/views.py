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
    
    if request.method == 'POST':
        pass
        #create cart and add ticket information
        #
    else:
        
        form = AddButton()
        event = Event.objects.get(id=id)
        tickets = Ticket.objects.filter(event__id=id)
        type=TicketType.objects.filter(event__id=id)
        #ticket types and thier count
        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'tickets':tickets,'ticket_types':type})