from django.db import models
from django.contrib import admin

class Consumer(models.Model):
    first_name= models.CharField(max_length=30,blank=True)
    other_name=models.CharField(max_length=30,blank=True)    
    email=models.EmailField(blank=True)
    phone=models.CharField(max_length=30) 
    created=models.DateTimeField(auto_now_add=True)
        
    def __unicode__(self):
        return self.phone 

class ConsumerAdmin(admin.ModelAdmin):
    pass

class EventOrganizer(models.Model):
    name= models.CharField(max_length=60)
    natID = models.CharField(max_length=15)
    phone1=models.CharField(max_length=12)
    phone2=models.CharField(max_length=12,null=True)
    email=models.EmailField(null=True)
    created=models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name  
    
class EventOrganizerAdmin(admin.ModelAdmin):
    pass

class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    user=models.CharField(max_length=30)
    created=models.DateField(auto_now_add=True)# to check the time the event was created
    
    def __unicode__(self):
        return self.name

class EventCategoryAdmin(admin.ModelAdmin):
    pass
    
class Event(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(EventCategory)
    venue = models.CharField(max_length=30)
    locationX = models.CharField(max_length=30,blank=True)# *
    locationY = models.CharField(max_length=30,blank=True)# *
    event_date=models.DateField()
    created=models.DateField(auto_now_add=True)
    event_time=models.TimeField()
    event_Rep=models.ForeignKey(EventOrganizer)   
    #poster = models.ImageField(upload_to='/tmp',null=True) 
    def __unicode__(self):
        return self.name

class EventAdmin(admin.ModelAdmin):
    pass
        

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
    pass


class Cart(models.Model):
    consumer=models.ForeignKey(Consumer) 
    value=models.DecimalField(max_digits=10,decimal_places=2)
    def __unicode__(self):
        return self.consumer
    
class CartAdmin(admin.ModelAdmin):
    pass

    
class Payment(models.Model):
    paymentType =  models.CharField(max_length=20)
    operator =  models.CharField(max_length=20)
    cart =  models.ForeignKey(Cart)   
    TransactionID =  models.CharField(max_length=20)
    created=models.DateField(auto_now_add=True)
    paid =  models.BooleanField()
    
    def __unicode__(self):
        return self.paymentType+' '+self.cart 

class PaymentAdmin(admin.ModelAdmin):
    pass
    
class Suggestion(models.Model):
    consumer =  models.ForeignKey(Event)
    suggestion =  models.TextField(max_length=30)
    created=models.DateField(auto_now_add=True)   
    
    def __unicode__(self):
        return self.suggestion 

class SuggestionAdmin(admin.ModelAdmin):
    pass

class OutgoingSMS(models.Model):
    reciever=models.ForeignKey(Consumer)
    message=models.CharField(max_length=160)
    sent=models.BooleanField()#chn from status >>> sent   
    created=models.DateField(auto_now_add=True) 
    time=models.TimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.message+' ' +reciever

class OutgoingSMSAdmin(admin.ModelAdmin):
    pass
    
class IncomingSMS(models.Model):
    sender=models.CharField(max_length=30)
    message=models.CharField(max_length=160)       
    created=models.DateField(auto_now_add=True) 
    time=models.TimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.tag 

class IncomingSMSAdmin(admin.ModelAdmin):
    pass

    
class CartAdmin(admin.ModelAdmin):
    pass

class Order(models.Model):
    cart=models.ForeignKey(Cart) 
    ticket=models.ForeignKey(Ticket) 
    def __unicode__(self):
        return self.id
    
class OrderAdmin(admin.ModelAdmin):
    pass
    

admin.site.register(Consumer,ConsumerAdmin)
admin.site.register(EventOrganizer,EventOrganizerAdmin)
admin.site.register(EventCategory,EventCategoryAdmin)
admin.site.register(Event,EventAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Suggestion,SuggestionAdmin)
admin.site.register(OutgoingSMS,OutgoingSMSAdmin)
admin.site.register(IncomingSMS,IncomingSMSAdmin)

# Create your models here.
