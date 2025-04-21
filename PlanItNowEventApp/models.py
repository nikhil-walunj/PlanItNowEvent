from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class PlanItNowCategory(models.Model):
    categoryName=models.CharField(max_length=100)
    categoryDesc=models.TextField()

    def __str__(self):
        return self.categoryName
    
class PlanItNowEventManager(models.Manager):
    def active(self):
        return self.filter(is_eventdeleted=False)
    
class PlanItNowEvents(models.Model):
    eventTitle=models.CharField(max_length=100)
    eventDesc=models.TextField()
    eventPrice=models.DecimalField(max_digits=10,decimal_places=2)
    eventImage=models.ImageField(upload_to='images/')
    eventDateTime = models.CharField(max_length=100)  
    eventVenue = models.CharField(max_length=255)
    eventRating=models.DecimalField(max_digits=2,decimal_places=1)
    eventCategory=models.ForeignKey(PlanItNowCategory,on_delete=models.CASCADE,null=True,blank=True)
    totalTickets = models.IntegerField(default=100) 
    quantity=models.IntegerField(default=1)
    is_eventdeleted=models.BooleanField(default=False)
    delete_eventdetails=models.DateTimeField(null=True,blank=True)
    objects = PlanItNowEventManager()

    def __str__(self):
        return self.eventTitle
    
    def is_sold_out(self):
        return self.totalTickets <= 0



class Customer(models.Model):
    customerId=models.IntegerField()   
    customerName=models.CharField(max_length=100)  
    customerSurname=models.TextField()   
    customerEmail=models.EmailField(max_length=30)
    customerContact=models.BigIntegerField()   
    
    def __str__(self):
        return self.customerName
    
class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    eid=models.ForeignKey(PlanItNowEvents,on_delete=models.CASCADE,db_column='eid')
    qty=models.IntegerField(default=1)

class EventBookingCustForm(models.Model):
    event = models.ForeignKey(PlanItNowEvents, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    event_date_time = models.CharField(max_length=100) 
    ticket_quantity = models.IntegerField()
    ticket_buy_date_time = models.DateTimeField(default=datetime.now)  
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.event:
            self.event_date_time = self.event.eventDateTime 

            cart_entry = cart.objects.filter(uid=self.user, eid=self.event).first()

            if cart_entry:
                self.ticket_quantity = cart_entry.qty  
            else:
                self.ticket_quantity = self.event.quantity 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} booked {self.event.eventTitle}"

class BookingDetails(models.Model):
    STATUS_CHOICES = [
        ('BOOKING SUCCESSFULL','Booking Successfull'),
        ('BOOKING FAILED','Booking Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(PlanItNowEvents, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    quantity=models.PositiveIntegerField(default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='Booking Successfull')
    payment_date = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.user.username} - {self.event.eventTitle}"
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/profile.jpg', blank=True)
    contact_number = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Male')
    area_pincode = models.CharField(max_length=10)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"