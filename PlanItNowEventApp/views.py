from django.shortcuts import render,HttpResponse,redirect
from .models import Customer,PlanItNowEvents,PlanItNowCategory,cart,EventBookingCustForm,BookingDetails,UserProfile
from .forms import RegisterForm,userAuthentication,PlanItNowEventsFormCrud,EventBookingForm,ContactForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse


# Create your views here.
def home(request):
    return render(request,'index.html')

def eventpage(request):
    category=PlanItNowCategory.objects.all()  #retrive all data from model PlanItNowCategory
    active_events=PlanItNowEvents.objects.active()  #retrive all data from model PlanItNowEvents
    print("Active Events are:",active_events)
    events=PlanItNowEvents.objects.filter(is_eventdeleted=False) 
    context={'category':category,'events':events}
    return render(request,'events.html',context)

def range(request):
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')
    sort_by = request.GET.get('sort')

    # Start with filtered queryset
    events = PlanItNowEvents.objects.all()

    # Apply price range filter
    if min_price and max_price:
        q1 = Q(eventPrice__gte=min_price)
        q2 = Q(eventPrice__lte=max_price)
        events = events.filter(q1 & q2)

    # Apply sorting
    if sort_by == 'price_asc':
        events = events.order_by('eventPrice')
    elif sort_by == 'price_desc':
        events = events.order_by('-eventPrice')
    elif sort_by == 'rating_asc':
        events = events.order_by('eventRating')
    elif sort_by == 'rating_desc':
        events = events.order_by('-eventRating')

    category = PlanItNowCategory.objects.all()

    context = {
        'events': events,
        'category': category,
    }

    return render(request, 'events.html', context)

def eventcategory(request,id):
    print(id)
    category=PlanItNowCategory.objects.all()
    events=PlanItNowEvents.objects.filter(eventCategory=id)
    return render(request,'events.html',{'category':category,'events':events})

def register(request):
    if request.method=='POST':
        registerForm=RegisterForm(request.POST)
        if registerForm.is_valid():
            registerForm.save()
            return redirect('home')
        else:
            return redirect('register')
    else:
        registerForm=RegisterForm()
        return render(request,'register.html',{'pd':registerForm})
    
# @login_required
# def profileView(request):
#     user = request.user
#     bookings = BookingDetails.objects.filter(user=user)

#     # Initialize the form with the current user's information
#     if request.method == 'POST':
#         form = RegisterForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()  # Save updated user info
#             return redirect('profile')  # Redirect to the profile page after update
#     else:
#         form = RegisterForm(instance=user)

#     return render(request, 'profile.html', {
#         'form': form,
#         'bookings': bookings
#     })
    
def loginuser(request):
    if request.method=="POST":
        uname=request.POST["username"]
        upass=request.POST["password"]
        print(uname)
        print(upass)
        user=authenticate(request,username=uname,password=upass)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return redirect('loginuser')

    else:
        userForm=userAuthentication()
        return render(request,'loginuser.html',{'userForm':userForm})
        
def signout(request):
    logout(request)
    return redirect('home')


from django.shortcuts import get_object_or_404

@login_required(login_url='loginuser')
def addtocart(request, id):
    customer = request.user  
    event = get_object_or_404(PlanItNowEvents, id=id)  

    # Check if event is already in cart
    cart_item, created = cart.objects.get_or_create(uid=customer, eid=event)

    context = {'events': [event]}  # Ensure it's in a list for template rendering
    if not created:
        context['msg'] = "Already added to Wishlist !! Please check in cart."
    else:
        context['success'] = "Successfully added to Wishlist !!"

    return render(request, 'viewcards.html', context)

def viewCards(request,id):
    events=PlanItNowEvents.objects.filter(id=id)
    
    return render(request,'viewcards.html',{'events':events})

@login_required(login_url='loginuser')
def viewcart(request):
    customer = request.user  
    cart_items = cart.objects.filter(uid=customer)

    if not cart_items.exists():  #Handle empty cart case
        return render(request, 'viewcart.html', {'events': [], 'totalCount': 0, 'totalamount': 0})

    totalCount = sum(item.qty for item in cart_items)
    totalamount = sum(item.eid.eventPrice * item.qty for item in cart_items)

    return render(request, 'viewcart.html', {'events': cart_items, 'totalCount': totalCount, 'totalamount': totalamount})

def changeqty(request,qv,id):
    cartqtydetails=cart.objects.filter(id=id)
    print(cartqtydetails)

    if qv=='1':
        totalcartqty=cartqtydetails[0].qty+1
        cartqtydetails.update(qty=totalcartqty)
    else:
        if cartqtydetails[0].qty>1:
            totalcartqty=cartqtydetails[0].qty-1
            cartqtydetails.update(qty=totalcartqty)
    return redirect('viewcart')


