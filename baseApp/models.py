from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User	# necessary for the user profile to work

class UserProfile(models.Model):
    user = models.OneToOneField(User)        # This field is required.
    phone=models.CharField(max_length=12)
    isOrganizingEvent = models.BooleanField()
    if isOrganizingEvent:
        natID = models.CharField(max_length=15, blank=True)
        phone2=models.CharField(max_length=12,null=True)


#class Consumer(models.Model):
#    first_name= models.CharField(max_length=30,blank=True)
#    other_name= models.CharField(max_length=30,blank=True)    
#    email=models.EmailField(blank=True)
#    phone=models.CharField(max_length=12) 
#    created=models.DateTimeField(auto_now_add=True)
#    def __unicode__(self):
#        return self.phone 
#    
#class ConsumerAdmin(admin.ModelAdmin):
#    list_display = ('first_name','other_name','phone','email','created')
#    search_fields = ('first_name','other_name')
#    list_filter = ('created',)
#
#    
#class EventOrganizer(models.Model):
#    name= models.CharField(max_length=60)
#    natID = models.CharField(max_length=15)
#    phone1=models.CharField(max_length=12)
#    phone2=models.CharField(max_length=12,null=True)
#    email=models.EmailField(null=True)
#    created=models.DateTimeField(auto_now_add=True)
#    def __unicode__(self):
#        return self.name  
#    
#class EventOrganizerAdmin(admin.ModelAdmin):
#    list_display = ('name','phone1','email','created','natID')
#    search_fields = ('name',)
#    list_filter = ('created',)
#    #inlines = [EventInLine]

class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    user=models.CharField(max_length=30)
    created=models.DateField(auto_now_add=True)# to check the time the event was created
    def __unicode__(self):
        return self.name

class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','user','created')
    search_fields = ('name',)
    list_filter = ('created',)
    #inlines = [EventInLine]



class Event(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(EventCategory)
    venue = models.CharField(max_length=30)
    locationX = models.CharField(max_length=30,blank=True)# *
    locationY = models.CharField(max_length=30,blank=True)# *
    event_date=models.DateTimeField()
    created=models.DateField(auto_now_add=True)
    #event_Rep=models.ForeignKey(EventOrganizer)
    event_Rep=models.ForeignKey(User)   
    #poster = models.ImageField(upload_to='/tmp',null=True) 
    def __unicode__(self):
        return self.name
    
class EventAdmin(admin.ModelAdmin):
    list_display = ('name','event_date','created','event_Rep')
    search_fields = ('category','event_date','venue')
    list_filter = ('event_date','created')


class Ticket(models.Model):
    ticketType =  models.CharField(max_length=30)
    price =  models.DecimalField(max_digits=10,decimal_places=2)
    pin=models.CharField(max_length=30)    
    serialNo=models.CharField(max_length=30)
    event =  models.ForeignKey(Event)
    #order =  models.CharField(max_length=30)
    def __unicode__(self):
        return self.ticketType 

class TicketAdmin(admin.ModelAdmin):
    list_display = ('pin','serialNo','ticketType')
    search_fields = ('ticketType','event')



class Cart(models.Model):
    transactionID =  models.CharField(max_length=20)
    consumer=models.ForeignKey(Ticket) 
    tickets=models.ForeignKey(User) 
    value=models.DecimalField(max_digits=10,decimal_places=2)
    paymentType =  models.CharField(max_length=20)
    operator =  models.CharField(max_length=20)
    created=models.DateTimeField(auto_now_add=True)
    paid =  models.BooleanField()
    def __unicode__(self):
        return self.paymentType+' '+self.cart 

class CartAdmin(admin.ModelAdmin):
    list_display = ('consumer','transactionID','paymentType','created','value','paid')
    search_fields = ('transactionID','cart','value','created')
    list_filter = ('created','paid')
    #inlines = [TicketInLine]
        
class Suggestion(models.Model):
    consumer =  models.ForeignKey(User,blank=True)
    suggestion =  models.TextField(max_length=30)
    created=models.DateField(auto_now_add=True)   
    def __unicode__(self):
        return self.suggestion 

class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('consumer','created')
    list_filter = ('created',)


class OutgoingSMS(models.Model):
    #receiver=models.ForeignKey(Consumer)
    receiver=models.ForeignKey(User)
    message=models.CharField(max_length=160)
    sent=models.BooleanField()	#chn from status >>> sent   
    created=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.message+' '+self.receiver

class OutgoingSMSAdmin(admin.ModelAdmin):
    list_display = ('receiver','created','sent')
    search_fields = ('receiver','sent')
    list_filter = ('created',)

    
class IncomingSMS(models.Model):
    sender=models.CharField(max_length=30)
    message=models.CharField(max_length=160)       
    created=models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.tag 

class IncomingSMSAdmin(admin.ModelAdmin):
    list_display = ('sender','created')
    search_fields = ('sender',)
    list_filter = ('created',)


#admin.site.register(Consumer,ConsumerAdmin)
#admin.site.register(EventOrganizer,EventOrganizerAdmin)
admin.site.register(EventCategory,EventCategoryAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Ticket,TicketAdmin)
#admin.site.register(Payment,PaymentAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Suggestion,SuggestionAdmin)
admin.site.register(OutgoingSMS,OutgoingSMSAdmin)
admin.site.register(IncomingSMS,IncomingSMSAdmin)

# Create your models here.
