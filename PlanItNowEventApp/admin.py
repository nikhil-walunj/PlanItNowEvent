from django.contrib import admin
from .models import PlanItNowCategory,PlanItNowEvents,Customer,cart,EventBookingCustForm,BookingDetails,ContactMessage,UserProfile

# Register your models here.

class PlanItNowCategoryAdmin(admin.ModelAdmin):
    list_display=['categoryName','categoryDesc']
admin.site.register(PlanItNowCategory,PlanItNowCategoryAdmin)

class PlanItNowEventsAdmin(admin.ModelAdmin):
    list_display=['eventTitle','eventDesc','eventPrice','eventImage','eventDateTime','eventVenue','eventRating','eventCategory','totalTickets','quantity','is_eventdeleted','delete_eventdetails']
admin.site.register(PlanItNowEvents,PlanItNowEventsAdmin)

class Customer_Admin(admin.ModelAdmin):
    list_display = ['customerId','customerName','customerSurname','customerEmail','customerContact']
admin.site.register(Customer,Customer_Admin)

class cartAdmin(admin.ModelAdmin):
    list_display=['uid','eid','qty']
admin.site.register(cart,cartAdmin)

class EventBookingCustFormAdmin(admin.ModelAdmin):
    list_display=['event','name','email','phone','event_date_time','ticket_quantity','ticket_buy_date_time','created_at']
admin.site.register(EventBookingCustForm,EventBookingCustFormAdmin)
   
class BookingDetailsAdmin(admin.ModelAdmin):
    list_display=['id','user','event','transaction_id','quantity','amount_paid','payment_status','payment_date','created_at']    
admin.site.register(BookingDetails,BookingDetailsAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display=['name','email','message']
admin.site.register(ContactMessage,ContactMessageAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number', 'gender', 'city', 'state')
    search_fields = ('user__username', 'contact_number', 'city', 'state')
admin.site.register(UserProfile, UserProfileAdmin)