def eventchangeqty(request,qv,id):
    eventqtydetails=PlanItNowEvents.objects.filter(id=id)
    print(eventqtydetails)
    
    if qv=='1':
        totaleventqty=eventqtydetails[0].quantity+1
        eventqtydetails.update(quantity=totaleventqty)
    else:
        if eventqtydetails[0].quantity>1:
            totaleventqty=eventqtydetails[0].quantity-1
            eventqtydetails.update(quantity=totaleventqty)

    events=PlanItNowEvents.objects.filter(id=id)
    return render(request,'viewcards.html',{'events':events})

def searchanything(request):
    if request.method=="POST":
        searchdata=request.POST['search']
        print(searchdata)
        result=PlanItNowEvents.objects.filter(eventTitle__icontains=searchdata)
        print(result)
        return render(request,'searchanything.html',{'result':result})
    else:
        return render(request,'searchanything.html')


def removeevent(request,id):
    event=cart.objects.filter(id=id)
    print(event)
    event.delete()
    return redirect('viewcart')

@login_required(login_url='loginuser')
def checkout(request, id):
    # Get event details or return 404 if not found
    event = get_object_or_404(PlanItNowEvents, id=id)

    # Check if event is sold out
    if event.is_sold_out():
        return HttpResponse("This event is sold out.", status=403)

    # Check if the event exists in the user's cart
    cart_entry = cart.objects.filter(uid=request.user, eid=event).first()

    # Set initial ticket quantity
    initial_ticket_quantity = cart_entry.qty if cart_entry else event.quantity

    # Prevent overbooking
    if initial_ticket_quantity > event.totalTickets:
        return HttpResponse("Not enough tickets available.", status=403)

    # Set initial data for the form
    initial_data = {
        'event_date_time': event.eventDateTime,
        'ticket_quantity': initial_ticket_quantity
    }

    if request.method == 'POST':
        custdetailsForm = EventBookingForm(request.POST)
        if custdetailsForm.is_valid():
            if initial_ticket_quantity > event.totalTickets:
                return HttpResponse("Sorry, not enough tickets available.", status=400)
            
            customer = custdetailsForm.save(commit=False)
            customer.user = request.user
            customer.event = event
            customer.event_date_time = event.eventDateTime
            customer.ticket_quantity = initial_ticket_quantity
            customer.save()

            # Update available tickets
            event.totalTickets -= initial_ticket_quantity
            event.save()

            # Remove event from cart after checkout
            if cart_entry:
                cart_entry.delete()

            return redirect('checkoutdetail')

    else:
        custdetailsForm = EventBookingForm(initial=initial_data)

    return render(request, 'checkout.html', {'pd': custdetailsForm, 'events': event})

def checkoutdetail(request):
    userid = request.user.id
    print(f"User ID: {userid}")

    latest_booking = EventBookingCustForm.objects.filter(user=userid).order_by('-id').first()
    print(f"Latest Booking: {latest_booking}")

    if not latest_booking:
        return HttpResponse("No bookings found!", status=404)

    events = latest_booking.event
    print(f"Event: {events}")

    if not events:
        return HttpResponse("Event details not found!", status=404)

    print(f"Event Title: {events.eventTitle}")
    print(f"Event Image: {events.eventImage}")  # Check if this field exists
    print(f"Event Price: {events.eventPrice}")

    totalamount = events.eventPrice * latest_booking.ticket_quantity
    print(f"Total Amount: {totalamount}")

    # ================= PayPal Code ==================== #
    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': totalamount,
        'item_name': 'PlanItNowEvent',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paypalsuccess')}",
        'cancel_url': f"http://{host}{reverse('paypalfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    return render(request, 'checkoutdetail.html', {
        'events': events,
        'totalamount': totalamount,
        'custformdetail': latest_booking,
        'paypalpayment': paypal_payment
    })

import uuid
from django.shortcuts import render
from .models import PlanItNowEvents, EventBookingCustForm, BookingDetails
from django.contrib import messages 
from django.core.mail import send_mail

