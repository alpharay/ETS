from django.db import models
from django.contrib import admin

class Consumer(models.Model):
    #firstName= models.CharField(max_length=30)
    #otherName=models.CharField(max_length=30)    
    email=models.EmailField()
    phone=models.CharField(max_length=30)     
    def __unicode__(self):
        return self.firstName+' '+self.lastName

class ConsumerAdmin(admin.ModelAdmin):
    pass

class EventOrganizer(models.Model):
    name= models.CharField(max_length=60)
    services = models.TextField()
    averageRating=models.CharField(max_length=60)
    categories=models.ForeignKey(Category)
    phone=models.CharField(max_length=60)
    email=models.CharField(max_length=60)
    city=models.CharField(max_length=60)
    hours=models.CharField(max_length=60)
    def __unicode__(self):
		return self.name  
	
class EventOrganizerAdmin(admin.ModelAdmin):
    pass

class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    user=models.ForeignKey(EventOrganizer)
    date=models.DateField(auto_now_add=True)# to check the time the event was created
    
    def __unicode__(self):
        return self.name

class EventCategoryAdmin(admin.ModelAdmin):
    pass
    
class Event(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(EventCategory)
    venue = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    date=models.DateField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField()
    user=models.ForeignKey(EventOrganizer)    
    
    def __unicode__(self):
        return self.name

class EventAdmin(admin.ModelAdmin):
    pass
        

class Tickets(models.Model):
    ticketType =  models.CharField(max_length=30)
    price =  models.CharField(max_length=30)
    pin=models.CharField(max_length=30)    
    serialNo=models.CharField(max_length=30)
    event =  models.ForeignKey(Event)
    paid =  models.CharField(max_length=30)
    #order =  models.CharField(max_length=30)
    def __unicode__(self):
        return self.tag 

class TicketsAdmin(admin.ModelAdmin):
    pass
    
class Payment(models.Model):
    paymentType =  models.CharField(max_length=30)
    operator =  models.CharField(max_length=30)
    ticket =  models.ForeignKey(Tickets)
    phone=models.CharField(max_length=30)    
    date=models.DateField(auto_now_add=True)
    def __unicode__(self):
        return self.tag 

class PaymentAdmin(admin.ModelAdmin):
    pass
    
class Suggestions(models.Model):
    consumer =  models.ForeignKey(Event)
    suggestion =  models.TextField(max_length=30)
    date=models.DateField(auto_now_add=True)   
    
    def __unicode__(self):
        return self.tag 

class SuggestionsAdmin(admin.ModelAdmin):
    pass

class OutgoingSMS(models.Model):
    reciever =  models.CharField(max_length=30)
    message =  models.CharField(max_length=160)
    status=models.BooleanField()   
    date=models.DateField(auto_now_add=True) 
    time=models.TimeField()
    
    def __unicode__(self):
        return self.tag 

class OutgoingSMSAdmin(admin.ModelAdmin):
    pass
    
class IncomingSMS(models.Model):
	reciever =  models.CharField(max_length=30)
    message =  models.CharField(max_length=160)       
    date=models.DateField(auto_now_add=True) 
    time=models.TimeField()
    
    def __unicode__(self):
        return self.tag 

class IncomingSMSAdmin(admin.ModelAdmin):
    pass

        

admin.site.register(User,UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(SearchTag,SearchTagAdmin)
admin.site.register(Company,CompanyAdmin)
admin.site.register(Review,ReviewAdmin)
