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
import time
import datetime
import re
    
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

class CartForm(ModelForm):
    class Meta:
        model =Cart
        #exclude=['author','post']     
        
class TicketForm(ModelForm):
    class Meta:
        model =Ticket

def cart_list(request,id):
    if id:        
        cart = Ticket.objects.filter(Cart__id=id)
        return render_to_response('baseApp/cart.html', {'cart':cart})
    else:
        return HttpResponse('<div align="center"><h5>Cart is empty</h5></div>')

	
def events_list(request,id):
    event_list = Event.objects.filter(category__id=id)
    return render_to_response('baseApp/eventList.html', {'events':event_list})

def isPhone(inp):
     result = re.search(r'^0[1-9]{9}', inp,re.L)
    # print result.groups() 
     if result:
         return True
     else:
         return False

@csrf_exempt
def event_detail(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    tstr={}
    sum=0
    if request.method == 'POST':
        i=0
        if isPhone(request.POST['phone']):
            for i in range(len(ticketsType)):
                if request.POST.get(ticketsType[i].name, None):             
                    tstr[request.POST[ticketsType[i].name]]=ticketsType[i].price
                    sum+=float(ticketsType[i].price)
            
            tdate=str(datetime.datetime.today())
            tForm=TicketForm()    
            cForm=CartForm(request.POST,initial={'consumerPhone':request.POST['phone'],'value':sum,'created': tdate})
            
#            if cForm.is_valid():
#                    cForm.save()
#            else:
#                return HttpResponse('Cart failed go back and try again')
#            
#            cart = Cart.objects.get(consumerPhone=request.POST['phone'],created=tdate) 
            
            tickets = Ticket.objects.filter(event__id=id)
            return HttpResponse(tickets)
            
            return HttpResponse(str)
        else:
            return HttpResponse('Enter a valid phnoe number and try again')
                
    else:
        form = AddButton()
        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType})
        
        
class SuggestionForm(ModelForm):
	class Meta:
		model=Suggestion
		exclude = ['consumer','created']

@csrf_exempt
def addSuggestion(request):
	suggestions = Suggestion.objects.all()
	msg=''
	#Start of form code
	comment = Suggestion()
	if request.method == 'POST':
		if request.user.is_authenticated():
			comment = Suggestion(consumer=request.user)
		else:
			comment = Suggestion()
		
		form = SuggestionForm(request.POST, instance = comment)
		if form.is_valid():
			form.save()
			msg = 'Your suggestion has been saved'
			return render_to_response('baseApp/suggestions.html', {'suggestions':suggestions,'msg':msg,'form':form.as_p() })
	else:
		form = SuggestionForm()
		#end of form code
		return render_to_response('baseApp/suggestions.html', {'suggestions':suggestions,'msg':msg,'form':form.as_p() })

#@csrf_exempt
#def editSuggestion(request, id):
#	msg=''
#	comment = Suggestion.objects.get(id=id)
#	#Start of form code
#	if request.user == suggestion.consumer:
#		if request.method == 'POST':
#			form = SuggestionForm(request.POST, instance = comment)
#			if form.is_valid():
#				form.save()
#				msg = 'Your suggestion has been saved'
#				return render_to_response('baseApp/editsuggestion.html', {'msg':msg,'form':form.as_p() })	
#		else:
#			form = SuggestionForm(instance = comment)
#			#end of form code
#			return render_to_response('baseApp/editsuggestion.html', {'msg':msg,'form':form.as_p() })
#	else:
#		msg = 'You do not have permission to edit this comment'
#		return render_to_response('baseApp/editsuggestion.html', {'msg':msg,'form':form.as_p() })