def paypalsuccess(request):
    userid = request.user.id

    # Get the latest event booked by the user
    latest_booking = EventBookingCustForm.objects.filter(user=userid).order_by('-id').first()

    if not latest_booking:
        messages.error(request, "No recent booking found.")
        return render(request, 'paymentsuccess.html', {'error': 'No recent booking found.'})

    event = latest_booking.event
    quantity = latest_booking.ticket_quantity

    # Calculate amount
    totalamount = event.eventPrice * quantity

    transaction_id = f"TXN{uuid.uuid4().hex[:10]}"

    # Create the booking for the selected event only
    booking = BookingDetails.objects.create(
        user=request.user,
        event=event,
        transaction_id=f"TXN{uuid.uuid4().hex[:10]}",
        quantity=latest_booking.ticket_quantity,
        amount_paid=totalamount,
        payment_status='Booking Successfull'
    )

    send_mail(
        subject="Booking Confirmation - PlanItNow",
        message=f"Dear {request.user.username},\n\n"
                f"Your booking for {event.eventTitle} is confirmed!\n\n"
                f"Event Details:\n"
                f"Venue: {event.eventVenue}\n"
                f"Date & Time: {event.eventDateTime}\n"
                f"Tickets: {quantity}\n"
                f"Transaction ID: {transaction_id}\n\n"
                f"Thank you for booking with us!\n\n"
                f"PlanItNow Team",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False
    )

    # Remove the event from the cart after booking
    cart.objects.filter(uid=request.user, eid=event).delete()

    return render(request, 'paymentsuccess.html', {'bookings': booking, 'custformdetail': latest_booking})

def booking(request):
    bookings=BookingDetails.objects.filter(user=request.user.id).order_by('-payment_date')
    return render(request,'bookinghistory.html',{'bookings':bookings})

def paypalfailed(request):

    return render(request,'paymentfailed.html')

def addevent(request):
    if request.method=='POST':
        eventForm=PlanItNowEventsFormCrud(request.POST,request.FILES)
        if eventForm.is_valid():
            eventForm.save()
            return redirect('home')
        else:
            return redirect('addevent')
    else:
        form=PlanItNowEventsFormCrud() 
        return render(request,'addeventcrud.html',{'addevent':form})

