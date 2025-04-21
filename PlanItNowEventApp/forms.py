from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import PlanItNowEvents, EventBookingCustForm, ContactMessage,UserProfile
import re

class RegisterForm(UserCreationForm):
    password1=forms.CharField(label="Enter password:",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label="Confirm password:",widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

        labels={
            'username':'Enter Username:',
            'first_name':'Enter First Name:',
            'last_name':'Enter Last Name:',
            'email':'Enter Email:',
        }

        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8 or not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must be at least 8 characters long and include a capital letter.")
        return password

class userAuthentication(AuthenticationForm):
    username=forms.CharField(label="Enter Username:",widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="Enter Password:",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','password']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('username') or not cleaned_data.get('password'):
            raise forms.ValidationError("Both fields are required.")

class PlanItNowEventsFormCrud(forms.ModelForm):
    class Meta:
        model=PlanItNowEvents
        fields=['eventTitle','eventDesc','eventPrice','eventImage','eventDateTime','eventVenue','eventRating','eventCategory','quantity']


class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBookingCustForm
        fields = ['ticket_buy_date_time', 'name', 'email', 'phone','ticket_quantity', 'event_date_time']
        
        labels = {
            'ticket_buy_date_time': 'Booking Date & Time',
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Contact Number',
            'ticket_quantity': 'Number of Tickets',
            'event_date_time': 'Event Date & Time'
        }

        widgets = {
            'ticket_buy_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly':True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'ticket_quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),  
            'event_date_time': forms.DateTimeInput(attrs={'class': 'form-control', 'readonly': True}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_ticket_quantity(self):
        qty = self.cleaned_data.get('ticket_quantity')
        if qty < 1 or qty > 5:
            raise forms.ValidationError("You can book between 1 and 5 tickets.")
        return qty

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'message': 'Your Message',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type your message here'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[A-Za-z\s]+$', name):
            raise forms.ValidationError("Name should only contain alphabets and spaces.")
        if len(name.strip()) < 3:
            raise forms.ValidationError("Name must be at least 3 characters long.")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

    def clean_message(self):
        msg = self.cleaned_data.get('message')
        if len(msg) < 10:
            raise forms.ValidationError("Message should be at least 10 characters long.")
        return msg

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'profile_image', 'contact_number', 'birthday', 'gender',
            'area_pincode', 'address_line1', 'address_line2',
            'landmark', 'city', 'state'
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not re.match(r'^\d{10}$', contact):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return contact

    def clean_area_pincode(self):
        pin = self.cleaned_data.get('area_pincode')
        if not re.match(r'^\d{6}$', str(pin)):
            raise forms.ValidationError("Enter a valid 6-digit pincode.")
        return pin
        