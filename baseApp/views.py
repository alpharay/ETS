# Create your views here.
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from models import *
from django.views.decorators.csrf import csrf_exempt

def home(request):
    t = loader.get_template('baseApp/index.html')
    c = Context(dict())
    return HttpResponse(t.render(c))
    
    
    
    
def categories_list(request, limit=100):
	category_list = EventCategory.objects.all()
	t = loader.get_template('baseApp/categorySearch.html')
	c = Context({'category_list':category_list})
	return HttpResponse(t.render(c))

def events_list(request, limit=100):
	event_list = Event.objects.all()
	t = loader.get_template('baseApp/eventSearch.html')
	c = Context({'event_list':event_list})
	return HttpResponse(t.render(c))

class EventForm(ModelForm):
	class Meta:
		model=Event
		#exclude=['post','author']
	
@csrf_exempt
def event_detail(request,id,showEvents=False):
	single_eventCat = EventCategory.objects.get(id=id)
	print single_eventCat	
	if showEvents:
		event = Event.objects.filter(post__id=id)
		print event
		#Start of form code
		if request.method == 'POST':
			event= Event(post=single_eventCat)
			form = EventForm(request.POST,instance=event)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(request.path)
		else:
			form = EventForm()
		#end of form code

	t = loader.get_template('baseApp/eventDetail.html') # to show the details of the event
	c = Context({'events':event,'single_eventCat':single_eventCat,'form':form.as_p()})
	return HttpResponse(t.render(c))



