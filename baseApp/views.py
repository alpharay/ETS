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

class CartForm(ModelForm):
    class Meta:
        model =Cart
        #exclude=['author','post']     
class AddEventForm(forms.Form):
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
                    tickets = Ticket.objects.filter(event__id=id,ticketType=tstr[j],cart='')
                    if len(tickets)<1:
                        msg="sorry we have run out of "+tstr[j]+" tickets for this event"
                        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                
            except:
                msg="sorry we have run out of tickets for this event"
                return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                
            try:#checks the availability of cart thus if it already exists
                carte=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
                
                if len(carte)>1 or len(carte)<0:
                    msg="a cart exist that you have not paid for"
                    return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
            
             #add tickets to cart if cart already exists     
                try:
                    cart=Cart.objects.get(cPhone=request.POST['phone'],paid=False)
                    for k in range(len(tstr)):                    
                        tickets = Ticket.objects.filter(event__id=id,ticketType=tstr[k],cart='')[:1]
                        t=Ticket(id=tickets.id,cart=cart)
                        t.save()
                        msg='Ticket has been added to cart successfully click on cart to checkoff or add more to cart'  
                        return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
                                    
                except:
                    msg='failed to add Ticket, try again1'
                    return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
                        
                
            except:
                pass  
            
            #if a cart is not available for the user(phone number) creates a cart 
            c=Cart(cPhone=request.POST['phone'],value=str(sum),created=tdate)
            c.save()
               
            try:# add tickets to cart      
                cart = Cart.objects.get(created=tdate,cPhone=request.POST['phone'],paid=False) 
                for j in range(len(tstr)):
                     tickets = Ticket.objects.filter(event__id=id,ticketType=tstr[j])[:1]
                     t=Ticket(id=tickets.id,cart=cart)
                     t.save()
                     msg='Ticket has been added to cart successfully click on cart to checkoff or add more to cart'  
                     return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
            except:
                msg='ticket/s cannot be added, try again'
                return render_to_response('baseApp/eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})
          
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
        categories = EventCategory.objects.get(name=request.POST['category'])
        if request.POST.get('addevent', None):
            form = AddEventForm(request.POST)
            e=Event(name=request.POST['name'],category=categories,venue=request.POST['venue'],
                    locationX=request.POST['gpsx'],locationY=request.POST['gpsy'],
                    event_date=request.POST['date'],created=str(datetime.datetime.today()))
            e.save()
            event=request.POST['name']
            return render_to_response('baseApp/ticket.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'event':e,'isaddevent':True})
        else:
            form = AddEventForm(request.POST)
            event=Event.objects.get(name=request.POST['name'])
            
            for i in range(int(request.POST['qty'])):
                pin=int(random.random()*10000000000000)
                s=int(random.random()*100000000)
                sn="SN"+str(s)
                t=Ticket(event=event,ticketType=request.POST['ttyp'],pin=pin,
                        serialNo=sn)
                t.save()
            return render_to_response('baseApp/ticket.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'event':event,'isaddevent':True})        
    
    else:
         form = AddEventForm()
         #return HttpResponse(form.as_p())
         return render_to_response('baseApp/addEvent.html', {'form':form.as_p(),'logged_in':request.user.is_authenticated(),'categories':categories})


@csrf_exempt
def ticket_view(request): 
    return HttpResponse('cut') 

@csrf_exempt
def suggest_view(request): 
    pass 