def updateevent(request,id):
    event = PlanItNowEvents.objects.get(id=id) 

    if request.method == 'POST':
        form = PlanItNowEventsFormCrud(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('home')  
        else:
            return render(request, 'updateevent.html', {'form': form})  
    else:
        form = PlanItNowEventsFormCrud(instance=event) 
        return render(request, 'updateevent.html', {'form': form})
    
def updateevents(request):
    return redirect("eventpage")

def deleteeventcrud(request,id):
    event=PlanItNowEvents.objects.get(id=id,is_eventdeleted=False)
    event.is_eventdeleted=True
    event.delete_eventdetails=timezone.now()
    event.save()
    return redirect('home')

def aboutus(request):
    return render(request,'aboutus.html')

import random
from django.contrib import messages 
from django.core.mail import send_mail

def forgotpassword(request):
    if request.method == 'POST':
        email= request.POST.get('email')

        users=User.objects.filter(email=email)
        if users.exists():
            user=users.first()
            otp=random.randint(100000,999999)
            request.session['reset_otp']=otp
            request.session['reset_email']=email
            request.session['otp_purpose']="login"

            subject = "Your Password Reset OTP"  
            message = f"Dear {user.username},\n\nYour OTP for passsword reset is: {otp}\n\nPlease enter proper OTP to reset password and It will be valid for 5 minute.\n\nBest Regards,\nYour Support Team."

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return redirect('verifyotp')
        
        else:
            messages.error(request,"Email not found! Please enter a registered email.")
            return render(request,'forgotpassword.html')
    
    return render(request,'forgotpassword.html')
        
def verifyotp(request):
    if request.method == 'POST':
        enterotp=request.POST.get('otp')
        storedotp=request.session.get('reset_otp')
        otppurpose=request.session.get('otp_purpose','')

        if storedotp and enterotp == str(storedotp):
            if otppurpose == 'login':
                return redirect('resetpassword')
            elif otppurpose == 'payment':
                return redirect('paypalsuccess')
            else:
                return redirect('home')
            
        else:
            messages.error(request,'Invalid OTP! Please Try Again.')  

    return render(request,'verifyotp.html')  
        
def resetpassword(request):
    if request.method == 'POST':
        newpassword=request.POST['new_password']
        confirmpassword=request.POST['confirm_password']
        email=request.session.get('reset_email')

        if newpassword == confirmpassword:
            try:
                user = User.objects.get(email=email)
                user.set_password(newpassword)
                user.save()

                # Clear session data: 
                del request.session['reset_otp']
                del request.session['reset_email']

                messages.success(request,"Password reset successfull! You can login now!")
                return redirect('loginuser')
            
            except User.DoesNotExist:
                messages.error(request,"Something went wrong!! Try Again!!")
                return redirect('forgotpassword')
        else:
            messages.error(request,'Password do not match !! Try Again!!')
            return render(request,'resetpassword.html')
        
    return render(request,'resetpassword.html')

from django.urls import reverse
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import customerserializer 

class crudapi(APIView):
    def get(self,request):    #self used then its a class method otherwise its a static method.
        custid=request.data.get('id',None) 
        if custid:
            try:
                customer=User.objects.get(id=custid)
                custData=customerserializer(customer)
                return Response(custData.data,status=status.HTTP_200_OK)
            except:
                return Response({'Msg':'For this id no data will be available!!'},status=status.HTTP_404_NOT_FOUND)
        else:
            customer=User.objects.all()
            print(customer)
            custData=customerserializer(customer,many=True)
            return Response(custData.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        custdetailData=request.data  #Data will be in single Quotes.
        custData=customerserializer(data=custdetailData)
        if custData.is_valid():
            custData.save()
            return Response({'Msg':'Data is successfully stored!!'},status=status.HTTP_200_OK)
        
        return Response({'Msg':'No data will be available!!'},status=status.HTTP_404_NOT_FOUND)
    
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contactus(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")  
            return redirect("contactus")  

    return render(request, "contactus.html", {"form": form})


def services(requesrt):
    return render(requesrt,'services.html')

@login_required
def profileView(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    bookings = BookingDetails.objects.filter(user=request.user).order_by('-payment_date')
    return render(request, 'profile.html', {'profile': profile, 'bookings': bookings})

@login_required
def editProfileview(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'editProfile.html', {'form': form})

# def register(request):
#     if request.method=='POST':
#         print("Request Is",request.method)
#         custId=request.POST['custid'] 
#         custName=request.POST['custname']  
#         custSurname=request.POST['custsurname']
#         custEmail=request.POST['custemail'] 
#         custContact=request.POST['custcontact']  
#         cust=Customer.objects.create(customerId=custId,customerName=custName,customerSurname=custSurname,customerEmail=custEmail,customerContact=custContact)
#         cust.save()
#         return HttpResponse("Form Data is submitted successfully !!!")
#     else:
#         print("Request Is",request.method)
#         return render(request,"register.html")
    
# def showdetails(request):
#     custdetails=Customer.objects.all()
#     return render(request,'details.html',{'customerDetails':custdetails})

# def deletecust(request,id):
#     custdetails=Customer.objects.filter(id=id)
#     custdetails.delete()
#     return redirect('/showalldetails')

# def edits(request,id):
#     if request.method=="POST":
#         print("Request Is",request.method)
#         custId=request.POST['custid'] 
#         custName=request.POST['custname']  
#         custSurname=request.POST['custsurname']
#         custEmail=request.POST['custemail'] 
#         custContact=request.POST['custcontact'] 
#         n=Customer.objects.filter(id=id)
#         n.update(customerId=custId,customerName=custName,customerSurname=custSurname,customerEmail=custEmail,customerContact=custContact)
#         return redirect('/showalldetails')
#     else:
#         custdetails=Customer.objects.get(id=id)
#         return render(request,'edit.html',{'customerDetails':custdetails})

# def addevent(request):
#     if request.method=='POST':
#         print("Request Is",request.method)
#         eventT=request.POST['eventtitle'] 
#         eventD=request.POST['eventdesc']  
#         eventP=request.POST['eventprice']
#         eventI=request.POST['eventimage'] 
#         eventR=request.POST['eventrating']  
#         # eventC=request.POST['eventcategory'] 
#         event=PlanItNowEvents.objects.create(eventTitle=eventT,eventDesc=eventD,eventPrice=eventP,eventImage=eventI,eventRating=eventR)
#         event.save()
#         return redirect('home')
#         # return HttpResponse("Form Data is submitted successfully !!!")
#     else:
#         print("Request Is",request.method)
#         return render(request,"addEvents.html")
    
# def showeventdetails(request):
#     eventdetails=PlanItNowEvents.objects.all()
#     return render(request,'updateevent.html',{'eventDetails':eventdetails})

# def deleteevent(request,id):
#     eventdetails=PlanItNowEvents.objects.filter(id=id)
#     eventdetails.delete()
#     return redirect('/showalleventdetails')

# def editevent(request,id):
#     if request.method=="POST":
#         print("Request Is",request.method)
#         eventT=request.POST['eventtitle'] 
#         eventD=request.POST['eventdesc']  
#         eventP=request.POST['eventprice']
#         eventI=request.POST['eventimage'] 
#         eventR=request.POST['eventrating']  
#         # eventC=request.POST['eventcategory']  
#         e=PlanItNowEvents.objects.filter(id=id)
#         e.update(eventTitle=eventT,eventDesc=eventD,eventPrice=eventP,eventImage=eventI,eventRating=eventR)
#         return redirect('/showalleventdetails')
#     else:
#         eventdetails=PlanItNowEvents.objects.get(id=id)
#         return render(request,'eventedit.html',{'eventDetails':eventdetails})
    
