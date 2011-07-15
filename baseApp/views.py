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
import random
import datetime
import re
from django.forms.widgets import *
from django.forms.extras.widgets import *
    
class AddForm(forms.Form):
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
#    class Meta:
#        model=Event
#        exclude=['post','author']
def view_map(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    return render_to_response('baseApp/map.html', {'event_details':event})

class TicketForm(ModelForm):
    class Meta:
        model =Ticket
        #exclude=['author','post']  

class CartForm(ModelForm):
    class Meta:
        model =Cart
           
class AddEventForm(forms.Form):
    pass
    
class CartForm(forms.Form):
    pass

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
     result = re.search(r'^[0][2|3|5][4|3|6|7|8]([1-9]){7}$', inp,re.L)
    # print result.groups() 
     if result:
         return True
     else:
         return False
     

@csrf_exempt
def event_detail(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    allTickets = Ticket.objects.filter(event__id=id)
    tdate=str(datetime.datetime.today())
    tstr={}
    sum=0
    msg=''
    
    if request.method == 'POST':  
        form = AddForm()
        i=0
        if isPhone(request.POST['phone']):
             
            for i in range(len(ticketsType)):
                if request.POST.get(ticketsType[i].name, None):             
                    tstr[i]=ticketsType[i].name
                    
                    sum+=float(ticketsType[i].price)
                else:
                    pass
              
            #check if a ticket has been selected    
            if len(tstr)<1:
                 msg="Please select a ticket"
                 return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                   
            try:#Check the for the availability of tickets
                
                for j in range(len(tstr)):
                    tyt=TicketType.objects.get(name=tstr[j])
                    tickets = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)
                    if len(tickets)<1:
                        msg="sorry we have run out of "+tstr[j]+" tickets for this event"
                        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                
            except:
                msg="sorry we have run out of tickets for this event"
                return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                
            try:#checks the availability of cart thus if it already exists
                carte=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
                
                 #if a cart is not available for the user(phone number) creates a cart 
                avail=len(carte)
                if avail==0:
                    c=Cart(cPhone=request.POST['phone'],value=str(sum),created=tdate)
                    c.save()
                       
                    try:# add tickets to cart      
                        cart=Cart.objects.get(cPhone=request.POST['phone'],paid=False)
                        for k in range(len(tstr)):  
                            
                            tyt=TicketType.objects.get(name=tstr[k]) 
                                     
                            tick = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)[:1]
                            t = Ticket.objects.get(serialNo=tick[0])
    #                        return HttpResponse(t.paid) 
                            t.paid=True
                            t.cart=cart.cPhone                    
                            t.save()
                            msg='Ticket has been added to cart successfully click on cart to checkoff or add more to cart'  
                            return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
                                
                    except:
                        msg='ticket/s cannot be added, try again'
                        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                    
                    
                if len(carte)>1 or len(carte)<0:
                    msg="a cart exist that you have not paid for"
                    return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
            
             #add tickets to cart if cart already exists     
                try:
                    cart=Cart.objects.get(cPhone=request.POST['phone'],paid=False)
                    for k in range(len(tstr)):  
                        
                        tyt=TicketType.objects.get(name=tstr[k]) 
                                 
                        tick = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)[:1]
                        t = Ticket.objects.get(serialNo=tick[0])
#                        return HttpResponse(t.paid) 
                        t.paid=True
                        t.cart=cart.cPhone                    
                        t.save()
                        msg='Ticket has been added to cart successfully click on cart to checkoff or add more to cart'  
                        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
                                    
                except:
                    msg='failed to add Ticket, try again1'
                    return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
                        
                
            except:
                return HttpResponse('error') 
            
        else:
            msg='Enter a valid phone number'
            return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})        
        
          
    else:
        form = AddForm()
        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets})
    
@csrf_exempt
def addEvent_view(request): 
    categories = EventCategory.objects.all() 
   # return HttpResponse(str(datetime.datetime.today()))     
    if request.method == 'POST':  
        
        if request.POST.get('addevent', None):
            categories = EventCategory.objects.get(name=request.POST['category'])
            #checks if fields are not empty
            if request.POST.get('name', None) or request.POST.get('venue', None) or request.POST.get('date', None):
                form = AddEventForm(request.POST)
                try: 
                    event=Event.objects.get(name=request.POST['name'])
                    categories = EventCategory.objects.all() 
                    form = AddEventForm()
                    msg="an event with this name already exists"
                    return render_to_response('baseApp/addEvent.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'categories':categories,'msg':msg})
    
                except:#creates an event
                    e=Event(name=request.POST['name'],category=categories,venue=request.POST['venue'],
                    locationX=request.POST['gpsx'],locationY=request.POST['gpsy'],
                    event_date=request.POST['date'],event_Rep=request.user,created=str(datetime.datetime.today()))
                    e.save()
                    event=request.POST['name']
                    return render_to_response('baseApp/ticket.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'event':e,'isaddevent':True})
                        
            else:
                categories = EventCategory.objects.all() 
                form = AddEventForm()
                msg="Please fill empty fields to contineu"
                return render_to_response('baseApp/addEvent.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'categories':categories,'msg':msg})

                
        else:#creates an event type        
            event=Event.objects.get(name=str(request.POST['name']))
            tt=TicketType(name=request.POST['ttype'],price=request.POST['price'],event=event)    
            tt.save()
            
             #generate tickets
            for i in range(int(request.POST['qty'])):
                pin=int(random.random()*10000000000000)
                s=int(random.random()*100000000)
                sn="SN"+str(s)
                t=Ticket(event=event,ticketType=tt,pin=pin,serialNo=sn)
                t.save()
                
            msg=str(request.POST['qty'])+' '+str(request.POST['ttype'])+" tickets has been generated for "+str(request.POST['name'])
            form = AddEventForm()
            return render_to_response('baseApp/ticket.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'event':event,'isaddevent':True,'msg':msg})
              
    else:
        form = AddEventForm() 
        return render_to_response('baseApp/addEvent.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'categories':categories})

        
class SuggestionForm(ModelForm):
	class Meta:
		model=Suggestion
		exclude = ['created',]

@csrf_exempt
def addSuggestion(request):
	suggestions = Suggestion.objects.all()
	msg=''
	#Start of form code
	comment = Suggestion()
	if request.method == 'POST':
		if request.user.is_authenticated():
			comment = Suggestion(name=request.user.username)
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
#        form = AddEventForm() 
#        return render_to_response('baseApp/addEvent.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'categories':categories})


@csrf_exempt
def ticket_view(request): 
    return HttpResponse('cut') 

@csrf_exempt
def Cart_view(request): 
    suggestions = Suggestion.objects.all()
    comment = Suggestion()
    if request.method == 'POST':
        if request.POST.get("phone", None): 
            cart=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
            return render_to_response('baseApp/cartlist.html', {'cart':cart })
    else:
        form = CartForm()
        #end of form code
        return render_to_response('baseApp/cart.html', {'form':form.as_p() })


@csrf_exempt
def aboutus(request): 
    return HttpResponse('cut') 


@csrf_exempt
def suggest_view(request): 
    pass 



