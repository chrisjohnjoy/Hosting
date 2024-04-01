from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import CartItem, User, Customer, Employee, Medicine

class BaseUserForm(UserCreationForm):
    name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True)  # Add email field

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, is_customer=False, is_employee=False, is_medical_representative=False, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data.get('name')
        user.email = self.cleaned_data.get('email')  # Save email
        user.is_customer = is_customer
        user.is_employee = is_employee
        user.is_medical_representative = is_medical_representative

        user.save()
        return user

class CustomerSignupForm(BaseUserForm):
    address = forms.CharField(required=True)

    @transaction.atomic
    def save(self):
        user = super().save(is_customer=True)
        customer = Customer.objects.create(user=user)
        customer.phone_number = self.cleaned_data.get('phone_number')
        customer.address = self.cleaned_data.get('address')
        customer.save()
        return user

class EmployeeSignupForm(BaseUserForm):
    designation = forms.CharField(required=True)

    @transaction.atomic
    def save(self):
        user = super().save(is_employee=True)
        employee = Employee.objects.create(user=user)
        employee.phone_number = self.cleaned_data.get('phone_number')
        employee.designation = self.cleaned_data.get('designation')
        employee.save()
        return user

class MedicalRepresentativeSignupForm(BaseUserForm):
    company = forms.CharField(required=True)

    @transaction.atomic
    def save(self, is_medical_representative=True, commit=True):
        user = super().save(is_medical_representative=is_medical_representative, commit=commit)

        if commit:
            medical_representative = MedicalRepresentative.objects.create(user=user)
            medical_representative.phone_number = self.cleaned_data.get('phone_number')
            medical_representative.company = self.cleaned_data.get('company')
            medical_representative.save()

        return user


# Create a form for the LoginForm
# ... (your existing imports)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

# ... (your existing form classes)

# Create a form for the LoginForm
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("Invalid username or password. Please try again.")
            elif not user.is_active:
                raise forms.ValidationError("This account is currently inactive.")
        
        return cleaned_data

# Create a form for the CustomerProfile
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'address']
        exclude = ['password']

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    password = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.user:
            self.fields['name'].initial = self.instance.user.name
            self.fields['email'].initial = self.instance.user.email

# Create a form for the Medicine
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
                   'mfg_date': forms.DateInput(attrs={'class': 'date-picker'}),
                   'exp_date': forms.DateInput(attrs={'class': 'date-picker'}),
               }



# Create a form for the CartItem
class CartItemForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'})
    )
    remove = forms.BooleanField(
        required=False,
        initial=False,  
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Prescription

class PrescriptionUploadForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription']
        labels = {
            'prescription': 'Prescription Image or PDF',
        }
        widgets = {
            'prescription': forms.ClearableFileInput(attrs={'accept': 'image/*,application/pdf'}),
        }

    # Define the prescription field with validators within the Meta class
    prescription = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf'])]
    )

    # forms.py

# orders/forms.py
from django import forms

class OrderPlacementForm(forms.Form):
    name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField()
    medicine_details = forms.CharField(widget=forms.Textarea, help_text="Enter medicine details")
    razorpay_payment_id = forms.CharField(widget=forms.HiddenInput())

from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .models import User, DeliveryPerson

class DeliveryPersonSignupForm(UserCreationForm):
    phone_number = forms.CharField(label='Phone Number', max_length=20)
    vehicle_number = forms.CharField(label='Vehicle Number', max_length=20)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'name', 'phone_number', 'vehicle_number']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_delivery_person = True
        if commit:
            user.save()
            delivery_person = DeliveryPerson.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                vehicle_number=self.cleaned_data['vehicle_number']
            )
            delivery_person.save()
        return user

# views.py

from django.shortcuts import render
from .models import DeliveryPerson

def delivery_person_list(request):
    # Retrieve all delivery personnel from the database
    delivery_personnel = DeliveryPerson.objects.all()

    # Pass the delivery personnel queryset to the template for rendering
    return render(request, 'delivery_person_list.html', {'delivery_personnel': delivery_personnel})
